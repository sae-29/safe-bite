from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import traceback
from dotenv import load_dotenv
import os

# Load environment variables from .env file (Override system/terminal variables)
load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: Loaded API Key starting with: {api_key[:10] if api_key else 'None'}...")

from .ocr.ocr_engine import extract_text
from .ocr.filter import filter_ingredient_text
from .ocr.parser import parse_ingredients
from .ml.predict import predict_ingredient
from .ml.risk_engine import calculate_risk_score
from .gemini.explain import explain_with_gemini

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Snack Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://safebite-flax.vercel.app",
        "https://safebite-flax.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReExplainRequest(BaseModel):
    ingredients_analysis: List[Dict[str, Any]]
    profile: str

@app.post("/analyze")
async def analyze_snack(file: UploadFile = File(...), profile: str = Form("General")):
    temp_path = f"temp_{uuid.uuid4()}.jpg"

    try:
        # Save uploaded image
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # OCR
        print(f"DEBUG: Extracting text from {temp_path}...")
        raw_text = extract_text(temp_path)
        print(f"DEBUG: Raw OCR text: {raw_text[:100]}...")
        
        # Filter to get only ingredients
        print("DEBUG: Filtering OCR text for ingredients...")
        filtered_text = filter_ingredient_text(raw_text)
        print(f"DEBUG: Filtered text: {filtered_text[:100]}...")

        # Ingredient parsing (use filtered text)
        parsed = parse_ingredients(filtered_text)
        print(f"DEBUG: Parsed ingredients: {parsed}")

        # ML inference
        results = [predict_ingredient(i) for i in parsed["ingredients"]]
        print(f"DEBUG: ML Results: {results}")

        # Risk Calculation
        risk_data = calculate_risk_score(filtered_text, results)
        print(f"DEBUG: Risk Score: {risk_data}")

        # Gemini explanation
        print(f"DEBUG: Calling Gemini with profile '{profile}'...")
        explanation = explain_with_gemini(results, profile)
        print("DEBUG: Gemini response received.")

        return {
            "extracted_text": filtered_text,
            "ingredients_analysis": results,
            "risk_score": risk_data["score"],
            "risk_level": risk_data["level"],
            "risk_breakdown": risk_data["breakdown"],
            "explanation": explanation
        }
    except Exception as e:
        print("ERROR: Analysis failed")
        traceback.print_exc()
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.post("/re-explain")
async def re_explain(request: ReExplainRequest):
    """
    Re-generates the Gemini explanation for an existing analysis based on a new profile.
    Does NOT re-run OCR or ML predictions.
    """
    try:
        print(f"DEBUG: Re-explaining for profile '{request.profile}'...")
        new_explanation = explain_with_gemini(request.ingredients_analysis, request.profile)
        return {"explanation": new_explanation}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
