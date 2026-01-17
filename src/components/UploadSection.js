import React, { useRef, useState, useEffect } from 'react';

const UploadSection = ({ onFileSelect, onPredict, onReset, selectedFile, imagePreview, loading }) => {
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showCamera, setShowCamera] = useState(false);
  const [stream, setStream] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const [cameraLoading, setCameraLoading] = useState(false);

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileSelect(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  // Camera functions
  const startCamera = async () => {
    console.log('startCamera called');
    try {
      setCameraError(null);
      setCameraLoading(true);
      
      console.log('Checking secure context...');
      // Check if we're in a secure context (HTTPS or localhost)
      const isSecureContext = window.isSecureContext || 
                              window.location.protocol === 'https:' || 
                              window.location.hostname === 'localhost' || 
                              window.location.hostname === '127.0.0.1';
      
      if (!isSecureContext) {
        throw new Error('Camera requires a secure connection (HTTPS). Please access this site via HTTPS or localhost.');
      }
      
      // Check if getUserMedia is available
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera API not supported in this browser. Please use a modern browser like Chrome, Firefox, or Safari.');
      }

      // Show modal first so video element exists
      setShowCamera(true);

      // Try different camera constraints with fallback
      let mediaStream = null;
      const constraints = [
        // Try 1: Back camera (mobile) with high quality
        {
          video: {
            facingMode: 'environment',
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        },
        // Try 2: Any camera with high quality
        {
          video: {
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        },
        // Try 3: Any camera with default quality
        {
          video: true
        },
        // Try 4: Front camera as last resort
        {
          video: {
            facingMode: 'user'
          }
        }
      ];

      // Try each constraint until one works
      for (const constraint of constraints) {
        try {
          mediaStream = await navigator.mediaDevices.getUserMedia(constraint);
          break; // Success, exit loop
        } catch (err) {
          console.log('Trying next camera constraint...', err.name);
          if (constraint === constraints[constraints.length - 1]) {
            throw err; // Last attempt failed, throw error
          }
        }
      }

      if (!mediaStream) {
        throw new Error('Could not access any camera');
      }

      console.log('Camera stream obtained successfully:', mediaStream);
      setStream(mediaStream);
      // Loading will be set to false in useEffect when video starts playing

    } catch (err) {
      console.error('Error accessing camera:', err);
      setCameraLoading(false);
      setShowCamera(true); // Show modal to display error
      
      // Provide specific error messages
      let errorMessage = 'Unable to access camera. ';
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        errorMessage += 'Camera permission was denied. Please allow camera access in your browser settings and try again.';
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        errorMessage += 'No camera found. Please connect a camera and try again.';
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        errorMessage += 'Camera is being used by another application. Please close other apps using the camera and try again.';
      } else if (err.name === 'OverconstrainedError' || err.name === 'ConstraintNotSatisfiedError') {
        errorMessage += 'Camera does not support the requested settings. Trying with default settings...';
        // Retry with simpler constraints
        setTimeout(() => {
          startCamera();
        }, 1000);
        return;
      } else if (err.message.includes('not supported')) {
        errorMessage = err.message;
      } else {
        errorMessage += `Error: ${err.message || err.name}`;
      }
      
      setCameraError(errorMessage);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
      videoRef.current.onloadedmetadata = null;
      videoRef.current.onplay = null;
      videoRef.current.onerror = null;
    }
    setShowCamera(false);
    setCameraError(null);
    setCameraLoading(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      // Set canvas dimensions to match video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Draw video frame to canvas
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Convert canvas to blob, then to File
      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], 'camera-capture.jpg', {
            type: 'image/jpeg',
            lastModified: Date.now()
          });
          
          // Use the existing file select handler
          onFileSelect(file);
          
          // Stop camera
          stopCamera();
        }
      }, 'image/jpeg', 0.95);
    }
  };

  // Handle video element when stream changes
  useEffect(() => {
    if (stream && videoRef.current && showCamera) {
      const video = videoRef.current;
      
      console.log('Setting up video element with stream:', stream);
      
      // Set the stream
      video.srcObject = stream;
      
      // Ensure video is ready
      const handleLoadedMetadata = () => {
        console.log('Video metadata loaded. Dimensions:', video.videoWidth, 'x', video.videoHeight);
        
        // Check if video has valid dimensions
        if (video.videoWidth === 0 || video.videoHeight === 0) {
          console.warn('Video has zero dimensions, waiting...');
          setTimeout(() => {
            if (video.videoWidth > 0 && video.videoHeight > 0) {
              video.play();
            }
          }, 100);
          return;
        }
        
        // Play the video
        video.play()
          .then(() => {
            console.log('Video playing successfully');
            setCameraLoading(false);
          })
          .catch(err => {
            console.error('Error playing video:', err);
            setCameraError('Error starting video playback: ' + err.message);
            setCameraLoading(false);
          });
      };

      const handlePlaying = () => {
        console.log('Video is now playing');
        setCameraLoading(false);
      };

      const handlePlay = () => {
        console.log('Video play event fired');
        setCameraLoading(false);
      };

      const handleError = (err) => {
        console.error('Video error:', err);
        setCameraError('Error displaying camera feed. Please try again.');
        setCameraLoading(false);
      };

      const handleCanPlay = () => {
        console.log('Video can play');
        if (video.paused) {
          video.play().catch(err => {
            console.error('Error in canPlay play:', err);
          });
        }
      };

      // Attach event listeners
      video.addEventListener('loadedmetadata', handleLoadedMetadata);
      video.addEventListener('playing', handlePlaying);
      video.addEventListener('play', handlePlay);
      video.addEventListener('canplay', handleCanPlay);
      video.addEventListener('error', handleError);

      // Try to play immediately (some browsers need this)
      if (video.readyState >= 2) {
        video.play().catch(err => {
          console.log('Immediate play failed, waiting for metadata:', err);
        });
      }

      // Force play after a short delay (for browsers that need user interaction)
      const forcePlayTimeout = setTimeout(() => {
        if (video.paused && video.readyState >= 2) {
          console.log('Force playing video...');
          video.play().catch(err => {
            console.log('Force play failed:', err);
          });
        }
      }, 500);

      // Cleanup function
      return () => {
        clearTimeout(forcePlayTimeout);
        video.removeEventListener('loadedmetadata', handleLoadedMetadata);
        video.removeEventListener('playing', handlePlaying);
        video.removeEventListener('play', handlePlay);
        video.removeEventListener('canplay', handleCanPlay);
        video.removeEventListener('error', handleError);
      };
    }

    return () => {
      // Cleanup on unmount
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream, showCamera]);

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

  return (
    <div className="card upload-card p-4 mb-4">
      <div 
        className={`upload-area ${isDragOver ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <i className="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
        <h5>Upload Plant Leaf Image</h5>
        <p className="text-muted">Drag and drop an image here or click to browse</p>
        <input 
          ref={fileInputRef}
          className="form-control d-none" 
          type="file" 
          accept="image/*" 
          onChange={handleFileInputChange}
        />
        <div className="d-flex gap-2 justify-content-center flex-wrap">
          <button 
            type="button" 
            className="btn btn-outline-primary"
            onClick={(e) => {
              e.stopPropagation();
              handleClick();
            }}
          >
            <i className="fas fa-folder-open me-2"></i>Choose File
          </button>
          <button 
            type="button" 
            className="btn btn-outline-success"
            onClick={(e) => {
              e.stopPropagation();
              console.log('Camera button clicked, starting camera...');
              startCamera();
            }}
            disabled={cameraLoading}
          >
            <i className="fas fa-camera me-2"></i>Use Camera
          </button>
        </div>
      </div>
      
      {imagePreview && (
        <div className="text-center">
          <img src={imagePreview} className="image-preview" alt="Preview" />
          <p className="text-muted mt-2">
            <i className="fas fa-check-circle text-success me-1"></i>Image ready for analysis
          </p>
        </div>
      )}
      
      <div className="text-center mt-3">
        {selectedFile ? (
          <div>
            <button 
              className="btn btn-primary btn-lg me-2" 
              onClick={onPredict}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="loading-spinner me-2"></span>Analyzing...
                </>
              ) : (
                <>
                  <i className="fas fa-search me-2"></i>Analyze Disease
                </>
              )}
            </button>
            <button 
              className="btn btn-outline-secondary" 
              onClick={onReset}
              disabled={loading}
            >
              <i className="fas fa-times me-2"></i>Reset
            </button>
          </div>
        ) : (
          <p className="text-muted">Please select an image to analyze</p>
        )}
      </div>

      {/* Camera Modal */}
      {showCamera && (
        <div className="camera-modal-overlay" onClick={stopCamera}>
          <div className="camera-modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="camera-modal-header">
              <h5 className="mb-0">
                <i className="fas fa-camera me-2"></i>Camera Capture
              </h5>
              <button 
                type="button" 
                className="btn-close" 
                onClick={stopCamera}
                aria-label="Close"
              ></button>
            </div>
            
            <div className="camera-modal-body">
              {cameraError ? (
                <div className="alert alert-danger m-3">
                  <i className="fas fa-exclamation-triangle me-2"></i>
                  <strong>Camera Error:</strong>
                  <p className="mb-0 mt-2">{cameraError}</p>
                  <div className="mt-3">
                    <button 
                      className="btn btn-primary"
                      onClick={() => {
                        setCameraError(null);
                        startCamera();
                      }}
                    >
                      <i className="fas fa-redo me-2"></i>Try Again
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  {/* Show video if stream exists, even if loading */}
                  {stream && (
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="camera-video"
                      style={{
                        width: '100%',
                        height: 'auto',
                        maxWidth: '100%',
                        display: 'block',
                        backgroundColor: '#000',
                        minHeight: '400px',
                        objectFit: 'contain'
                      }}
                    ></video>
                  )}
                  
                  {/* Show loading overlay only if loading and no stream yet */}
                  {cameraLoading && !stream && (
                    <div className="d-flex flex-column align-items-center justify-content-center" style={{ 
                      minHeight: '400px',
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      bottom: 0,
                      backgroundColor: 'rgba(0,0,0,0.8)',
                      zIndex: 10
                    }}>
                      <div className="loading-spinner mb-3" style={{ width: '50px', height: '50px', borderWidth: '5px' }}></div>
                      <p className="text-white">Starting camera...</p>
                      <small className="text-white-50">Please allow camera access if prompted</small>
                    </div>
                  )}
                  
                  <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>
                  
                  {stream && !cameraLoading && (
                    <div className="text-white text-center mt-2" style={{ position: 'relative', zIndex: 5 }}>
                      <small>Camera is active. Position your leaf in the frame.</small>
                    </div>
                  )}
                </>
              )}
            </div>
            
            <div className="camera-modal-footer">
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={stopCamera}
              >
                <i className="fas fa-times me-2"></i>Cancel
              </button>
              {!cameraError && (
                <button 
                  type="button" 
                  className="btn btn-primary btn-lg"
                  onClick={capturePhoto}
                >
                  <i className="fas fa-camera me-2"></i>Capture Photo
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadSection;
