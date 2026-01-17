import React from 'react';

const ResultsSection = ({ results }) => {
  const { prediction, pesticide_recommendations = [], safety_guidelines = {} } = results;

  const formatDiseaseName = (className) => {
    let formatted = className;
    
    // Replace underscores with spaces
    formatted = formatted.replace(/_/g, ' ');
    
    // Handle specific patterns
    formatted = formatted.replace(/___/g, ' - ');
    formatted = formatted.replace(/\s+/g, ' '); // Remove extra spaces
    
    // Capitalize words properly
    formatted = formatted.replace(/\b\w/g, l => l.toUpperCase());
    
    // Handle specific cases
    formatted = formatted.replace(/Augmented\s+/g, ''); // Remove "Augmented" prefix
    formatted = formatted.replace(/Banana\s+/g, 'Banana '); // Fix Banana spacing
    formatted = formatted.replace(/Apple\s+/g, 'Apple '); // Fix Apple spacing
    formatted = formatted.replace(/Tomato\s+/g, 'Tomato '); // Fix Tomato spacing
    formatted = formatted.replace(/Corn\s*\(maize\)/g, 'Corn (Maize)'); // Fix Corn formatting
    formatted = formatted.replace(/Cherry\s*\(including\s*sour\)/g, 'Cherry (Including Sour)'); // Fix Cherry formatting
    formatted = formatted.replace(/Pepper,\s*bell/g, 'Pepper, Bell'); // Fix Pepper formatting
    
    // Handle specific disease names
    formatted = formatted.replace(/Black\s*Sigatoka/g, 'Black Sigatoka');
    formatted = formatted.replace(/Yellow\s*Sigatoka/g, 'Yellow Sigatoka');
    formatted = formatted.replace(/Bract\s*Mosaic\s*Virus/g, 'Bract Mosaic Virus');
    formatted = formatted.replace(/Insect\s*Pest/g, 'Insect Pest');
    formatted = formatted.replace(/Leaf\s*Blight/g, 'Leaf Blight');
    formatted = formatted.replace(/Early\s*Blight/g, 'Early Blight');
    formatted = formatted.replace(/Late\s*Blight/g, 'Late Blight');
    formatted = formatted.replace(/Powdery\s*Mildew/g, 'Powdery Mildew');
    formatted = formatted.replace(/Bacterial\s*Spot/g, 'Bacterial Spot');
    formatted = formatted.replace(/Spider\s*Mites/g, 'Spider Mites');
    formatted = formatted.replace(/Target\s*Spot/g, 'Target Spot');
    formatted = formatted.replace(/Leaf\s*Mold/g, 'Leaf Mold');
    formatted = formatted.replace(/Septoria\s*Leaf\s*Spot/g, 'Septoria Leaf Spot');
    formatted = formatted.replace(/Two-Spotted\s*Spider\s*Mite/g, 'Two-Spotted Spider Mite');
    formatted = formatted.replace(/Yellow\s*Leaf\s*Curl\s*Virus/g, 'Yellow Leaf Curl Virus');
    formatted = formatted.replace(/Mosaic\s*Virus/g, 'Mosaic Virus');
    formatted = formatted.replace(/Leaf\s*Scorch/g, 'Leaf Scorch');
    formatted = formatted.replace(/Common\s*Rust/g, 'Common Rust');
    formatted = formatted.replace(/Northern\s*Leaf\s*Blight/g, 'Northern Leaf Blight');
    formatted = formatted.replace(/Cedar\s*Apple\s*Rust/g, 'Cedar Apple Rust');
    formatted = formatted.replace(/Black\s*Rot/g, 'Black Rot');
    formatted = formatted.replace(/Esca\s*\(Black\s*Measles\)/g, 'Esca (Black Measles)');
    formatted = formatted.replace(/Isariopsis\s*Leaf\s*Spot/g, 'Isariopsis Leaf Spot');
    formatted = formatted.replace(/Haunglongbing\s*\(Citrus\s*Greening\)/g, 'Huanglongbing (Citrus Greening)');
    formatted = formatted.replace(/Cercospora\s*Leaf\s*Spot\s*Gray\s*Leaf\s*Spot/g, 'Cercospora Leaf Spot / Gray Leaf Spot');
    
    return formatted;
  };

  // Determine disease status and styling
  const isHealthy = prediction.predicted_class.toLowerCase().includes('healthy');
  const confidence = prediction.confidence;
  const confidenceClass = confidence >= 0.8 ? 'confidence-high' : confidence >= 0.6 ? 'confidence-medium' : 'confidence-low';
  const diseaseClass = isHealthy ? 'disease-healthy' : confidence >= 0.8 ? 'disease-infected' : 'disease-moderate';
  
  // Format disease name for better display
  const diseaseName = formatDiseaseName(prediction.predicted_class);

  return (
    <div className="card result-card p-4">
      <div className="row">
        <div className="col-md-6">
          <h4 className="mb-3">
            <i className="fas fa-microscope me-2"></i>Disease Analysis
          </h4>
          <div className="mb-3">
            <span className={`disease-badge ${diseaseClass}`}>
              {diseaseName}
            </span>
          </div>
          <div className="mb-3">
            <label className="form-label">
              <strong>Confidence Level:</strong>
            </label>
            <div className="confidence-bar">
              <div 
                className={`confidence-fill ${confidenceClass}`} 
                style={{ width: `${confidence * 100}%` }}
              ></div>
            </div>
            <small className="text-muted">
              {(confidence * 100).toFixed(1)}% confidence
            </small>
          </div>
          {prediction.top_3_predictions && (
            <div className="mb-3">
              <label className="form-label">
                <strong>Top Predictions:</strong>
              </label>
              <div className="list-group">
                {prediction.top_3_predictions.map((p, i) => (
                  <div key={i} className="list-group-item d-flex justify-content-between align-items-center">
                    <span>{formatDiseaseName(p.class)}</span>
                    <span className="badge bg-secondary">
                      {(p.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        <div className="col-md-6">
          <h4 className="mb-3">
            <i className="fas fa-shield-alt me-2"></i>Treatment Recommendations
          </h4>
          {pesticide_recommendations.length > 0 ? (
            pesticide_recommendations.slice(0, 3).map((rec, index) => (
              <div key={index} className="pesticide-card">
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <h6 className="mb-1">{rec.name}</h6>
                  <div>
                    {rec.organic_approved && (
                      <span className="organic-badge me-1">Organic</span>
                    )}
                    <span className={`safety-badge safety-${rec.safety_level.toLowerCase().replace(' ', '-')}`}>
                      {rec.safety_level}
                    </span>
                  </div>
                </div>
                <p className="text-muted small mb-2">
                  <strong>Active Ingredient:</strong> {rec.active_ingredient}<br />
                  <strong>Method:</strong> {rec.application_method}<br />
                  <strong>Dosage:</strong> {rec.dosage}<br />
                  <strong>Frequency:</strong> {rec.frequency}
                </p>
                <div className="d-flex justify-content-between align-items-center">
                  <small className="text-muted">
                    <i className="fas fa-chart-line me-1"></i>
                    {rec.effectiveness} Effectiveness
                  </small>
                  <small className="text-muted">
                    <i className="fas fa-dollar-sign me-1"></i>
                    {rec.cost_level} Cost
                  </small>
                </div>
              </div>
            ))
          ) : (
            <div className="alert alert-info">
              <i className="fas fa-info-circle me-2"></i>
              No specific pesticide recommendations available for this disease.
            </div>
          )}
        </div>
      </div>
      
      {safety_guidelines.general_safety && (
        <>
          <hr className="my-4" />
          <div className="row">
            <div className="col-md-4">
              <h6>
                <i className="fas fa-exclamation-triangle text-warning me-2"></i>
                Safety Guidelines
              </h6>
              <ul className="list-unstyled small">
                {safety_guidelines.general_safety.slice(0, 3).map((g, i) => (
                  <li key={i}>
                    <i className="fas fa-check text-success me-2"></i>{g}
                  </li>
                ))}
              </ul>
            </div>
            <div className="col-md-4">
              <h6>
                <i className="fas fa-leaf text-success me-2"></i>
                Environmental Protection
              </h6>
              <ul className="list-unstyled small">
                {safety_guidelines.environmental_protection.slice(0, 3).map((g, i) => (
                  <li key={i}>
                    <i className="fas fa-check text-success me-2"></i>{g}
                  </li>
                ))}
              </ul>
            </div>
            <div className="col-md-4">
              <h6>
                <i className="fas fa-recycle text-info me-2"></i>
                Sustainable Practices
              </h6>
              <ul className="list-unstyled small">
                {safety_guidelines.sustainable_practices.slice(0, 3).map((g, i) => (
                  <li key={i}>
                    <i className="fas fa-check text-success me-2"></i>{g}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ResultsSection;
