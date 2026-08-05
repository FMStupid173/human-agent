from __future__ import annotations

import wave
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public" / "soundbed.wav"
RATE = 44_100
DURATION = 30.0


def add_tone(track: np.ndarray, start: float, duration: float, frequency: float, gain: float) -> None:
    begin = int(start * RATE)
    length = min(int(duration * RATE), len(track) - begin)
    if length <= 0:
        return
    time = np.arange(length) / RATE
    envelope = np.exp(-time * 13.0)
    track[begin : begin + length] += np.sin(2 * np.pi * frequency * time) * envelope * gain


def main() -> None:
    rng = np.random.default_rng(20260805)
    samples = int(RATE * DURATION)
    time = np.arange(samples) / RATE
    track = 0.012 * np.sin(2 * np.pi * 110 * time)
    track += 0.008 * np.sin(2 * np.pi * 165 * time)

    for beat in np.arange(0, DURATION, 0.5):
        add_tone(track, float(beat), 0.18, 68, 0.20)

    for tick in np.arange(0.25, DURATION, 0.5):
        begin = int(tick * RATE)
        length = min(int(0.035 * RATE), samples - begin)
        envelope = np.exp(-np.arange(length) / RATE * 95)
        track[begin : begin + length] += rng.normal(0, 0.055, length) * envelope

    for cut in (0, 2.85, 7.52, 9.58, 16.04, 20.20, 24.56, 27.20):
        add_tone(track, cut, 0.32, 46, 0.34)
        add_tone(track, cut + 0.02, 0.18, 124, 0.15)

    fade = int(0.8 * RATE)
    track[:fade] *= np.linspace(0, 1, fade)
    track[-fade:] *= np.linspace(1, 0, fade)
    peak = float(np.max(np.abs(track))) or 1.0
    pcm = np.int16(np.clip(track / peak * 0.72, -1, 1) * 32767)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUTPUT), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(RATE)
        handle.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
