# 人味 Agent 30-Second Promo v5

Editable Remotion source for the 1080 x 1920 launch video. The v5 cut uses nine compact sections, larger mobile-safe type, burned-in Chinese captions, warm Mandarin narration, and an evolving editorial electronic arrangement aligned to the scene cuts.

```powershell
npm install
npm run render
npm run still
```

Outputs:

- `out/human-agent-30s-v5.mp4`
- `out/human-agent-cover-v5.png`

Narration source and timing live in `narration.zh-CN.txt` and `public/voiceover.srt`. Run `generate-voice.ps1` to regenerate the warm `zh-CN-XiaoxiaoNeural` female voice at its natural rate. `generate-soundbed.py` creates the copyright-safe 92 BPM D-minor BGM used by the composition, with evolving pads, keys, arpeggios, bass, percussion, counter-melody, and scene transitions. `suno-bgm-prompt.md` provides a timing-aware prompt for generating an alternative instrumental in Suno.

The MP4 contains both narration and sound. When posting, keep original audio enabled; platform music should only be added quietly underneath it.
