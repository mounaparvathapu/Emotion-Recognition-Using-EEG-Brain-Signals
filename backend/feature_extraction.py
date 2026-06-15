"""
Feature extraction for EEG emotion recognition.

This module defines functions to compute power spectral density (PSD) and band‑power
features from EEG data.  The signals are segmented into 1‑second epochs and the
PSD is estimated using Welch’s method.  The band‑power for each epoch and
channel is integrated over canonical frequency bands (theta, alpha, beta,
gamma), producing a feature vector per epoch.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import welch
from typing import List, Tuple, Dict


DEFAULT_BANDS: List[Tuple[str, float, float]] = [
    ('theta', 4.0, 8.0),
    ('alpha', 8.0, 13.0),
    ('beta', 13.0, 30.0),
    ('gamma', 30.0, 45.0),
]


def compute_psd(epoch: np.ndarray, fs: float = 128.0, nperseg: int | None = None) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the power spectral density of a 1‑D signal using Welch’s method.

    Parameters
    ----------
    epoch : np.ndarray
        1‑D array of shape (samples,) representing a single epoch from one channel.
    fs : float
        Sampling frequency in Hz.
    nperseg : int, optional
        Length of each segment for Welch’s method.  Defaults to half the epoch length.

    Returns
    -------
    freqs : np.ndarray
        Array of sample frequencies.
    psd : np.ndarray
        Power spectral density of the input signal.
    """
    if nperseg is None:
        nperseg = len(epoch) // 2
    freqs, psd = welch(epoch, fs=fs, nperseg=nperseg)
    return freqs, psd


def bandpower(freqs: np.ndarray, psd: np.ndarray, bands: List[Tuple[str, float, float]]) -> Dict[str, float]:
    """Integrate power spectral density within given frequency bands.

    Parameters
    ----------
    freqs : np.ndarray
        Frequency bins returned by Welch’s method.
    psd : np.ndarray
        Power spectral density values corresponding to `freqs`.
    bands : list of tuples
        Each tuple contains (name, f_low, f_high) defining a frequency band.

    Returns
    -------
    dict
        Dictionary mapping band name to integrated power.
    """
    bp = {}
    for name, f_low, f_high in bands:
        idx = np.logical_and(freqs >= f_low, freqs < f_high)
        bp[name] = np.trapz(psd[idx], freqs[idx])
    return bp


def extract_features(data: np.ndarray, fs: float = 128.0, epoch_length: float = 1.0,
                     bands: List[Tuple[str, float, float]] | None = None,
                     aggregate: bool = True) -> Tuple[np.ndarray, int]:
    """Extract band‑power features from raw EEG data.

    Parameters
    ----------
    data : np.ndarray
        EEG data of shape (trials, channels, samples).
    fs : float
        Sampling frequency in Hz.
    epoch_length : float
        Length of each epoch in seconds.  The number of samples per epoch is
        `int(fs * epoch_length)`.
    bands : list of tuples, optional
        Frequency bands to integrate.  If None, ``DEFAULT_BANDS`` is used.
    aggregate : bool, default True
        If True, band‑power is averaged across channels for each band,
        yielding a feature vector of length equal to the number of bands.
        If False, band‑power values from each channel are concatenated,
        yielding a feature vector of length ``n_channels * n_bands``.

    Returns
    -------
    features : np.ndarray
        2‑D array of shape (N_epochs, n_features) containing features.
    epoch_samples : int
        Number of samples per epoch.
    """
    if bands is None:
        bands = DEFAULT_BANDS
    n_trials, n_channels, n_samples = data.shape
    epoch_samples = int(fs * epoch_length)
    n_epochs_per_trial = n_samples // epoch_samples
    features_list = []
    for trial in range(n_trials):
        for e in range(n_epochs_per_trial):
            start = e * epoch_samples
            end = start + epoch_samples
            feat_per_channel = []
            for ch in range(n_channels):
                epoch = data[trial, ch, start:end]
                freqs, psd = compute_psd(epoch, fs=fs)
                bp = bandpower(freqs, psd, bands)
                # preserve order of bands
                feat_per_channel.append([bp[name] for name, _, _ in bands])
            feat_per_channel = np.array(feat_per_channel)  # shape (channels, n_bands)
            if aggregate:
                # mean across channels
                feat = feat_per_channel.mean(axis=0)
            else:
                feat = feat_per_channel.flatten()
            features_list.append(feat)
    features = np.vstack(features_list)
    return features, epoch_samples
