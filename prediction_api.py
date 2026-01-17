"""
Prediction API for AI-Powered Crop Pest Classification System
Provides prediction endpoints and pesticide recommendations
"""

import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import base64
from typing import Dict, List
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from pesticide_database import get_pesticide_recommendations, get_safety_guidelines

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BEST_MODEL_PATH = "model/best_model.keras"
FINAL_MODEL_PATH = "model/final_model.keras"
CLASS_INDICES_PATH = "model/class_indices.json"
COMBINED_DATASET_DIR = "dataset/combined_dataset"

class PestClassifier:
    def __init__(self):
        self.model = None
        self.class_names = []
        self._load()

    def _load(self):
        model_path = BEST_MODEL_PATH if os.path.exists(BEST_MODEL_PATH) else FINAL_MODEL_PATH
        if not os.path.exists(model_path):
            logger.error("Model file not found. Please train the model first.")
            return
        # Load without compiling to avoid custom metric deserialization issues
        self.model = tf.keras.models.load_model(model_path, compile=False)
        
        # Get number of classes from model output shape
        num_classes = self.model.output_shape[-1]
        
        if os.path.exists(CLASS_INDICES_PATH):
            with open(CLASS_INDICES_PATH, "r") as f:
                class_indices = json.load(f)
            # class_indices is mapping name->index; convert to list ordered by index
            self.class_names = [None] * len(class_indices)
            for name, idx in class_indices.items():
                if idx < len(self.class_names):
                    self.class_names[idx] = name
            # fill any None slots conservatively
            self.class_names = [n if n is not None else f"class_{i}" for i, n in enumerate(self.class_names)]
        else:
            # Try to infer class names from the combined dataset directory (alphabetical order)
            try:
                if os.path.isdir(COMBINED_DATASET_DIR):
                    inferred = sorted([d for d in os.listdir(COMBINED_DATASET_DIR)
                                       if os.path.isdir(os.path.join(COMBINED_DATASET_DIR, d))])
                    if len(inferred) == num_classes:
                        self.class_names = inferred
                        # Persist for next runs
                        mapping = {name: i for i, name in enumerate(self.class_names)}
                        os.makedirs(os.path.dirname(CLASS_INDICES_PATH), exist_ok=True)
                        with open(CLASS_INDICES_PATH, "w") as f:
                            json.dump(mapping, f, indent=2)
                        logger.info(f"Inferred {len(self.class_names)} classes from {COMBINED_DATASET_DIR} and saved to {CLASS_INDICES_PATH}")
                    else:
                        logger.warning(f"Could not infer classes: model has {num_classes} outputs but found {len(inferred)} folders in {COMBINED_DATASET_DIR}")
                        self.class_names = [f"class_{i}" for i in range(num_classes)]
                else:
                    logger.warning(f"Combined dataset dir not found: {COMBINED_DATASET_DIR}")
                    self.class_names = [f"class_{i}" for i in range(num_classes)]
            except Exception:
                logger.exception("Failed to infer class names; falling back to generic names")
                self.class_names = [f"class_{i}" for i in range(num_classes)]
        
        logger.info(f"Loaded model: {model_path} with {len(self.class_names)} classes")

    @staticmethod
    def analyze_leaf_likelihood(image: Image.Image) -> dict:
        """Lightweight heuristic leaf detector to filter obvious non-leaf images.
        Returns metrics and an is_leaf boolean.
        """
        result = {"green_ratio": 0.0, "exg_ratio": 0.0, "sat_mean": 0.0, "skin_ratio": 0.0, "leaf_score": 0.0, "is_leaf": False}
        try:
            small = image.convert("RGB").resize((256, 256))
            arr = np.asarray(small, dtype=np.uint8)
            r = arr[..., 0].astype(np.int16)
            g = arr[..., 1].astype(np.int16)
            b = arr[..., 2].astype(np.int16)

            # Excess Green index (vegetation cue)
            exg = 2 * g - r - b
            exg_ratio = float(np.count_nonzero(exg > 0)) / float(exg.size)

            # HSV green-ish pixels and saturation
            hsv = small.convert("HSV")
            a = np.asarray(hsv, dtype=np.uint8)
            h, s, v = a[..., 0], a[..., 1], a[..., 2]
            green_mask = (h >= 70) & (h <= 160) & (s >= 50) & (v >= 40)
            green_ratio = float(np.count_nonzero(green_mask)) / float(a.shape[0] * a.shape[1])
            sat_mean = float(np.mean(s)) / 255.0

            # Rough skin-tone suppression in YCbCr to avoid portraits
            ycbcr = small.convert("YCbCr")
            yc = np.asarray(ycbcr, dtype=np.uint8)
            Cb, Cr = yc[..., 1], yc[..., 2]
            skin_mask = (Cr >= 135) & (Cr <= 180) & (Cb >= 85) & (Cb <= 135)
            skin_ratio = float(np.count_nonzero(skin_mask)) / float(yc.shape[0] * yc.shape[1])

            # Combine signals (permissive gate)
            leaf_score = 0.55 * green_ratio + 0.35 * exg_ratio + 0.10 * sat_mean
            is_leaf = not ((skin_ratio >= 0.20) or (green_ratio < 0.05 and exg_ratio < 0.10))

            result.update({
                "green_ratio": round(green_ratio, 4),
                "exg_ratio": round(exg_ratio, 4),
                "sat_mean": round(sat_mean, 4),
                "skin_ratio": round(skin_ratio, 4),
                "leaf_score": round(leaf_score, 4),
                "is_leaf": bool(is_leaf),
            })
        except Exception:
            pass
        return result

    def preprocess(self, image: Image.Image) -> np.ndarray:
        # Use the model's expected spatial input size when available
        target_h, target_w = 224, 224
        try:
            if self.model is not None and hasattr(self.model, "input_shape"):
                # input_shape like (None, H, W, C)
                shp = self.model.input_shape
                if isinstance(shp, tuple) and len(shp) >= 3 and shp[1] and shp[2]:
                    target_h, target_w = int(shp[1]), int(shp[2])
        except Exception:
            pass
        image = image.convert("RGB").resize((target_w, target_h))
        x = np.asarray(image, dtype=np.float32) / 255.0
        return np.expand_dims(x, 0)

    def predict(self, image: Image.Image) -> Dict:
        if self.model is None:
            return {"error": "Model not loaded"}
        x = self.preprocess(image)
        probs = self.model.predict(x, verbose=0)[0]
        top_idx = int(np.argmax(probs))
        top_conf = float(probs[top_idx])
        top3 = np.argsort(probs)[-3:][::-1]
        top3_list = [{"class": self.class_names[i] if i < len(self.class_names) else str(i),
                      "confidence": float(probs[i])} for i in top3]
        return {
            "predicted_class": self.class_names[top_idx] if top_idx < len(self.class_names) else str(top_idx),
            "confidence": top_conf,
            "top_3_predictions": top3_list
        }

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
classifier = PestClassifier()

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/predict", methods=["POST"]) 
def predict_route():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    image = Image.open(file.stream)
    leaf = classifier.analyze_leaf_likelihood(image)
    if not leaf.get("is_leaf", False):
        return jsonify({
            "error": "The uploaded image doesn't appear to be a plant leaf. Please upload a clear leaf photo on a plain background.",
            "hint": leaf
        }), 400
    pred = classifier.predict(image)
    if "error" in pred:
        return jsonify(pred), 500
    recs = get_pesticide_recommendations(pred["predicted_class"], pred["confidence"])
    guidelines = get_safety_guidelines()
    return jsonify({"prediction": pred, "pesticide_recommendations": recs, "safety_guidelines": guidelines})

@app.route("/predict_base64", methods=["POST"]) 
def predict_base64_route():
    data = request.get_json(silent=True) or {}
    b64 = data.get("image")
    if not b64:
        return jsonify({"error": "No base64 image provided"}), 400
    if b64.startswith("data:image"):
        b64 = b64.split(",", 1)[1]
    image = Image.open(io.BytesIO(base64.b64decode(b64)))
    leaf = classifier.analyze_leaf_likelihood(image)
    if not leaf.get("is_leaf", False):
        return jsonify({
            "error": "The uploaded image doesn't appear to be a plant leaf. Please upload a clear leaf photo on a plain background.",
            "hint": leaf
        }), 400
    pred = classifier.predict(image)
    if "error" in pred:
        return jsonify(pred), 500
    recs = get_pesticide_recommendations(pred["predicted_class"], pred["confidence"])
    guidelines = get_safety_guidelines()
    return jsonify({"prediction": pred, "pesticide_recommendations": recs, "safety_guidelines": guidelines})

@app.route("/recommendations/<disease_name>")
def recommendations_route(disease_name: str):
    try:
        confidence = float(request.args.get('confidence', 0.8))
        recs = get_pesticide_recommendations(disease_name, confidence)
        return jsonify({"disease": disease_name, "pesticide_recommendations": recs})
    except Exception as e:
        logging.exception("recommendations_route error")
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": classifier.model is not None,
        "num_classes": len(classifier.class_names)
    })

@app.route("/reload", methods=["POST"]) 
def reload_model():
    try:
        logger.info("Reloading model and class indices from disk...")
        classifier._load()
        return jsonify({
            "reloaded": True,
            "model_loaded": classifier.model is not None,
            "num_classes": len(classifier.class_names)
        })
    except Exception as e:
        logger.exception("Failed to reload model")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    os.makedirs("model", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
