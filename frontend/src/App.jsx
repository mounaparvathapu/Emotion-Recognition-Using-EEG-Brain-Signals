import { useRef } from "react";
import Hero from "./components/Hero";
import SignalInfo from "./components/SignalInfo";
import UploadSection from "./components/UploadSection";

function App() {
  const signalRef = useRef(null);
  const uploadRef = useRef(null);

  const scrollToSignal = () => {
    signalRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const scrollToUpload = () => {
    uploadRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <>
      <Hero onContinue={scrollToSignal} />

      <div ref={signalRef}>
        <SignalInfo onContinue={scrollToUpload} />
      </div>

      <div ref={uploadRef}>
        <UploadSection />
      </div>
    </>
  );
}

export default App;