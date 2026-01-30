import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [profile, setProfile] = useState("General");
  const [loading, setLoading] = useState(false);
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const resultsRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setResult(null);
    setError("");

    // Create preview URL
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleProfileChange = (e) => {
    setProfile(e.target.value);
  };

  // Real-time personalization effect
  useEffect(() => {
    if (result && result.ingredients_analysis && profile) {
      const reExplain = async () => {
        const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

        try {
          setIsPersonalizing(true);
          const payload = {
            ingredients_analysis: result.ingredients_analysis,
            profile: profile
          };

          const response = await axios.post(`${API_URL}/re-explain`, payload);

          if (response.data && response.data.explanation) {
            setResult(prev => ({
              ...prev,
              explanation: response.data.explanation
            }));
          }
        } catch (err) {
          console.error("Re-explanation failed:", err);
        } finally {
          setIsPersonalizing(false);
        }
      };

      const timer = setTimeout(reExplain, 500);
      return () => clearTimeout(timer);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profile]);

  const analyzeSnack = async () => {
    const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

    if (!image) {
      setError("Please select an image first");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("profile", profile);

    try {
      setLoading(true);
      setError("");

      const response = await axios.post(
        `${API_URL}/analyze`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      if (response.data.error) {
        setError(`Analysis failed: ${response.data.error}`);
        console.error("Backend error:", response.data);
        return;
      }

      if (!response.data.ingredients_analysis || !response.data.explanation) {
        setError("Invalid response from server. Please try again.");
        console.error("Invalid response:", response.data);
        return;
      }

      setResult(response.data);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);

    } catch (err) {
      setError("Analysis failed. Please check if the backend is running.");
      console.error("Request error:", err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    if (level === "Safe") return "#28a745";
    if (level === "Moderate") return "#ffc107";
    return "#dc3545";
  };

  return (
    <div className="main-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="grid-overlay"></div>
        <div className="hero-content">
          <div className="badge-pill">AI-Powered Food Safety</div>
          <h1>Understand what you eat <br /><span>before it affects your health.</span></h1>
          <p className="hero-subtext">
            Upload a snack label to get instant ingredient analysis, risk scoring,
            and personalized health insights.
          </p>

          <div className="action-area">
            <div className="upload-wrapper">
              <input
                type="file"
                id="file-upload"
                accept="image/*"
                onChange={handleImageChange}
              />
              <label htmlFor="file-upload" className="custom-file-upload">
                {image ? "✅ Image Selected" : "  Upload Label Image"}
              </label>
            </div>

            {image && (
              <div className="profile-wrapper">
                <span className="label-text">For Profile:</span>
                <select value={profile} onChange={handleProfileChange} className="profile-select">
                  <option value="General">General</option>
                  <option value="Diabetic">Diabetic (Diabetes)</option>
                  <option value="Hypertension">Hypertension (High BP)</option>
                  <option value="Child">Child (Sensitive)</option>
                  <option value="Allergy-Prone">Allergy Prone</option>
                  <option value="Weight Loss">Weight Loss</option>
                </select>
              </div>
            )}

            <button
              className={`analyze-btn ${loading ? 'loading' : ''}`}
              onClick={analyzeSnack}
              disabled={loading || !image}
            >
              {loading ? "Analyzing..." : "🔍 Analyze Now"}
            </button>
          </div>
          {error && <p className="error-message">{error}</p>}
        </div>
      </section>

      {/* Split-Screen Results */}
      <div ref={resultsRef}>
        {result && result.ingredients_analysis && result.explanation && (
          <div className="split-container">

            {/* LEFT PANEL - What Was Scanned (Static) */}
            <div className="left-panel">
              <div className="panel-header">
                <h2>� What Was Scanned</h2>
                <p>This is what we found on the label</p>
              </div>

              {/* Uploaded Image Preview */}
              {imagePreview && (
                <div className="image-preview-section">
                  <img src={imagePreview} alt="Uploaded food label" className="uploaded-image" />
                </div>
              )}

              {/* Extracted Text */}
              <div className="ocr-section">
                <h3>📄 Detected Ingredients (from packaging)</h3>
                <p className="filter-note">Filtered to show only consumable ingredients</p>
                <div className="receipt-paper">
                  "{result.extracted_text || 'No ingredients detected'}"
                </div>
              </div>

              {/* Ingredients List */}
              <div className="ingredients-section">
                <h3>🧾 Detected Ingredients</h3>
                <div className="ingredients-grid">
                  {(result.ingredients_analysis || []).map((item, index) => (
                    <div key={index} className={`ingredient-card ${item.risk?.toLowerCase() || 'safe'}`}>
                      <div className="card-top">
                        <strong>{item.ingredient || 'Unknown'}</strong>
                        <span className={`risk-badge ${item.risk?.toLowerCase() || 'safe'}`}>
                          {item.risk || 'Safe'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* RIGHT PANEL - What It Means for YOU (Dynamic) */}
            <div className="right-panel">
              <div className="panel-header sticky-header">
                <div className="header-content">
                  <h2>🧠 What It Means for YOU</h2>
                  <div className="profile-selector-inline">
                    <label>Health Profile:</label>
                    <select value={profile} onChange={handleProfileChange} className="profile-select-inline">
                      <option value="General">General</option>
                      <option value="Diabetic">Diabetic</option>
                      <option value="Hypertension">Hypertension</option>
                      <option value="Child">Child</option>
                      <option value="Allergy-Prone">Allergy Prone</option>
                      <option value="Weight Loss">Weight Loss</option>
                    </select>
                  </div>
                </div>
                {isPersonalizing && <div className="personalizing-banner">🔄 Personalizing for {profile}...</div>}
              </div>

              <div className={`dynamic-content ${isPersonalizing ? 'blur-text' : ''}`}>
                {/* Risk Score */}
                <div className="risk-score-compact">
                  <div className="score-circle-small" style={{
                    background: `conic-gradient(
                                ${getRiskColor(result.risk_level || 'Safe')} ${result.risk_score || 0}%, 
                                #eef2f5 ${result.risk_score || 0}% 100%
                            )`
                  }}>
                    <div className="score-inner">
                      <span className="score-num">{result.risk_score || 0}</span>
                    </div>
                  </div>
                  <div className="score-info">
                    <h3>{result.risk_level || 'Safe'} Risk</h3>
                    <p>For {profile} profile</p>
                  </div>
                </div>

                {/* Risk Explanation */}
                <div className="risk-explanation-box">
                  <h3>1️⃣ Why This Product Is Risky for {profile}</h3>
                  <div className="explanation-content">
                    <p className="main-explanation">
                      {typeof result.explanation.harm_explanation === 'string'
                        ? result.explanation.harm_explanation
                        : JSON.stringify(result.explanation.harm_explanation)}
                    </p>
                  </div>

                  {result.explanation.risk_factors && result.explanation.risk_factors.length > 0 && (
                    <ul className="risk-list">
                      {result.explanation.risk_factors.map((r, i) => (
                        <li key={i}>{r}</li>
                      ))}
                    </ul>
                  )}
                </div>

                {/* Natural Alternatives */}
                {result.explanation.alternatives && result.explanation.alternatives.length > 0 && (
                  <div className="alternatives-box">
                    <h3>2️⃣ Safer Food Alternatives (Natural / Homemade)</h3>
                    <p className="section-subtitle">Practical & healthier options</p>
                    <div className="alt-cards">
                      {result.explanation.alternatives.map((alt, i) => (
                        <div key={i} className="alt-card">
                          <h4>🥗 {alt.name || 'Alternative'}</h4>
                          <p><strong>Why:</strong> {alt.why || 'Healthier option'}</p>
                          <div className="tag-group">
                            <span className="benefit-tag">Benefit: {alt.benefit}</span>
                            <span className="usage-tag">Tip: {alt.how_to_use}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Commercial Products */}
                {result.explanation.commercial_alternatives && result.explanation.commercial_alternatives.length > 0 && (
                  <div className="commercial-box">
                    <h3>3️⃣ Commercial Healthier Product Suggestions</h3>
                    <p className="section-subtitle">Realistic market options</p>
                    <div className="commercial-cards">
                      {result.explanation.commercial_alternatives.map((prod, i) => (
                        <div key={i} className="commercial-card">
                          <h4>🛒 {prod.product_name || 'Product'}</h4>
                          <p><strong>Why Better:</strong> {prod.why_better}</p>
                          <p className="availability"><small>📍 {prod.availability}</small></p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

