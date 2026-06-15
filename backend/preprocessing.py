"""
Preprocessing functions for EEG data.

Includes band‑pass filtering and basic independent component analysis (ICA)
using scikit‑learn.  These functions operate on NumPy arrays representing
segments of EEG data.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.decomposition import FastICA


def butter_bandpass(lowcut: float, highcut: float, fs: float, order: int = 5):
    """Design a Butterworth band‑pass filter.

    Returns the filter coefficients (b, a).
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def bandpass_filter(data: np.ndarray, lowcut: float = 4.0, highcut: float = 45.0,
                    fs: float = 128.0, order: int = 5) -> np.ndarray:
    """Apply a Butterworth band‑pass filter to EEG data.

    Parameters
    ----------
    data : np.ndarray
        EEG data of shape (trials, channels, samples) or (channels, samples).
    lowcut : float
        Lower cutoff frequency in Hz.
    highcut : float
        Upper cutoff frequency in Hz.
    fs : float
        Sampling frequency in Hz.
    order : int
        Order of the Butterworth filter.

    Returns
    -------
    np.ndarray
        Filtered data with the same shape as the input.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    if data.ndim == 3:
        # Iterate over trials and channels
        filtered = np.empty_like(data)
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                filtered[i, j] = filtfilt(b, a, data[i, j])
        return filtered
    elif data.ndim == 2:
        filtered = np.empty_like(data)
        for j in range(data.shape[0]):
            filtered[j] = filtfilt(b, a, data[j])
        return filtered
    else:
        raise ValueError(f"Unsupported data shape: {data.shape}")


def apply_fastica(data: np.ndarray, n_components: int | None = None, random_state: int = 0) -> np.ndarray:
    """Apply FastICA to EEG data along the channel dimension.

    This is a simplified ICA implementation using scikit‑learn.  ICA decomposes
    multichannel signals into statistically independent sources.  For practical
    artefact removal one would inspect and remove components corresponding
    to eye blinks or muscle activity.  Here we reconstruct the signal from
    all components, which may still whiten the data and reduce correlations.

    Parameters
    ----------
    data : np.ndarray
        EEG data of shape (trials, channels, samples) or (channels, samples).
    n_components : int, optional
        Number of independent components.  If None, all channels are used.
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    np.ndarray
        The reconstructed data with the same shape as the input.
    """
    def ica_single(x: np.ndarray) -> np.ndarray:
        """Apply ICA to a single trial (channels × samples)."""
        ica = FastICA(n_components=n_components, random_state=random_state)
        sources = ica.fit_transform(x.T)  # shape: (samples, components)
        reconstructed = ica.inverse_transform(sources).T
        return reconstructed

    if data.ndim == 3:
        cleaned = np.empty_like(data)
        for i in range(data.shape[0]):
            cleaned[i] = ica_single(data[i])
        return cleaned
    elif data.ndim == 2:
        return ica_single(data)
    else:
        raise ValueError(f"Unsupported data shape: {data.shape}")
