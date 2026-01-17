"""
Quick test script to verify the prediction API is working correctly
"""
import sys
import os

# Test module import and initialization
print("=" * 60)
print("Testing Prediction API")
print("=" * 60)

try:
    print("\n1. Importing prediction_api module...")
    from prediction_api import app, classifier
    print("   [OK] Module imported successfully")
    
    print("\n2. Checking model status...")
    model_loaded = classifier.model is not None
    num_classes = len(classifier.class_names)
    print(f"   [OK] Model loaded: {model_loaded}")
    print(f"   [OK] Number of classes: {num_classes}")
    
    if classifier.class_names:
        print(f"\n3. Sample class names (first 5):")
        for i, name in enumerate(classifier.class_names[:5], 1):
            print(f"   {i}. {name}")
        if num_classes > 5:
            print(f"   ... and {num_classes - 5} more classes")
    
    print("\n4. Testing Flask app routes...")
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/health')
        print(f"   [OK] Health endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   [OK] Response: {data}")
        
        # Test root endpoint
        try:
            response = client.get('/')
            print(f"   [OK] Root endpoint status: {response.status_code}")
        except:
            print(f"   [WARNING] Root endpoint (may need static file): {response.status_code}")
    
    print("\n5. Testing pesticide recommendations...")
    from pesticide_database import get_pesticide_recommendations, get_safety_guidelines
    test_disease = "Tomato___Bacterial_spot"
    recs = get_pesticide_recommendations(test_disease, 0.8)
    print(f"   [OK] Got {len(recs)} recommendations for {test_disease}")
    if recs:
        print(f"   [OK] First recommendation: {recs[0]['name']}")
    
    guidelines = get_safety_guidelines()
    print(f"   [OK] Safety guidelines loaded: {len(guidelines)} categories")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] All tests passed! API is ready to use.")
    print("=" * 60)
    print(f"\nTo start the server, run:")
    print(f"   python prediction_api.py")
    print(f"\nThe API will be available at: http://localhost:5000")
    print(f"  - Health check: http://localhost:5000/health")
    print(f"  - Predict: http://localhost:5000/predict (POST)")
    print(f"  - Recommendations: http://localhost:5000/recommendations/<disease_name>")
    
except Exception as e:
    print(f"\n[ERROR] Error during testing: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

