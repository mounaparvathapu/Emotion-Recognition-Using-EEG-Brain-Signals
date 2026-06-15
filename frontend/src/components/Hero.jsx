import "./Hero.css";
import backgroundVideo from "../assets/youtubebrain.mp4";

function Hero({ onContinue }) {
  return (
    <section className="hero-container">

      <video
        className="background-video"
        src={backgroundVideo}
        autoPlay
        loop
        muted
        playsInline
      />

      <div className="overlay"></div>

      <div className="hero-content">
        <h1 className="hero-title">
          Emotion Recognition
          <br />
          <span>Using EEG-Based Signals</span>
        </h1>

        <p className="hero-description">
          AI-powered neural system that detects emotional states using EEG.
        </p>

        <button className="hero-button" onClick={onContinue}>
          Continue
        </button>
      </div>

    </section>
  );
}

export default Hero;