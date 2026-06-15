"""
Transformer model for EEG emotion recognition using band‑power sequences.

This module defines a PyTorch module that accepts a sequence of band‑power
vectors (e.g., 1‑second epochs aggregated across channels) and outputs class
logits for emotion classification.  It uses a standard TransformerEncoder
architecture with positional encoding and a simple mean‑pooling readout.

The model expects input of shape (batch_size, seq_len, input_dim).  Each
time‑step corresponds to an epoch and contains features such as theta, alpha,
beta and gamma band powers.  The positional encoding is learnable.

This implementation is inspired by recent work that uses separate spatial and
temporal transformers to model EEG signals.  For example, the EmoSTT model
applies separate Transformer modules to capture correlations between EEG
channels and between time frames; these Transformer blocks learn
spatial‑temporal dependencies and feed their outputs into a fully connected
layer to decode emotions【332443011832974†L320-L331】.  Here we adopt a simpler
temporal Transformer on pre‑aggregated band‑power sequences.
"""

from __future__ import annotations

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class PositionalEncoding(nn.Module):
    """Learnable positional encoding for sequences.

    Adds a learnable embedding vector to each time step to encode position
    information.  This is a simplified alternative to fixed sine‑cosine
    encodings and allows the model to learn arbitrary positional patterns.
    """

    def __init__(self, d_model: int, max_len: int = 500):
        super().__init__()
        self.position_embed = nn.Embedding(max_len, d_model)
        self.max_len = max_len

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (batch, seq_len, d_model)
        seq_len = x.size(1)
        if seq_len > self.max_len:
            raise ValueError(f"Sequence length {seq_len} exceeds maximum positional encoding length {self.max_len}")
        positions = torch.arange(seq_len, device=x.device, dtype=torch.long)
        pos_embed = self.position_embed(positions)
        # Broadcast batch dimension
        return x + pos_embed.unsqueeze(0)


class EmotionTransformer(nn.Module):
    """Transformer encoder for EEG emotion recognition.

    The network embeds the input features to a hidden dimension, adds a learnable
    positional encoding, passes the sequence through multiple Transformer
    encoder layers and then averages the output across the time dimension.
    A final linear layer outputs logits for each class.
    """

    def __init__(self, input_dim: int = 4, d_model: int = 128, n_heads: int = 4,
                 num_layers: int = 3, num_classes: int = 4, dim_feedforward: int = 256,
                 dropout: float = 0.1, max_seq_len: int = 60):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, d_model)
        self.pos_encoder = PositionalEncoding(d_model, max_len=max_seq_len)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=n_heads,
                                                   dim_feedforward=dim_feedforward, dropout=dropout,
                                                   batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.classifier = nn.Linear(d_model, num_classes)
        self.d_model = d_model
        self.num_classes = num_classes

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, input_dim)
        x = self.input_proj(x)  # (batch, seq_len, d_model)
        x = self.pos_encoder(x)
        x = self.transformer(x)  # (batch, seq_len, d_model)
        # Mean pooling across sequence
        out = x.mean(dim=1)  # (batch, d_model)
        logits = self.classifier(out)  # (batch, num_classes)
        return logits
