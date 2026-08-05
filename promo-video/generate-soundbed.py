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
BPM = 92
BEAT = 60.0 / BPM
SCENE_CUTS = (0.0, 3.37, 8.63, 11.60, 17.83, 20.47, 24.20, 26.50, 28.33)


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


def pluck(frequency: float, duration: float = 0.68, velocity: float = 1.0) -> np.ndarray:
    t = np.arange(int(duration * RATE)) / RATE
    wave_body = (
        np.sin(2 * np.pi * frequency * t)
        + 0.24 * np.sin(2 * np.pi * frequency * 2.01 * t)
        + 0.10 * np.sin(2 * np.pi * frequency * 3.98 * t)
    )
    shimmer = 0.035 * np.sin(2 * np.pi * frequency * 6.02 * t)
    return (wave_body + shimmer) * np.exp(-t * 5.4) * 0.060 * velocity


def soft_key(frequency: float, duration: float = 1.15, velocity: float = 1.0) -> np.ndarray:
    t = np.arange(int(duration * RATE)) / RATE
    body = (
        np.sin(2 * np.pi * frequency * t)
        + 0.20 * np.sin(2 * np.pi * frequency * 2.005 * t)
        + 0.07 * np.sin(2 * np.pi * frequency * 3.01 * t)
    )
    attack = np.clip(t / 0.018, 0, 1)
    return body * attack * np.exp(-t * 2.9) * 0.050 * velocity


def counter_note(frequency: float, duration: float = 0.92) -> np.ndarray:
    t = np.arange(int(duration * RATE)) / RATE
    body = np.sin(2 * np.pi * frequency * t) + 0.16 * np.sin(2 * np.pi * frequency * 2.99 * t)
    envelope = np.clip(t / 0.05, 0, 1) * np.exp(-t * 3.4)
    return body * envelope * 0.032


def bass(frequency: float, duration: float = 0.44) -> np.ndarray:
    t = np.arange(int(duration * RATE)) / RATE
    body = np.sin(2 * np.pi * frequency * t) + 0.22 * np.sin(2 * np.pi * frequency * 2 * t)
    return body * np.exp(-t * 4.6) * 0.095


def kick() -> np.ndarray:
    duration = 0.34
    t = np.arange(int(duration * RATE)) / RATE
    phase = 2 * np.pi * (42 * t + 65 * (1 - np.exp(-t * 18)) / 18)
    click = np.exp(-t * 70) * np.sin(2 * np.pi * 1200 * t) * 0.045
    return (np.sin(phase) * np.exp(-t * 10) * 0.31) + click


def snare(rng: np.random.Generator) -> np.ndarray:
    duration = 0.24
    t = np.arange(int(duration * RATE)) / RATE
    noise = rng.normal(0, 1, len(t))
    tone = np.sin(2 * np.pi * 185 * t)
    return (noise * 0.055 + tone * 0.06) * np.exp(-t * 18)


def hat(rng: np.random.Generator, open_hat: bool = False) -> np.ndarray:
    duration = 0.16 if open_hat else 0.055
    t = np.arange(int(duration * RATE)) / RATE
    noise = rng.normal(0, 1, len(t))
    metallic = np.sin(2 * np.pi * 7200 * t) + 0.5 * np.sin(2 * np.pi * 9800 * t)
    return (noise * 0.014 + metallic * 0.006) * np.exp(-t * (18 if open_hat else 72))


def shaker(rng: np.random.Generator) -> np.ndarray:
    duration = 0.085
    t = np.arange(int(duration * RATE)) / RATE
    noise = rng.normal(0, 1, len(t))
    high = np.concatenate(([0.0], np.diff(noise)))
    return high * np.exp(-t * 46) * 0.010


def impact() -> np.ndarray:
    duration = 0.52
    t = np.arange(int(duration * RATE)) / RATE
    low = np.sin(2 * np.pi * (46 + 35 * np.exp(-t * 9)) * t) * np.exp(-t * 7)
    snap = np.sin(2 * np.pi * 420 * t) * np.exp(-t * 24)
    return low * 0.18 + snap * 0.035


def riser(rng: np.random.Generator, duration: float = 0.58) -> np.ndarray:
    t = np.arange(int(duration * RATE)) / RATE
    noise = rng.normal(0, 1, len(t))
    high = np.concatenate(([0.0], np.diff(noise)))
    sweep = np.sin(2 * np.pi * (260 * t + 520 * t * t))
    envelope = np.clip(t / duration, 0, 1) ** 2
    return (high * 0.012 + sweep * 0.018) * envelope


def add_pad(track: np.ndarray, start: float, duration: float, frequencies: tuple[float, ...]) -> None:
    begin, length, t = segment(start, duration, len(track))
    if length <= 0:
        return
    attack = np.clip(t / 0.25, 0, 1)
    release = np.clip((duration - t) / 0.45, 0, 1)
    envelope = attack * release
    left = np.zeros(length)
    right = np.zeros(length)
    drift = 1 + 0.0025 * np.sin(2 * np.pi * 0.11 * t)
    for index, frequency in enumerate(frequencies):
        harmonic = 0.11 * np.sin(2 * np.pi * frequency * 2 * t)
        left += np.sin(2 * np.pi * frequency * t) + harmonic
        right += np.sin(2 * np.pi * frequency * drift * t + index * 0.08) + harmonic
    left *= envelope * 0.025 / len(frequencies)
    right *= envelope * 0.025 / len(frequencies)
    track[begin : begin + length, 0] += left
    track[begin : begin + length, 1] += right


def main() -> None:
    rng = np.random.default_rng(20260805)
    total = int(RATE * DURATION)
    track = np.zeros((total, 2), dtype=np.float64)

    # D minor -> Bb major -> F major -> C major. Each pass gains detail, then clears for the CTA.
    progression = (
        ((146.83, 174.61, 220.00, 261.63), 73.42),
        ((116.54, 146.83, 174.61, 233.08), 58.27),
        ((174.61, 220.00, 261.63, 349.23), 87.31),
        ((130.81, 164.81, 196.00, 261.63), 65.41),
    )
    arp_patterns = (
        (0, 1, 2, 1, 3, 2, 1, 2),
        (0, 2, 1, 3, 2, 1, 3, 2),
        (1, 2, 3, 2, 0, 2, 1, 3),
        (0, 1, 3, 2, 1, 2, 3, 1),
    )
    counter_scale = (293.66, 349.23, 392.00, 440.00, 523.25, 587.33)
    bar = BEAT * 4
    bars = int(np.ceil(DURATION / bar))

    for bar_index in range(bars):
        start = bar_index * bar
        chord, root = progression[bar_index % len(progression)]
        add_pad(track, start, min(bar + 0.18, DURATION - start), chord)

        section = 0 if start < 9.0 else 1 if start < 17.7 else 2 if start < 26.67 else 3
        pattern = arp_patterns[bar_index % len(arp_patterns)]
        step_count = 4 if section == 0 else 8
        for step in range(step_count):
            grid = step * (BEAT if section == 0 else BEAT / 2)
            note_index = pattern[step * (2 if section == 0 else 1)]
            note = chord[note_index] * (2 if section >= 2 and step in {3, 7} else 1)
            velocity = 0.72 + 0.18 * ((step + bar_index) % 3 == 0)
            pan = -0.42 if step % 2 == 0 else 0.42
            source = soft_key(note, velocity=velocity) if section == 0 else pluck(note, velocity=velocity)
            add_mono(track, start + grid, source, pan)

        # Root movement stays simple while a fifth pickup gives later sections momentum.
        add_mono(track, start, bass(root, 0.58), -0.10)
        if section >= 1:
            add_mono(track, start + 2 * BEAT, bass(root, 0.50), 0.08)
            add_mono(track, start + 3.5 * BEAT, bass(root * 1.5, 0.30), 0.14)

        if section == 0:
            add_mono(track, start, kick() * 0.55)
            add_mono(track, start + 2 * BEAT, kick() * 0.42)
        elif section in {1, 2}:
            kick_steps = (0.0, 2.0) if section == 1 else (0.0, 1.5, 2.5)
            for beat_pos in kick_steps:
                add_mono(track, start + beat_pos * BEAT, kick() * (0.72 if section == 1 else 0.82))
            for beat_pos in (1.0, 3.0):
                add_mono(track, start + beat_pos * BEAT, snare(rng) * (0.72 if section == 1 else 0.84), 0.06)
            for step in range(8 if section == 1 else 16):
                grid = BEAT / (2 if section == 1 else 4)
                add_mono(track, start + step * grid, shaker(rng), -0.35 if step % 2 == 0 else 0.35)
            for beat_index in range(4):
                add_mono(track, start + (beat_index + 0.5) * BEAT, hat(rng, beat_index == 3 and section == 2), 0.44)
        else:
            add_mono(track, start, kick() * 0.38)

        if section >= 1 and bar_index % 2 == 0:
            note = counter_scale[(bar_index + 1) % len(counter_scale)]
            add_mono(track, start + 1.5 * BEAT, counter_note(note), -0.24)
            add_mono(track, start + 3.0 * BEAT, counter_note(note * 0.75), 0.26)

    for index, cut in enumerate(SCENE_CUTS):
        if cut > 0.6:
            add_mono(track, cut - 0.58, riser(rng), -0.30 if index % 2 == 0 else 0.30)
        add_mono(track, cut, impact() * (0.72 if index % 3 else 0.92), -0.12 if index % 2 == 0 else 0.12)

    # Let the final line land on a fuller D-minor voicing without adding more percussion.
    add_pad(track, 26.65, DURATION - 26.65, (146.83, 174.61, 220.00, 293.66))
    add_mono(track, 27.18, counter_note(440.00, 1.25), -0.18)
    add_mono(track, 28.45, counter_note(349.23, 1.10), 0.20)

    # Immediate start, then a clean final half-second for the CTA to land.
    intro = int(0.16 * RATE)
    outro = int(0.72 * RATE)
    track[:intro] *= np.linspace(0.35, 1.0, intro)[:, None]
    track[-outro:] *= np.linspace(1.0, 0.0, outro)[:, None]

    track = np.tanh(track * 1.10)
    peak = float(np.max(np.abs(track))) or 1.0
    pcm = np.int16(np.clip(track / peak * 0.82, -1, 1) * 32767)

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
