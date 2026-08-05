# 人味 Agent 30-Second Promo v2

Editable Remotion source for the 1080 x 1920 launch video. The v2 cut uses eight fast sections, burned-in Chinese captions, synthetic Mandarin narration, and a low-volume procedural sound bed.

```powershell
npm install
npm run render
npm run still
```

Outputs:

- `out/human-agent-30s-v2.mp4`
- `out/human-agent-cover-v2.png`

Narration source and timing live in `narration.zh-CN.txt` and `public/voiceover.srt`. Run `generate-voice.ps1` to regenerate the synthetic `zh-CN-XiaoxiaoNeural` voice. `generate-soundbed.py` creates the copyright-safe procedural bed used by the composition.

The MP4 contains both narration and sound. When posting, keep original audio enabled; platform music should only be added quietly underneath it.
