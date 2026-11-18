# Reels format — motion-graphics infographic reels (owner's references, 2026-11-18)

STATUS: not started. Do NOT make or schedule Reels until the owner says so.

## Standard outro (2026-11-18, v4 — LIME accent on dark, owner's pick)
- Owner finds red off-putting: reels use accent LIME #c6f432 on dark #141414 (text on lime chips = #161616);
  red stays only for falling candles. Carousels keep their current colors until the owner decides.
- `reels/outro/romchek_outro.mp4` (13.3 s, 1080×1920, voice + subtitles + SFX, NO music — the reel's music runs under it
  at final assembly so it stays continuous). Source: `reels/outro/outro.html` (window.render(t)), frames via
  `tools/render_frames.py`, voice = ElevenLabs "romchek", text: «Хочешь научиться торговать или усилить свои навыки? Напиши в комментариях
  слово „обучение“ — и я пришлю тебе 13 авторских видеоуроков по трейдингу и добавлю в чат сообщества.»
- Append it to the end of EVERY reel.
- Getting ElevenLabs audio out: container and Mac shell can't reach elevenlabsusercontent.com; working path =
  open the content_url in the built-in browser on the owner's Mac, fetch → blob → <a download> into ~/Downloads,
  then device_stage_files.

## Owner's decisions
- Topic: crypto / trading only. Vertical 1080×1920, ~15–45 s.
- Voiceover: owner's ElevenLabs voice clone "romchek" (voice_id dePhkRzAG2xmWcT92bn3) via the ElevenLabs connector.
- Background music mixed into the video file (generate royalty-free via ElevenLabs Music, or another free source).
- SFX: owner's own set in ~/Movies/SFX (whoosh, riser, impact, pop, ding) — quiet, never startling,
  only on purpose: card/plaque appears, info changes, swipe/transition. Not every second.
- Subtitles always.

## What the 4 reference reels have in common
1. **Hook = the first frame is already infographic**: huge bold headline (2 lines, 2 colors) + one UI card that
   shows the result/claim immediately ("2,300,000 views", "$16/мес", "BOING! WHOOSH!").
2. **Kinetic typography synced to the voice**: each phrase appears word-by-word, the key word highlighted
   (colored, boxed, underlined). Text changes every 1–2 s.
3. **Animated UI mockups instead of footage**: app windows, timelines, waveforms, counters, charts, gauges,
   progress bars, checklists, search boxes ("0 matches"), terminal lines. Everything moves (counters tick,
   bars fill, cards slide/scale, blur transitions between scenes).
4. **Numbered structure**: "3 things → #1 / #2 / #3" with a sticky header showing the current item, or locked
   cards 01/02/03 that unlock one by one. Progress dots/■■□ show where the viewer is.
5. **Contrast devices**: before/after, NO MATCH → found, easy vs hard gauge, cost ($22) vs free.
6. **Mascot / character** (pixel creature, robot) reacting in a corner — adds personality, recurring brand element.
7. **Ending CTA**: "Подпишись!" with mascot, or "Comment 'слово' — пришлю гайд" (comment-trigger → DMs).
8. Palettes seen: dark + neon lime; dark green-teal; pastel gradient (cream/lilac/peach) + black text + orange/red accent.
   For @romchekcrypto use our brand: cream or dark #1b1b1b, red #d03a3e accent, green/red candles.

## Crypto adaptations (ideas)
- "3 бесплатных инструмента трейдера": #1 CoinGlass (liquidation heatmap), #2 TradingView, #3 Farside (ETF flows).
- "Ликвидации за 30 секунд": candle pierces a level, longs "burn", $ counter ticks up.
- "Имбаланс / ордерблок в движении": 3 candles build up, gap highlights, price returns to the zone.
- "Ошибка, которая сливает депозит": before/after with risk gauge.
