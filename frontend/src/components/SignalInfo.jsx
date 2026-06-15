import React from 'react';
import "./SignalInfo.css";

function SignalInfo({ onContinue }) {
  return (
    <section className="signal-viewport">
      <div className="overlay-shade"></div>
      
      <div className="content-layer">
        <header className="glass-header">
          {/* <span className="accent-line">Neural Spectrum Analysis</span> */}
          <h1>DETECTED EMOTIONAL STATES</h1>
        </header>

        <div className="identities-grid">
          {/* LEFT SIDE */}
          <div className="column left">
            <div className="neu-card alpha">
              <div className="glow-dot"></div>
              <div className="card-text">
                <h3>Happy</h3>
                <span className="state-tag">Deep Calm</span>
                <p>Positive state with increased Alpha (α) and Gamma (γ) activity.</p>
              </div>
            </div>

            <div className="neu-card theta">
              <div className="glow-dot"></div>
              <div className="card-text">
                <h3> Relaxed</h3>
                <span className="state-tag">Introspection</span>
                <p>Dominant Alpha (α) and Theta (θ) waves indicating calm mental state.</p>
              </div>
            </div>
          </div>

          {/* RIGHT SIDE */}
          <div className="column right">
            <div className="neu-card beta">
              <div className="glow-dot"></div>
              <div className="card-text">
                <h3>sad</h3>
                <span className="state-tag">Active Focus</span>
                <p>Associated with Theta (θ) and Delta (δ) activity reflecting low arousal.</p>
              </div>
            </div>

            <div className="neu-card gamma">
              <div className="glow-dot"></div>
              <div className="card-text">
                <h3>Stressed</h3>
                <span className="state-tag">Peak Performance</span>
                <p>High Beta (β) and Gamma (γ) waves linked to stress and alertness.</p>
              </div>
            </div>
          </div>
        </div>

        {/* NEW CONTINUE BUTTON */}
        <div className="signal-continue">
          <button className="upload-btn" onClick={onContinue}>
            Upload Neural Data
          </button>
        </div>

      </div>
    </section>
  );
}

export default SignalInfo;