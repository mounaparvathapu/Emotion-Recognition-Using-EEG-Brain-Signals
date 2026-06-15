"""
Utility functions for emotion mapping and evaluation.

This module defines helper functions to map continuous valence and
arousal scores (range 1–9 in the DEAP dataset) to discrete emotion
categories.  It also contains convenience functions for computing
confusion matrices and plotting results.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


EMOTION_LABELS = ['happy', 'sad', 'relaxed', 'stressed']


def map_emotions(valence: np.ndarray, arousal: np.ndarray) -> np.ndarray:
    """Map continuous valence and arousal scores to discrete emotions.

    High valence (>5) and high arousal (>5) → happy.
    High valence (>5) and low arousal (≤5) → relaxed.
    Low valence (≤5) and high arousal (>5) → stressed.
    Low valence (≤5) and low arousal (≤5) → sad.

    Parameters
    ----------
    valence : array-like
        Vector of valence ratings (1–9).
    arousal : array-like
        Vector of arousal ratings (1–9).

    Returns
    -------
    np.ndarray
        Array of discrete emotion labels (strings).
    """
    valence = np.asarray(valence)
    arousal = np.asarray(arousal)
    emotions = []
    for v, a in zip(valence, arousal):
        if v > 5 and a > 5:
            emotions.append('happy')
        elif v > 5 and a <= 5:
            emotions.append('relaxed')
        elif v <= 5 and a > 5:
            emotions.append('stressed')
        else:
            emotions.append('sad')
    return np.array(emotions)


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, labels: list[str] | None = None,
                          save_path: str | None = None) -> None:
    """Plot a confusion matrix using seaborn heatmap.

    Parameters
    ----------
    y_true : np.ndarray
        True class labels.
    y_pred : np.ndarray
        Predicted class labels.
    labels : list of str, optional
        List of class names in order.  If None, unique labels from
        `y_true` will be used.
    save_path : str, optional
        If provided, the figure will be saved to this path.
    """
    if labels is None:
        labels = sorted(np.unique(np.concatenate([y_true, y_pred])))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.close()


def plot_training_curves(history: dict[str, list[float]], save_path: str | None = None) -> None:
    """Plot training loss and accuracy curves.

    Parameters
    ----------
    history : dict
        Dictionary with keys 'loss' and 'accuracy' mapping to lists of
        floats representing loss/accuracy values over epochs.
    save_path : str, optional
        If provided, the figure will be saved to this path.
    """
    epochs = range(1, len(history['loss']) + 1)
    fig, ax1 = plt.subplots(figsize=(7, 5))
    color1 = 'tab:red'
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss', color=color1)
    ax1.plot(epochs, history['loss'], color=color1, label='Loss')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.set_ylabel('Accuracy', color=color2)
    ax2.plot(epochs, history['accuracy'], color=color2, label='Accuracy')
    ax2.tick_params(axis='y', labelcolor=color2)
    fig.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.close()
