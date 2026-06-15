import React, { useRef, useState } from "react";
import "./UploadSection.css";

function UploadSection() {
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [prediction, setPrediction] = useState(null);

  const emotionEmojis = {
  Happy: "😄",
  Relaxed: "🙂",
  Angry: "😠",
  Sad: "😢"
};
const emotionColors = {
  Happy: "#22c55e",
  Relaxed: "#10b981",
  Angry: "#ef4444",
  Sad: "#3b82f6"
};

  const handleBoxClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const startAnalysis = async () => {
    if (!file) {
      alert("PLEASE INITIALIZE DATA INPUT: NO FILE DETECTED");
      return;
    }

    setIsAnalyzing(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData
      });

      if (!response.ok) throw new Error("Neural Link Failure");

      const data = await response.json();
      setPrediction(data.emotion);

    } catch (error) {
      console.error("Analysis Error:", error);
      alert("SYSTEM ERROR: UNABLE TO REACH BACKEND");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <section className="upload-section">
      <div className="upload-glass-container">
        <div className="scan-line"></div>

        <header className="upload-header">
          <span className="system-status">
            {isAnalyzing
              ? "ANALYZING..."
              : prediction
              ? "ANALYSIS COMPLETE"
              : "System Ready"}
          </span>

          <h2>NEURAL DATA INPUT</h2>
          <p>Initialize emotion recognition by uploading your EEG dataset.</p>
        </header>

        <div className="upload-drop-zone" onClick={handleBoxClick}>
          <div className="icon-wrap">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
          </div>

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            hidden
            accept=".dat,.csv,.bin"
          />

          <span className="upload-label">
            {fileName ? fileName : "DROP EEG FILE OR CLICK TO BROWSE"}
          </span>

          {prediction && (
            <div
              style={{
                marginTop: "25px",
                fontFamily: "Syncopate",
                textAlign: "center"
              }}
            >
              <div
                style={{
                  color: "#10b981",
                  fontSize: "12px",
                  letterSpacing: "3px",
                  marginBottom: "10px"
                }}
              >
                EMOTION DETECTED
              </div>

              {/* EMOJI */}
              <div style={{ fontSize: "45px", marginBottom: "10px" }}>
  {emotionEmojis[prediction]}
</div>

              {/* EMOTION TEXT */}
              <div
                style={{
                  color: emotionColors[prediction] || "#3b82f6",
                  fontSize: "28px",
                  letterSpacing: "4px"
                }}
              >
                {prediction}
              </div>
            </div>
          )}

          <div className="corner-tl"></div>
          <div className="corner-br"></div>
        </div>

        <button
          className="process-btn"
          onClick={startAnalysis}
          disabled={isAnalyzing}
        >
          <span className="btn-glow"></span>

          <span className="btn-text">
            {isAnalyzing ? "PROCESSING..." : "START ANALYSIS"}
          </span>
        </button>

        <footer className="upload-footer">
          <span>Supported: CSV, EDF, RAW</span>
          <span>Encryption: AES-256</span>
        </footer>
      </div>
    </section>
  );
}

export default UploadSection;