import torch
import pickle
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# Import preprocessing functions
from preprocessing import bandpass_filter
from feature_extraction import extract_features
from utils import EMOTION_LABELS

# Import correct transformer model
from transformer_model import EmotionTransformer

# ---------------------------
# FastAPI Initialization
# ---------------------------
app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Load Model
# ---------------------------
device = torch.device("cpu")

model = EmotionTransformer()

state_dict = torch.load("transformer_model.pth", map_location=device)

model.load_state_dict(state_dict, strict=False)

model.eval()

# ---------------------------
# Prediction Endpoint
# ---------------------------
@app.post("/predict")
async def predict_emotion(file: UploadFile = File(...)):

    try:
        # Read uploaded EEG file
        contents = await file.read()

        # Load DEAP .dat file
        raw_data = pickle.loads(contents, encoding="latin1")

        # Extract EEG signals
        X = raw_data["data"].astype("float32")

        # Process only first trial for demo
        trial = X[0:1]

        # ---------------------------
        # Preprocessing
        # ---------------------------
        X_filt = bandpass_filter(
            trial,
            fs=128,
            lowcut=4,
            highcut=45
        )

        features, _ = extract_features(
            X_filt,
            fs=128,
            aggregate=True,
            epoch_length=1
        )

        # ---------------------------
        # Prepare Transformer Input
        # ---------------------------
        features_seq = features.reshape(1, -1, 4)

        # Trim to model sequence length
        features_seq = features_seq[:, :60, :]

        X_tensor = torch.tensor(
            features_seq,
            dtype=torch.float32
        ).to(device)

        # ---------------------------
        # Model Prediction
        # ---------------------------
        with torch.no_grad():

            output = model(X_tensor)

            prediction = torch.argmax(output, dim=1).item()

            prob = torch.softmax(output, dim=1)

            confidence = prob[0][prediction].item()

        return {
            "status": "success",
            "emotion": EMOTION_LABELS[prediction],
            "confidence": confidence
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

# ---------------------------
# Run Server
# ---------------------------
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )