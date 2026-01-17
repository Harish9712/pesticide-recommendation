"""
Pesticide Recommendation Database
Contains comprehensive information about pesticides for different plant diseases and pests
with sustainability and safety considerations.
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class SafetyLevel(Enum):
    """Pesticide safety levels"""
    VERY_SAFE = "Very Safe"
    SAFE = "Safe"
    MODERATE = "Moderate"
    CAUTION = "Caution"
    DANGEROUS = "Dangerous"

class EnvironmentalImpact(Enum):
    """Environmental impact levels"""
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"

@dataclass
class PesticideInfo:
    """Information about a specific pesticide"""
    name: str
    active_ingredient: str
    target_diseases: List[str]
    target_pests: List[str]
    application_method: str
    dosage: str
    frequency: str
    safety_level: SafetyLevel
    environmental_impact: EnvironmentalImpact
    organic_approved: bool
    pre_harvest_interval: str  # Days before harvest
    reentry_interval: str  # Hours before reentry
    toxicity_notes: str
    environmental_notes: str
    alternatives: List[str]
    cost_level: str  # Low, Medium, High
    effectiveness: str  # High, Medium, Low

# Comprehensive pesticide database
PESTICIDE_DATABASE = {
    # Fungal Diseases
    "Apple_scab": [
        PesticideInfo(
            name="Copper Fungicide",
            active_ingredient="Copper Hydroxide",
            target_diseases=["Apple_scab", "Black_rot", "Cedar_apple_rust"],
            target_pests=[],
            application_method="Foliar spray",
            dosage="2-4 lbs per 100 gallons",
            frequency="Every 7-14 days during growing season",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="4 hours",
            toxicity_notes="Low toxicity to humans and beneficial insects",
            environmental_notes="Minimal environmental impact, copper can accumulate in soil",
            alternatives=["Sulfur fungicide", "Bacillus subtilis"],
            cost_level="Medium",
            effectiveness="High"
        ),
        PesticideInfo(
            name="Sulfur Fungicide",
            active_ingredient="Elemental Sulfur",
            target_diseases=["Apple_scab", "Powdery_mildew"],
            target_pests=[],
            application_method="Foliar spray or dust",
            dosage="3-5 lbs per 100 gallons",
            frequency="Every 7-10 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="24 hours",
            toxicity_notes="Very low toxicity",
            environmental_notes="Minimal environmental impact",
            alternatives=["Copper fungicide", "Baking soda solution"],
            cost_level="Low",
            effectiveness="Medium"
        )
    ],
    
    "Black_rot": [
        PesticideInfo(
            name="Copper Fungicide",
            active_ingredient="Copper Hydroxide",
            target_diseases=["Black_rot", "Apple_scab"],
            target_pests=[],
            application_method="Foliar spray",
            dosage="2-4 lbs per 100 gallons",
            frequency="Every 7-14 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="4 hours",
            toxicity_notes="Low toxicity",
            environmental_notes="Minimal environmental impact",
            alternatives=["Sulfur fungicide", "Bacillus subtilis"],
            cost_level="Medium",
            effectiveness="High"
        )
    ],
    
    "Powdery_mildew": [
        PesticideInfo(
            name="Sulfur Fungicide",
            active_ingredient="Elemental Sulfur",
            target_diseases=["Powdery_mildew", "Apple_scab"],
            target_pests=[],
            application_method="Foliar spray",
            dosage="3-5 lbs per 100 gallons",
            frequency="Every 7-10 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="24 hours",
            toxicity_notes="Very low toxicity",
            environmental_notes="Minimal environmental impact",
            alternatives=["Baking soda solution", "Milk solution"],
            cost_level="Low",
            effectiveness="High"
        ),
        PesticideInfo(
            name="Baking Soda Solution",
            active_ingredient="Sodium Bicarbonate",
            target_diseases=["Powdery_mildew"],
            target_pests=[],
            application_method="Foliar spray",
            dosage="1 tablespoon per gallon + 1 drop dish soap",
            frequency="Every 7 days",
            safety_level=SafetyLevel.VERY_SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="0 hours",
            toxicity_notes="Completely safe for humans and environment",
            environmental_notes="No environmental impact",
            alternatives=["Milk solution", "Sulfur fungicide"],
            cost_level="Very Low",
            effectiveness="Medium"
        )
    ],
    
    # Bacterial Diseases
    "Bacterial_spot": [
        PesticideInfo(
            name="Copper Bactericide",
            active_ingredient="Copper Hydroxide",
            target_diseases=["Bacterial_spot"],
            target_pests=[],
            application_method="Foliar spray",
            dosage="1-2 lbs per 100 gallons",
            frequency="Every 7-10 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="4 hours",
            toxicity_notes="Low toxicity",
            environmental_notes="Minimal environmental impact",
            alternatives=["Bacillus subtilis", "Streptomycin"],
            cost_level="Medium",
            effectiveness="High"
        ),
        PesticideInfo(
            name="Bacillus subtilis",
            active_ingredient="Bacillus subtilis strain QST 713",
            target_diseases=["Bacterial_spot", "Fungal diseases"],
            target_pests=[],
            application_method="Foliar spray",
            dosage="2-4 oz per 100 gallons",
            frequency="Every 7-14 days",
            safety_level=SafetyLevel.VERY_SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="0 hours",
            toxicity_notes="Completely safe for humans and beneficial insects",
            environmental_notes="Beneficial bacteria, improves soil health",
            alternatives=["Copper bactericide", "Streptomycin"],
            cost_level="Medium",
            effectiveness="Medium"
        )
    ],
    
    # Viral Diseases
    "Tomato_Yellow_Leaf_Curl_Virus": [
        PesticideInfo(
            name="Insecticide for Whiteflies",
            active_ingredient="Neem Oil",
            target_diseases=[],
            target_pests=["Whiteflies", "Aphids"],
            application_method="Foliar spray",
            dosage="2-4 oz per gallon",
            frequency="Every 7-14 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="4 hours",
            toxicity_notes="Low toxicity, safe for beneficial insects",
            environmental_notes="Biodegradable, minimal environmental impact",
            alternatives=["Pyrethrin", "Insecticidal soap"],
            cost_level="Low",
            effectiveness="Medium"
        ),
        PesticideInfo(
            name="Insecticidal Soap",
            active_ingredient="Potassium Salts of Fatty Acids",
            target_diseases=[],
            target_pests=["Whiteflies", "Aphids", "Spider mites"],
            application_method="Foliar spray",
            dosage="2.5-5 oz per gallon",
            frequency="Every 7-10 days",
            safety_level=SafetyLevel.VERY_SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="0 hours",
            toxicity_notes="Very low toxicity",
            environmental_notes="Biodegradable, safe for environment",
            alternatives=["Neem oil", "Pyrethrin"],
            cost_level="Low",
            effectiveness="Medium"
        )
    ],
    
    # Banana Diseases
    "Banana_Black_Sigatoka_Disease": [
        PesticideInfo(
            name="Copper Fungicide",
            active_ingredient="Copper Hydroxide",
            target_diseases=["Black_Sigatoka", "Yellow_Sigatoka"],
            target_pests=[],
            application_method="Foliar spray",
            dosage="2-4 lbs per 100 gallons",
            frequency="Every 7-14 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="4 hours",
            toxicity_notes="Low toxicity",
            environmental_notes="Minimal environmental impact",
            alternatives=["Sulfur fungicide", "Bacillus subtilis"],
            cost_level="Medium",
            effectiveness="High"
        )
    ],
    
    "Banana_Panama_Disease": [
        PesticideInfo(
            name="Soil Treatment",
            active_ingredient="Bacillus subtilis",
            target_diseases=["Panama_Disease"],
            target_pests=[],
            application_method="Soil drench",
            dosage="1-2 oz per gallon, 1 gallon per plant",
            frequency="Every 30 days",
            safety_level=SafetyLevel.VERY_SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="0 hours",
            toxicity_notes="Completely safe",
            environmental_notes="Improves soil health",
            alternatives=["Crop rotation", "Resistant varieties"],
            cost_level="Medium",
            effectiveness="Medium"
        )
    ],
    
    # Insect Pests
    "Spider_mites": [
        PesticideInfo(
            name="Neem Oil",
            active_ingredient="Azadirachtin",
            target_diseases=[],
            target_pests=["Spider_mites", "Aphids", "Whiteflies"],
            application_method="Foliar spray",
            dosage="2-4 oz per gallon",
            frequency="Every 7-14 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="4 hours",
            toxicity_notes="Low toxicity, safe for beneficial insects",
            environmental_notes="Biodegradable",
            alternatives=["Insecticidal soap", "Horticultural oil"],
            cost_level="Low",
            effectiveness="High"
        ),
        PesticideInfo(
            name="Horticultural Oil",
            active_ingredient="Mineral Oil",
            target_diseases=[],
            target_pests=["Spider_mites", "Scale insects", "Aphids"],
            application_method="Foliar spray",
            dosage="2-4 oz per gallon",
            frequency="Every 7-14 days",
            safety_level=SafetyLevel.SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="0 days",
            reentry_interval="4 hours",
            toxicity_notes="Low toxicity",
            environmental_notes="Minimal environmental impact",
            alternatives=["Neem oil", "Insecticidal soap"],
            cost_level="Low",
            effectiveness="High"
        )
    ],
    
    # Healthy plants
    "Healthy": [
        PesticideInfo(
            name="Preventive Care",
            active_ingredient="None",
            target_diseases=[],
            target_pests=[],
            application_method="Cultural practices",
            dosage="N/A",
            frequency="Ongoing",
            safety_level=SafetyLevel.VERY_SAFE,
            environmental_impact=EnvironmentalImpact.LOW,
            organic_approved=True,
            pre_harvest_interval="N/A",
            reentry_interval="N/A",
            toxicity_notes="No toxicity",
            environmental_notes="No environmental impact",
            alternatives=["Continue monitoring", "Maintain plant health"],
            cost_level="Very Low",
            effectiveness="High"
        )
    ]
}

def get_pesticide_recommendations(disease_name: str, confidence: float = 0.8) -> List[Dict]:
    """
    Get pesticide recommendations for a specific disease
    
    Args:
        disease_name: Name of the disease/pest
        confidence: Confidence level of the prediction (0-1)
    
    Returns:
        List of pesticide recommendations with safety and sustainability info
    """
    
    # Normalize disease name and create mapping for actual class names
    disease_name_clean = disease_name.replace("_", " ").replace("___", " ").strip()
    
    # Create mapping from actual class names to database keys
    class_mapping = {
        # Apple diseases
        "Apple___Apple_scab": "Apple_scab",
        "Apple___Black_rot": "Black_rot", 
        "Apple___Cedar_apple_rust": "Apple_scab",  # Similar treatment
        "Apple___healthy": "Healthy",
        
        # Cherry diseases
        "Cherry_(including_sour)___Powdery_mildew": "Powdery_mildew",
        "Cherry_(including_sour)___healthy": "Healthy",
        
        # Corn diseases
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Powdery_mildew",  # Similar treatment
        "Corn_(maize)___Common_rust_": "Powdery_mildew",  # Similar treatment
        "Corn_(maize)___Northern_Leaf_Blight": "Powdery_mildew",  # Similar treatment
        "Corn_(maize)___healthy": "Healthy",
        
        # Grape diseases
        "Grape___Black_rot": "Black_rot",
        "Grape___Esca_(Black_Measles)": "Black_rot",  # Similar treatment
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Powdery_mildew",  # Similar treatment
        "Grape___healthy": "Healthy",
        
        # Orange diseases
        "Orange___Haunglongbing_(Citrus_greening)": "Bacterial_spot",  # Similar treatment
        
        # Peach diseases
        "Peach___Bacterial_spot": "Bacterial_spot",
        "Peach___healthy": "Healthy",
        
        # Pepper diseases
        "Pepper,_bell___Bacterial_spot": "Bacterial_spot",
        "Pepper,_bell___healthy": "Healthy",
        
        # Potato diseases
        "Potato___Early_blight": "Powdery_mildew",  # Similar treatment
        "Potato___Late_blight": "Powdery_mildew",  # Similar treatment
        "Potato___healthy": "Healthy",
        
        # Other healthy plants
        "Blueberry___healthy": "Healthy",
        "Raspberry___healthy": "Healthy",
        "Soybean___healthy": "Healthy",
        "Strawberry___healthy": "Healthy",
        "Tomato___healthy": "Healthy",
        
        # Squash diseases
        "Squash___Powdery_mildew": "Powdery_mildew",
        
        # Strawberry diseases
        "Strawberry___Leaf_scorch": "Powdery_mildew",  # Similar treatment
        
        # Tomato diseases
        "Tomato___Bacterial_spot": "Bacterial_spot",
        "Tomato___Early_blight": "Powdery_mildew",  # Similar treatment
        "Tomato___Late_blight": "Powdery_mildew",  # Similar treatment
        "Tomato___Leaf_Mold": "Powdery_mildew",  # Similar treatment
        "Tomato___Septoria_leaf_spot": "Powdery_mildew",  # Similar treatment
        "Tomato___Spider_mites Two-spotted_spider_mite": "Spider_mites",
        "Tomato___Target_Spot": "Powdery_mildew",  # Similar treatment
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus": "Tomato_Yellow_Leaf_Curl_Virus",  # Similar treatment
        
        # Banana diseases
        "Augmented Banana Black Sigatoka Disease": "Banana_Black_Sigatoka_Disease",
        "Augmented Banana Bract Mosaic Virus Disease": "Banana_Black_Sigatoka_Disease",  # Similar treatment
        "Augmented Banana Healthy Leaf": "Healthy",
        "Augmented Banana Insect Pest Disease": "Spider_mites",  # Similar treatment
        "Augmented Banana Moko Disease": "Banana_Panama_Disease",  # Similar treatment
        "Augmented Banana Panama Disease": "Banana_Panama_Disease",
        "Augmented Banana Yellow Sigatoka Disease": "Banana_Black_Sigatoka_Disease"  # Similar treatment
    }
    
    # Get the mapped key for the disease
    mapped_key = class_mapping.get(disease_name, disease_name_clean)
    
    # Find matching pesticides
    recommendations = []
    
    for key, pesticides in PESTICIDE_DATABASE.items():
        if mapped_key.lower() in key.lower() or key.lower() in mapped_key.lower():
            for pesticide in pesticides:
                # Adjust recommendation based on confidence
                if confidence >= 0.8:
                    effectiveness = pesticide.effectiveness
                elif confidence >= 0.6:
                    effectiveness = "Medium" if pesticide.effectiveness == "High" else "Low"
                else:
                    effectiveness = "Low"
                
                recommendations.append({
                    "name": pesticide.name,
                    "active_ingredient": pesticide.active_ingredient,
                    "target_diseases": pesticide.target_diseases,
                    "target_pests": pesticide.target_pests,
                    "application_method": pesticide.application_method,
                    "dosage": pesticide.dosage,
                    "frequency": pesticide.frequency,
                    "safety_level": pesticide.safety_level.value,
                    "environmental_impact": pesticide.environmental_impact.value,
                    "organic_approved": pesticide.organic_approved,
                    "pre_harvest_interval": pesticide.pre_harvest_interval,
                    "reentry_interval": pesticide.reentry_interval,
                    "toxicity_notes": pesticide.toxicity_notes,
                    "environmental_notes": pesticide.environmental_notes,
                    "alternatives": pesticide.alternatives,
                    "cost_level": pesticide.cost_level,
                    "effectiveness": effectiveness,
                    "confidence_adjusted": True if confidence < 0.8 else False
                })
    
    # If no specific recommendations found, suggest general organic options
    if not recommendations:
        recommendations = [
            {
                "name": "General Organic Treatment",
                "active_ingredient": "Multiple",
                "target_diseases": ["General"],
                "target_pests": ["General"],
                "application_method": "Foliar spray",
                "dosage": "As per product label",
                "frequency": "Every 7-14 days",
                "safety_level": "Safe",
                "environmental_impact": "Low",
                "organic_approved": True,
                "pre_harvest_interval": "0 days",
                "reentry_interval": "4 hours",
                "toxicity_notes": "Low toxicity",
                "environmental_notes": "Minimal environmental impact",
                "alternatives": ["Neem oil", "Copper fungicide", "Bacillus subtilis"],
                "cost_level": "Medium",
                "effectiveness": "Medium",
                "confidence_adjusted": True
            }
        ]
    
    return recommendations

def get_safety_guidelines() -> Dict:
    """Get general safety guidelines for pesticide use"""
    
    return {
        "general_safety": [
            "Always read and follow pesticide label instructions",
            "Wear appropriate protective equipment (gloves, mask, goggles)",
            "Apply pesticides during calm weather conditions",
            "Keep children and pets away from treated areas",
            "Store pesticides in original containers, away from food",
            "Dispose of empty containers properly"
        ],
        "environmental_protection": [
            "Avoid applying near water sources",
            "Don't apply during heavy rain or wind",
            "Use integrated pest management (IPM) practices",
            "Rotate different types of pesticides to prevent resistance",
            "Consider beneficial insects and pollinators",
            "Use organic options when possible"
        ],
        "sustainable_practices": [
            "Implement crop rotation",
            "Use resistant plant varieties",
            "Maintain proper plant spacing and air circulation",
            "Remove diseased plant material promptly",
            "Improve soil health with organic matter",
            "Monitor plants regularly for early detection"
        ]
    }

def save_database_to_json(filename: str = "pesticide_database.json"):
    """Save the pesticide database to a JSON file"""
    
    # Convert dataclass objects to dictionaries
    db_dict = {}
    for disease, pesticides in PESTICIDE_DATABASE.items():
        db_dict[disease] = []
        for pesticide in pesticides:
            db_dict[disease].append({
                "name": pesticide.name,
                "active_ingredient": pesticide.active_ingredient,
                "target_diseases": pesticide.target_diseases,
                "target_pests": pesticide.target_pests,
                "application_method": pesticide.application_method,
                "dosage": pesticide.dosage,
                "frequency": pesticide.frequency,
                "safety_level": pesticide.safety_level.value,
                "environmental_impact": pesticide.environmental_impact.value,
                "organic_approved": pesticide.organic_approved,
                "pre_harvest_interval": pesticide.pre_harvest_interval,
                "reentry_interval": pesticide.reentry_interval,
                "toxicity_notes": pesticide.toxicity_notes,
                "environmental_notes": pesticide.environmental_notes,
                "alternatives": pesticide.alternatives,
                "cost_level": pesticide.cost_level,
                "effectiveness": pesticide.effectiveness
            })
    
    with open(filename, 'w') as f:
        json.dump(db_dict, f, indent=2)
    
    print(f"Pesticide database saved to {filename}")

if __name__ == "__main__":
    # Save database to JSON file
    save_database_to_json()
    
    # Test the recommendation system
    print("Testing pesticide recommendation system...")
    
    test_diseases = [
        "Apple_scab",
        "Powdery_mildew", 
        "Bacterial_spot",
        "Spider_mites",
        "Banana_Black_Sigatoka_Disease",
        "Healthy"
    ]
    
    for disease in test_diseases:
        print(f"\nRecommendations for {disease}:")
        recommendations = get_pesticide_recommendations(disease, 0.9)
        for i, rec in enumerate(recommendations[:2], 1):  # Show top 2 recommendations
            print(f"{i}. {rec['name']} - {rec['effectiveness']} effectiveness")
            print(f"   Safety: {rec['safety_level']}, Environmental Impact: {rec['environmental_impact']}")
            print(f"   Organic Approved: {rec['organic_approved']}")
    
    print("\n✅ Pesticide database created successfully!")
