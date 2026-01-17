import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import mixed_precision 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.metrics import Metric
from sklearn.utils import class_weight
import shutil
from pathlib import Path

# Custom Top-3 Accuracy Metric
class Top3Accuracy(Metric):
    def __init__(self, name='top_3_accuracy', **kwargs):
        super(Top3Accuracy, self).__init__(name=name, **kwargs)
        self.correct = self.add_weight(name='correct', initializer='zeros')
        self.total = self.add_weight(name='total', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        # Get top-3 predictions
        top3_pred = tf.nn.top_k(y_pred, k=3).indices
        # Get true labels
        true_labels = tf.argmax(y_true, axis=1)
        # Ensure both have the same data type
        true_labels = tf.cast(true_labels, tf.int32)
        top3_pred = tf.cast(top3_pred, tf.int32)
        # Check if true label is in top-3 predictions
        correct = tf.reduce_any(tf.equal(tf.expand_dims(true_labels, 1), top3_pred), axis=1)
        correct = tf.cast(correct, tf.float32)
        
        if sample_weight is not None:
            sample_weight = tf.cast(sample_weight, tf.float32)
            correct = correct * sample_weight
        
        self.correct.assign_add(tf.reduce_sum(correct))
        self.total.assign_add(tf.cast(tf.shape(y_true)[0], tf.float32))

    def result(self):
        return self.correct / self.total

    def reset_state(self):
        self.correct.assign(0)
        self.total.assign(0)

# Enable mixed precision if supported
try:
	mixed_precision.set_global_policy('mixed_float16')
except Exception:
	pass

# Dataset paths
PLANT_COLOR_DIR = 'dataset/plantvillage dataset/color'
PLANT_GRAY_DIR = 'dataset/plantvillage dataset/grayscale'
BANANA_ORIG_DIR = 'dataset/Banana_Disease_Recognition_Dataset/Original Images/Original Images'
BANANA_AUG_DIR = 'dataset/Banana_Disease_Recognition_Dataset/Augmented images/Augmented images'

# Combined dataset directory
COMBINED_DIR = 'dataset/combined_dataset'
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30  # Increased epochs for better training
VAL_SPLIT = 0.2

MODEL_DIR = 'model'
BEST_PATH = os.path.join(MODEL_DIR, 'best_model.keras')
FINAL_PATH = os.path.join(MODEL_DIR, 'final_model.keras')
CLASS_MAP_PATH = os.path.join(MODEL_DIR, 'class_indices.json')

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(COMBINED_DIR, exist_ok=True)

# Control whether to rebuild the combined dataset on each run
# Set to True to force rebuilding, or leave False to reuse if present
REBUILD_COMBINED = False

def create_combined_dataset():
	"""Create a combined dataset from all available image sources"""
	print("Creating combined dataset from all available sources...")
	
	# Get all class names from PlantVillage color dataset (our reference)
	plant_classes = sorted([d for d in os.listdir(PLANT_COLOR_DIR) 
						   if os.path.isdir(os.path.join(PLANT_COLOR_DIR, d))])
	
	# Get banana classes and map them to consistent names
	banana_orig_classes = sorted([d for d in os.listdir(BANANA_ORIG_DIR) 
								 if os.path.isdir(os.path.join(BANANA_ORIG_DIR, d))])
	banana_aug_classes = sorted([d for d in os.listdir(BANANA_AUG_DIR) 
								if os.path.isdir(os.path.join(BANANA_AUG_DIR, d))])
	
	# Create mapping for banana classes to match our naming convention
	banana_mapping = {
		'Banana Black Sigatoka Disease': 'Augmented Banana Black Sigatoka Disease',
		'Banana Bract Mosaic Virus Disease': 'Augmented Banana Bract Mosaic Virus Disease', 
		'Banana Healthy Leaf': 'Augmented Banana Healthy Leaf',
		'Banana Insect Pest Disease': 'Augmented Banana Insect Pest Disease',
		'Banana Moko Disease': 'Augmented Banana Moko Disease',
		'Banana Panama Disease': 'Augmented Banana Panama Disease',
		'Banana Yellow Sigatoka Disease': 'Augmented Banana Yellow Sigatoka Disease'
	}
	
	# Combine all classes
	all_classes = plant_classes + list(banana_mapping.values())
	
	# Create class directories in combined dataset
	for class_name in all_classes:
		class_dir = os.path.join(COMBINED_DIR, class_name)
		os.makedirs(class_dir, exist_ok=True)
	
	# Copy PlantVillage color images
	print("Copying PlantVillage color images...")
	for class_name in plant_classes:
		src_dir = os.path.join(PLANT_COLOR_DIR, class_name)
		dst_dir = os.path.join(COMBINED_DIR, class_name)
		
		for img_file in os.listdir(src_dir):
			if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
				src_path = os.path.join(src_dir, img_file)
				dst_path = os.path.join(dst_dir, f"color_{img_file}")
				if not os.path.exists(dst_path):
					shutil.copy2(src_path, dst_path)
	
	# Copy PlantVillage grayscale images
	print("Copying PlantVillage grayscale images...")
	for class_name in plant_classes:
		src_dir = os.path.join(PLANT_GRAY_DIR, class_name)
		dst_dir = os.path.join(COMBINED_DIR, class_name)
		
		if os.path.exists(src_dir):
			for img_file in os.listdir(src_dir):
				if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
					src_path = os.path.join(src_dir, img_file)
					dst_path = os.path.join(dst_dir, f"gray_{img_file}")
					if not os.path.exists(dst_path):
						shutil.copy2(src_path, dst_path)
	
	# Copy Banana original images
	print("Copying Banana original images...")
	for orig_class, mapped_class in banana_mapping.items():
		src_dir = os.path.join(BANANA_ORIG_DIR, orig_class)
		dst_dir = os.path.join(COMBINED_DIR, mapped_class)
		
		if os.path.exists(src_dir):
			for img_file in os.listdir(src_dir):
				if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
					src_path = os.path.join(src_dir, img_file)
					dst_path = os.path.join(dst_dir, f"orig_{img_file}")
					if not os.path.exists(dst_path):
						shutil.copy2(src_path, dst_path)
	
	# Copy Banana augmented images
	print("Copying Banana augmented images...")
	for orig_class, mapped_class in banana_mapping.items():
		src_dir = os.path.join(BANANA_AUG_DIR, mapped_class)
		dst_dir = os.path.join(COMBINED_DIR, mapped_class)
		
		if os.path.exists(src_dir):
			for img_file in os.listdir(src_dir):
				if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
					src_path = os.path.join(src_dir, img_file)
					dst_path = os.path.join(dst_dir, f"aug_{img_file}")
					if not os.path.exists(dst_path):
						shutil.copy2(src_path, dst_path)
	
	# Print dataset statistics
	print("\nDataset Statistics:")
	total_images = 0
	for class_name in all_classes:
		class_dir = os.path.join(COMBINED_DIR, class_name)
		image_count = len([f for f in os.listdir(class_dir) 
						  if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
		total_images += image_count
		print(f"  {class_name}: {image_count} images")
	
	print(f"\nTotal images: {total_images}")
	print(f"Total classes: {len(all_classes)}")
	
	return all_classes

# Create or reuse combined dataset
def get_existing_combined_classes(base_dir: str):
	if not os.path.exists(base_dir):
		return []
	classes = []
	for name in sorted(os.listdir(base_dir)):
		class_dir = os.path.join(base_dir, name)
		if os.path.isdir(class_dir):
			# consider it valid if it contains at least one image file
			if any(f.lower().endswith((".jpg", ".jpeg", ".png")) for f in os.listdir(class_dir)):
				classes.append(name)
	return classes

existing_classes = get_existing_combined_classes(COMBINED_DIR)
if REBUILD_COMBINED or not existing_classes:
	all_classes = create_combined_dataset()
else:
	print("Reusing existing combined dataset. Set REBUILD_COMBINED=True to force rebuild.")
	print(f"Found {len(existing_classes)} classes in existing combined dataset.")
	all_classes = existing_classes

# Data generators with enhanced augmentation for better generalization
train_datagen = ImageDataGenerator(
	rescale=1./255,
	rotation_range=30,  # Increased rotation for better generalization
	width_shift_range=0.15,  # Increased shift range
	height_shift_range=0.15,
	horizontal_flip=True,
	vertical_flip=True,  # Added vertical flip
	zoom_range=0.25,  # Increased zoom range
	brightness_range=[0.7, 1.3],  # Increased brightness range
	shear_range=0.2,  # Added shear transformation
	channel_shift_range=0.1,  # Added channel shift
	validation_split=VAL_SPLIT
)

val_datagen = ImageDataGenerator(rescale=1./255, validation_split=VAL_SPLIT)

# Load combined dataset
print("Loading combined dataset...")
train_gen = train_datagen.flow_from_directory(
	COMBINED_DIR, 
	target_size=IMG_SIZE, 
	batch_size=BATCH_SIZE,
	class_mode='categorical', 
	subset='training', 
	shuffle=True, 
	color_mode='rgb'
)

val_gen = val_datagen.flow_from_directory(
	COMBINED_DIR, 
	target_size=IMG_SIZE, 
	batch_size=BATCH_SIZE,
	class_mode='categorical', 
	subset='validation', 
	shuffle=False, 
	color_mode='rgb'
)

# Create class indices from the combined dataset
class_indices = train_gen.class_indices
print(f"Loaded {len(class_indices)} classes from combined dataset")

# Calculate steps
steps_per_epoch = train_gen.samples // BATCH_SIZE
validation_steps = val_gen.samples // BATCH_SIZE

print(f"Training samples: {train_gen.samples}")
print(f"Validation samples: {val_gen.samples}")
print(f"Steps per epoch: {steps_per_epoch}")
print(f"Validation steps: {validation_steps}")

# Model - Enhanced architecture for better generalization
print("Building model...")
base = MobileNetV2(include_top=False, weights='imagenet', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
base.trainable = False

# Enhanced head with more layers for better feature learning
x = base.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dropout(0.4)(x)  # Increased dropout for better regularization

# Additional dense layers
x = Dense(512, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)

x = Dense(256, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.2)(x)

head = Dense(len(class_indices), activation='softmax', dtype='float32')(x)
model = Model(base.input, head)

# Compile with better optimizer settings
opt = tf.keras.optimizers.Adam(learning_rate=1e-3, beta_1=0.9, beta_2=0.999)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy', Top3Accuracy()])

# Enhanced callbacks
callbacks = [
	EarlyStopping(monitor='val_accuracy', patience=8, restore_best_weights=True, verbose=1),
	ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7, verbose=1),
	ModelCheckpoint(BEST_PATH, monitor='val_accuracy', save_best_only=True, verbose=1)
]

# Compute class weights for balanced training
print("Computing class weights...")
all_y = train_gen.classes
cw = class_weight.compute_class_weight('balanced', classes=np.unique(all_y), y=all_y)
class_weights = {i: w for i, w in enumerate(cw)}

print(f"Class weights computed for {len(class_weights)} classes")

# Phase 1: Train the head
print('Phase 1: Training head...')
hist1 = model.fit(
	train_gen,
	validation_data=val_gen,
	steps_per_epoch=steps_per_epoch,
	validation_steps=validation_steps,
	epochs=EPOCHS // 2,  # Half epochs for head training
	callbacks=callbacks,
	class_weight=class_weights,
	verbose=1
)

# Phase 2: Fine-tune the entire model
print('Phase 2: Fine-tuning entire model...')
base.trainable = True
# Unfreeze more layers for better feature learning
for layer in base.layers[:-50]:  # Keep only the last 50 layers trainable initially
	layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4, beta_1=0.9, beta_2=0.999), 
			  loss='categorical_crossentropy', metrics=['accuracy', Top3Accuracy()])

hist2 = model.fit(
	train_gen,
	validation_data=val_gen,
	steps_per_epoch=steps_per_epoch,
	validation_steps=validation_steps,
	epochs=EPOCHS // 2,  # Remaining epochs for fine-tuning
	callbacks=callbacks,
	class_weight=class_weights,
	verbose=1
)

# Phase 3: Final fine-tuning with very low learning rate
print('Phase 3: Final fine-tuning...')
for layer in base.layers:
	layer.trainable = True

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5, beta_1=0.9, beta_2=0.999), 
			  loss='categorical_crossentropy', metrics=['accuracy', Top3Accuracy()])

hist3 = model.fit(
	train_gen,
	validation_data=val_gen,
	steps_per_epoch=steps_per_epoch,
	validation_steps=validation_steps,
	epochs=5,  # Final few epochs
	callbacks=callbacks,
	class_weight=class_weights,
	verbose=1
)

# Save final model and class indices
print("Saving final model...")
model.save(FINAL_PATH)
with open(CLASS_MAP_PATH, 'w') as f:
	json.dump(class_indices, f, indent=2)

# Print training summary
print("\n" + "="*60)
print("TRAINING COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"Final model saved to: {FINAL_PATH}")
print(f"Best model saved to: {BEST_PATH}")
print(f"Class indices saved to: {CLASS_MAP_PATH}")
print(f"Total classes: {len(class_indices)}")
print(f"Total training samples: {train_gen.samples}")
print(f"Total validation samples: {val_gen.samples}")

# Print class list for reference
print("\nClasses in the model:")
for i, (class_name, class_idx) in enumerate(sorted(class_indices.items(), key=lambda x: x[1])):
	print(f"{class_idx:2d}: {class_name}")

print("\nModel is ready for deployment!")
print("="*60)
