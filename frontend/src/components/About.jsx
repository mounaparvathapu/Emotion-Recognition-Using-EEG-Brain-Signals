import React from 'react';
import "./About.css";

function About() {
  return (
    <section className="about-page">
      <div className="about-glass-card">
        <span className="subtitle">Neural Science</span>
        <h2>EEG & Brain Signals</h2>
        <p>
          EEG (Electroencephalography) measures voltage fluctuations resulting from ionic current 
          within the neurons of the brain. These signals are categorized 
          into frequency bands:
        </p>
        <ul className="science-list">
          <li><strong>Alpha:</strong> Associated with deep calm and flow.</li>
          <li><strong>Beta:</strong> Linked to active focus and problem-solving.</li>
          <li><strong>Gamma:</strong> The highest frequency for peak performance.</li>
        </ul>
        <div className="about-divider"></div>
        <h2>The AI Developer</h2>
        <p>
          I am Gemini, your AI peer. I designed this interface to visualize the invisible 
          rhythms of the human mind, combining neural data with cinematic design.
        </p>
      </div>
    </section>
  );
}

export default About;