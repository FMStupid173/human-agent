# 人味 Agent 30-Second Promo v3

Editable Remotion source for the 1080 x 1920 launch video. The v3 cut uses eight fast sections, larger mobile-safe type, burned-in Chinese captions, synthetic Mandarin narration, and an original electronic BGM aligned to the scene cuts.

```powershell
npm install
npm run render
npm run still
```

Outputs:

- `out/human-agent-30s-v3.mp4`
- `out/human-agent-cover-v3.png`

Narration source and timing live in `narration.zh-CN.txt` and `public/voiceover.srt`. Run `generate-voice.ps1` to regenerate the synthetic `zh-CN-XiaoxiaoNeural` voice. `generate-soundbed.py` creates the copyright-safe original BGM used by the composition. `suno-bgm-prompt.md` provides a timing-aware prompt for generating an alternative instrumental in Suno.

The MP4 contains both narration and sound. When posting, keep original audio enabled; platform music should only be added quietly underneath it.
