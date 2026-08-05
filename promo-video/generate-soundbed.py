from __future__ import annotations

import subprocess
import wave
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
WAV_OUTPUT = PUBLIC / "soundbed.wav"
MP3_OUTPUT = PUBLIC / "soundbed.mp3"
FFMPEG = ROOT / "node_modules" / "@remotion" / "compositor-win32-x64-msvc" / "ffmpeg.exe"
RATE = 48_000
DURATION = 30.0
BPM = 112
BEAT = 60.0 / BPM
SCENE_CUTS = (0.0, 2.87, 7.53, 9.57, 16.03, 20.33, 24.17, 27.20)


def segment(start: float, duration: float, total: int) -> tuple[int, int, np.ndarray]:
    begin = max(0, int(start * RATE))
    length = min(int(duration * RATE), total - begin)
    return begin, length, np.arange(max(0, length), dtype=np.float64) / RATE


def pan_gains(pan: float) -> tuple[float, float]:
    angle = (np.clip(pan, -1.0, 1.0) + 1.0) * np.pi / 4
    return float(np.cos(angle)), float(np.sin(angle))


def add_mono(track: np.ndarray, start: float, sound: np.ndarray, pan: float = 0.0) -> None:
    begin = max(0, int(start * RATE))
    length = min(len(sound), len(track) - begin)
    if length <= 0:
        return
    left, right = pan_gains(pan)
    track[begin : begin + length, 0] += sound[:length] * left
    track[begin : begin + length, 1] += sound[:length] * right


def pluck(frequency: float, duration: float = 0.42) -> np.ndarray:
    t = np.arange(int(duration * RATE)) / RATE
    wave_body = (
        np.sin(2 * np.pi * frequency * t)
        + 0.35 * np.sin(2 * np.pi * frequency * 2 * t)
        + 0.16 * np.sin(2 * np.pi * frequency * 3 * t)
    )
    return wave_body * np.exp(-t * 8.5) * 0.10


def bass(frequency: float, duration: float = 0.44) -> np.ndarray:
    t = np.arange(int(duration * RATE)) / RATE
    body = np.sin(2 * np.pi * frequency * t) + 0.22 * np.sin(2 * np.pi * frequency * 2 * t)
    return body * np.exp(-t * 5.2) * 0.13


def kick() -> np.ndarray:
    duration = 0.34
    t = np.arange(int(duration * RATE)) / RATE
    phase = 2 * np.pi * (42 * t + 65 * (1 - np.exp(-t * 18)) / 18)
    click = np.exp(-t * 70) * np.sin(2 * np.pi * 1500 * t) * 0.10
    return (np.sin(phase) * np.exp(-t * 11) * 0.52) + click


def snare(rng: np.random.Generator) -> np.ndarray:
    duration = 0.24
    t = np.arange(int(duration * RATE)) / RATE
    noise = rng.normal(0, 1, len(t))
    tone = np.sin(2 * np.pi * 185 * t)
    return (noise * 0.13 + tone * 0.09) * np.exp(-t * 16)


def hat(rng: np.random.Generator, open_hat: bool = False) -> np.ndarray:
    duration = 0.16 if open_hat else 0.055
    t = np.arange(int(duration * RATE)) / RATE
    noise = rng.normal(0, 1, len(t))
    metallic = np.sin(2 * np.pi * 7200 * t) + 0.5 * np.sin(2 * np.pi * 9800 * t)
    return (noise * 0.026 + metallic * 0.012) * np.exp(-t * (18 if open_hat else 72))


def impact() -> np.ndarray:
    duration = 0.52
    t = np.arange(int(duration * RATE)) / RATE
    low = np.sin(2 * np.pi * (46 + 35 * np.exp(-t * 9)) * t) * np.exp(-t * 7)
    snap = np.sin(2 * np.pi * 420 * t) * np.exp(-t * 24)
    return low * 0.28 + snap * 0.06


def add_pad(track: np.ndarray, start: float, duration: float, frequencies: tuple[float, ...]) -> None:
    begin, length, t = segment(start, duration, len(track))
    if length <= 0:
        return
    attack = np.clip(t / 0.25, 0, 1)
    release = np.clip((duration - t) / 0.45, 0, 1)
    envelope = attack * release
    pad = np.zeros(length)
    for frequency in frequencies:
        pad += np.sin(2 * np.pi * frequency * t) + 0.12 * np.sin(2 * np.pi * frequency * 2 * t)
    pad *= envelope * 0.018 / len(frequencies)
    track[begin : begin + length, 0] += pad * 0.96
    track[begin : begin + length, 1] += pad * 1.04


def main() -> None:
    rng = np.random.default_rng(20260805)
    total = int(RATE * DURATION)
    track = np.zeros((total, 2), dtype=np.float64)

    # C minor -> Ab major -> Eb major -> Bb major. The harmony stays below the voice.
    progression = (
        ((130.81, 155.56, 196.00), 65.41),
        ((103.83, 130.81, 155.56), 51.91),
        ((155.56, 196.00, 233.08), 77.78),
        ((116.54, 146.83, 174.61), 58.27),
    )
    bar = BEAT * 4
    bars = int(np.ceil(DURATION / bar))

    for bar_index in range(bars):
        start = bar_index * bar
        chord, root = progression[bar_index % len(progression)]
        add_pad(track, start, min(bar + 0.18, DURATION - start), chord)

        for step in range(8):
            note = chord[(step + bar_index) % len(chord)] * (2 if step in {3, 7} else 1)
            pan = -0.38 if step % 2 == 0 else 0.38
            add_mono(track, start + step * BEAT / 2, pluck(note), pan)

        for beat_index in range(4):
            beat_start = start + beat_index * BEAT
            add_mono(track, beat_start, bass(root), -0.08)
            add_mono(track, beat_start, kick())
            if beat_index in {1, 3}:
                add_mono(track, beat_start, snare(rng), 0.05)
            add_mono(track, beat_start, hat(rng), -0.45)
            add_mono(track, beat_start + BEAT / 2, hat(rng, beat_index == 3), 0.45)

    for index, cut in enumerate(SCENE_CUTS):
        add_mono(track, cut, impact(), -0.12 if index % 2 == 0 else 0.12)

    # Immediate start, then a clean final half-second for the CTA to land.
    intro = int(0.16 * RATE)
    outro = int(0.72 * RATE)
    track[:intro] *= np.linspace(0.35, 1.0, intro)[:, None]
    track[-outro:] *= np.linspace(1.0, 0.0, outro)[:, None]

    track = np.tanh(track * 1.32)
    peak = float(np.max(np.abs(track))) or 1.0
    pcm = np.int16(np.clip(track / peak * 0.86, -1, 1) * 32767)

    PUBLIC.mkdir(parents=True, exist_ok=True)
    with wave.open(str(WAV_OUTPUT), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(RATE)
        handle.writeframes(pcm.tobytes())

    if not FFMPEG.is_file():
        raise FileNotFoundError(f"Remotion ffmpeg not found: {FFMPEG}")
    subprocess.run(
        [
            str(FFMPEG),
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(WAV_OUTPUT),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(MP3_OUTPUT),
        ],
        check=True,
    )
    WAV_OUTPUT.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
