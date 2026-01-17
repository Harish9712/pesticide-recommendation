"""
Configuration file for AI-Powered Crop Pest Classification System
Contains all system settings and parameters
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "model"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = BASE_DIR / "uploads"

# Dataset paths
PLANTVILLAGE_DIR = DATASET_DIR / "plantvillage dataset" / "color"
BANANA_DIR = DATASET_DIR / "Banana_Disease_Recognition_Dataset" / "Original Images" / "Original Images"

# Model configuration
MODEL_CONFIG = {
    "image_size": (224, 224),
    "batch_size": 32,
    "epochs": 50,
    "learning_rate": 0.001,
    "dropout_rate": 0.3,
    "validation_split": 0.2,
    "patience": 10,
    "min_lr": 1e-7
}

# Data augmentation parameters
AUGMENTATION_CONFIG = {
    "rotation_range": 20,
    "width_shift_range": 0.2,
    "height_shift_range": 0.2,
    "horizontal_flip": True,
    "zoom_range": 0.2,
    "brightness_range": [0.8, 1.2],
    "shear_range": 0.2,
    "fill_mode": "nearest"
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True,
    "max_content_length": 16 * 1024 * 1024,  # 16MB
    "allowed_extensions": {"png", "jpg", "jpeg", "gif", "bmp", "tiff"}
}

# Model file paths
MODEL_PATHS = {
    "final_model": MODEL_DIR / "final_pest_classifier.h5",
    "best_model": MODEL_DIR / "best_pest_classifier.h5",
    "class_indices": MODEL_DIR / "class_indices.json",
    "training_history": MODEL_DIR / "training_history.json",
    "confusion_matrix": MODEL_DIR / "confusion_matrix.png",
    "training_plot": MODEL_DIR / "training_history.png"
}

# Pesticide database configuration
PESTICIDE_CONFIG = {
    "database_file": "pesticide_database.json",
    "safety_guidelines_file": "safety_guidelines.json",
    "sustainability_database_file": "sustainability_database.json"
}

# Sustainability configuration
SUSTAINABILITY_CONFIG = {
    "min_confidence_for_recommendations": 0.6,
    "organic_priority": True,
    "environmental_impact_weight": 0.3,
    "cost_effectiveness_weight": 0.2,
    "safety_weight": 0.3,
    "effectiveness_weight": 0.2
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/system.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# Web interface configuration
WEB_CONFIG = {
    "title": "AI-Powered Crop Pest Classification System",
    "description": "Identify plant diseases and get sustainable pesticide recommendations",
    "version": "1.0.0",
    "author": "AI Agriculture Team",
    "contact_email": "support@crop-pest-ai.com"
}

# Feature flags
FEATURES = {
    "enable_training": True,
    "enable_prediction": True,
    "enable_recommendations": True,
    "enable_sustainability": True,
    "enable_api": True,
    "enable_web_interface": True,
    "enable_logging": True,
    "enable_caching": False
}

# Performance settings
PERFORMANCE_CONFIG = {
    "use_gpu": True,
    "gpu_memory_growth": True,
    "mixed_precision": False,
    "cache_predictions": False,
    "max_cache_size": 1000
}

# Security settings
SECURITY_CONFIG = {
    "max_file_size": 16 * 1024 * 1024,  # 16MB
    "allowed_file_types": ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff"],
    "rate_limiting": {
        "enabled": False,
        "requests_per_minute": 60
    },
    "cors": {
        "enabled": True,
        "origins": ["*"]
    }
}

# Notification settings
NOTIFICATION_CONFIG = {
    "email_notifications": False,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email_username": "",
    "email_password": "",
    "admin_email": "admin@crop-pest-ai.com"
}

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        MODEL_DIR,
        TEMPLATES_DIR,
        STATIC_DIR,
        UPLOADS_DIR,
        BASE_DIR / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_config():
    """Get complete configuration dictionary"""
    return {
        "base_dir": BASE_DIR,
        "dataset_dir": DATASET_DIR,
        "model_dir": MODEL_DIR,
        "templates_dir": TEMPLATES_DIR,
        "static_dir": STATIC_DIR,
        "uploads_dir": UPLOADS_DIR,
        "plantvillage_dir": PLANTVILLAGE_DIR,
        "banana_dir": BANANA_DIR,
        "model_config": MODEL_CONFIG,
        "augmentation_config": AUGMENTATION_CONFIG,
        "api_config": API_CONFIG,
        "model_paths": MODEL_PATHS,
        "pesticide_config": PESTICIDE_CONFIG,
        "sustainability_config": SUSTAINABILITY_CONFIG,
        "logging_config": LOGGING_CONFIG,
        "web_config": WEB_CONFIG,
        "features": FEATURES,
        "performance_config": PERFORMANCE_CONFIG,
        "security_config": SECURITY_CONFIG,
        "notification_config": NOTIFICATION_CONFIG
    }

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check required directories
    if not PLANTVILLAGE_DIR.exists():
        errors.append(f"PlantVillage dataset directory not found: {PLANTVILLAGE_DIR}")
    
    if not BANANA_DIR.exists():
        errors.append(f"Banana dataset directory not found: {BANANA_DIR}")
    
    # Check model configuration
    if MODEL_CONFIG["image_size"][0] != MODEL_CONFIG["image_size"][1]:
        errors.append("Image size must be square (width == height)")
    
    if MODEL_CONFIG["batch_size"] <= 0:
        errors.append("Batch size must be positive")
    
    if MODEL_CONFIG["epochs"] <= 0:
        errors.append("Epochs must be positive")
    
    # Check API configuration
    if API_CONFIG["port"] < 1024 or API_CONFIG["port"] > 65535:
        errors.append("Port must be between 1024 and 65535")
    
    if API_CONFIG["max_content_length"] <= 0:
        errors.append("Max content length must be positive")
    
    return errors

if __name__ == "__main__":
    # Create directories
    create_directories()
    
    # Validate configuration
    errors = validate_config()
    
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Configuration validation passed")
    
    # Print configuration summary
    config = get_config()
    print(f"\n📊 Configuration Summary:")
    print(f"   - Model: {config['model_config']['image_size']} images, {config['model_config']['batch_size']} batch size")
    print(f"   - API: http://{config['api_config']['host']}:{config['api_config']['port']}")
    print(f"   - Features: {sum(config['features'].values())}/{len(config['features'])} enabled")
    print(f"   - Datasets: PlantVillage + Banana Disease")
