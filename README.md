# 🌱 AI Plant Disease Classifier

React frontend for AI-powered plant disease classification with pesticide recommendations.

## 🚀 Quick Start

### Development Mode
```cmd
# Command Prompt
start_dev.bat

# PowerShell
.\start_dev.bat
```
This starts both React (port 3000) and Flask (port 5000).

### Manual Start
```cmd
# Terminal 1: Flask backend
python app.py

# Terminal 2: React frontend  
npm start
```

## 📁 Project Structure
- `src/` - React components
- `public/` - Static files
- `app.py` - Flask backend
- `prediction_api.py` - ML prediction API
- `model/` - Trained ML models
- `dataset/` - Training data

## 🎯 Features
- Drag & drop image upload
- AI disease classification
- Pesticide recommendations
- Safety guidelines
- Responsive design

## 🔧 Dependencies
- Python: `pip install -r requirements.txt`
- Node.js: `npm install`

## 📤 Upload Dataset to S3

To store the `dataset/` folder in AWS S3:

### Prerequisites
1. [Install AWS CLI](https://aws.amazon.com/cli/) (optional, for CLI method)
2. Configure AWS credentials:
   - **Option A**: `aws configure` (sets `~/.aws/credentials`)
   - **Option B**: Environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

### Method 1: Python script (recommended)
```bash
pip install boto3
python upload_dataset_to_s3.py YOUR_BUCKET_NAME dataset
```
Or with env vars:
```bash
set S3_BUCKET=your-bucket-name
set S3_DATASET_PREFIX=dataset
python upload_dataset_to_s3.py
```

### Method 2: AWS CLI
```bash
aws s3 sync dataset/ s3://YOUR_BUCKET_NAME/dataset/
```

## ☁️ Deploy backend on Render

1. Push this repo to GitHub (see below).
2. In [Render](https://render.com): **New** → **Web Service** → connect the repo.
3. **Settings:**
   - **Runtime:** Python
   - **Build command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start command:** `gunicorn prediction_api:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120`
4. **Model files:** `model/` is gitignored by default. Add `best_model.keras` / `final_model.keras` and `class_indices.json` via Git LFS, or upload after deploy — see `model/README.md`.
5. TensorFlow needs **enough RAM**; the free tier may fail — use a **paid** instance if builds or runtime crash.
6. After deploy, copy your service URL (e.g. `https://plant-disease-api.onrender.com`).
7. **Frontend:** create `.env.production` or set in your host:
   ```bash
   REACT_APP_API_URL=https://your-service.onrender.com
   ```
   Then `npm run build`. For local dev, leave unset to use `http://localhost:5000`.

Optional: **New** → **Blueprint** → select `render.yaml` in the repo.

## 📤 Push to GitHub

```bash
git add .
git status
git commit -m "Your message"
git push origin main
```