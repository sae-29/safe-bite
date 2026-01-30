# 🥗 Safe Bite: AI-Powered Snack Analyzer

Safe Bite is a premium AI-powered web application designed to help users understand what's in their food. By simply uploading a photo of a snack label, the app extracts ingredients using **Gemini Cloud Vision**, analyzes their health risks based on a personalized profile (Diabetic, Hypertension, etc.), and provides natural and commercial alternatives.

## 🚀 Live Demo
- **Web App**: [https://safebite-flax.vercel.app/](https://safebite-flax.vercel.app/)
- **Backend API**: [https://safe-bite-backend-39h0.onrender.com/health](https://safe-bite-backend-39h0.onrender.com/health)

## ✨ Key Features
- **Cloud OCR**: Ultra-accurate ingredient extraction using Gemini 1.5 Flash.
- **Intelligent Risk Scoring**: Ingredients are automatically categorized as Safe, Moderate, or Harmful.
- **Personalized Insights**: Tailored advice for specific health profiles (e.g., Diabetic, Child, Weight Loss).
- **Smart Recommendations**: Suggests 3 natural and 3 commercial healthier alternatives for every scan.
- **Premium UI**: Modern, glassmorphism-inspired design with smooth animations.

---

## 🛠️ Local Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Node.js & npm
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 2. Backend Setup (FastAPI)
```bash
# Navigate to the root directory
cd snack-analyzer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file in the root
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run the server
uvicorn backend.main:app --reload
```
The backend will be running at `http://localhost:8000`.

### 3. Frontend Setup (React)
```bash
# Navigate to the frontend directory
cd snack-analyzer-frontend

# Install dependencies
npm install

# Create a .env file in snack-analyzer-frontend/
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start the app
npm start
```
The app will be running at `http://localhost:3000`.

---

## 🏗️ Technology Stack
- **Frontend**: React, Vanilla CSS3 (Custom Glassmorphism), Axios
- **Backend**: Ml model, FastAPI (Python), Uvicorn, Pydantic
- **AI/ML**: DistilBert Model(Fine Tuning), Google GenAI SDK (Gemini 1.5 Flash), Custom Keyword Scoring Engine(ocr)
- **Deployment**: Vercel (Frontend), Render (Backend)

## 🛡️ Security
- **Strict CORS**: Only trusted domains can interact with the API.
- **Server-Side Processing**: API keys are never exposed to the client.

---

## 🤝 Contributing
Feel free to fork this repository, open issues, or submit pull requests to help make everyone's snacking habits safer!

**Stay Healthy! 🍎**
