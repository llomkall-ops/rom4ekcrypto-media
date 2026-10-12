# rom4ekcrypto-media — Instagram content pipeline

This repo hosts images for the Instagram account **@romchekcrypto** (crypto / trading).
Images are public via `https://raw.githubusercontent.com/llomkall-ops/rom4ekcrypto-media/main/<path>`
and are passed by URL to Metricool, which publishes them to Instagram.

Only post images go here. Nothing else.

## Layout
- `posts/YYYY-MM-DD-HHMM-<slug>/slide_N.jpg` — one folder per carousel, JPG, 1080×1350.
- `tools/example_carousel_build.py` — reference implementation of the visual style
  (HTML/CSS rendered with Playwright + Chromium, fonts "Inter Display"/"Inter" which are installed).
  Copy it, change the slide content, keep the CSS, components, cover and CTA slide.
  Run: `python3 tools/example_carousel_build.py <out_dir>`.
- `posts/2026-10-10-btc-ma50w/` — approved reference carousel. Match its look.

## Visual style (approved by the owner)
- Format: Instagram carousel, 4:5, 1080×1350, usually 5–7 slides. Counter "N/total" top-right.
- **Slide 1 (cover):** dark background (#1b1b1b), huge full-width intriguing headline in heavy condensed
  uppercase (Inter Display Black, scaleX .8), white + red (#d03a3e) words; a short subtitle line;
  a candlestick chart (green/red candles, optional blue MA line) in the lower half; a pill tag top-left
  that makes the crypto topic obvious ("₿ Разбор биткоина", "Ξ Эфириум", "Новости крипты" …);
  "@romchekcrypto" bottom-left, "Листай →" bottom-right.
- **Middle slides:** light cream background (#f6f1eb), pill tag top-left ("База 🧠", "История 📜",
  "Шпаргалка ✅", "Сделка 🎯" …), big bold headline black + red, infographic content: cards, timelines,
  tables, checklists, schematic candle charts. End cheat-sheet slides with "Сохрани это."
- **Last slide — ALWAYS:** "ВСТУПАЙ В ТГ-КАНАЛ" CTA with @romchekcrypto and "ССЫЛКА В ПРОФИЛЕ",
  four round icons row, rising candle chart (copy slide 5 from the example as is).
- Charts that are illustrative (not real data) must not show fake price axis numbers.

## Caption format
1. Line 1: post title with emoji (e.g. "📈 Биткоин и 50-недельная средняя")
2. Line 2: intriguing hook/headline question
3. 2–4 short paragraphs with the substance
4. "Листай карусель 👉 …" line
5. "💾 Сохрани…" and "💬 <question to the audience>"
6. "Больше аналитики каждый день — в Telegram @romchekcrypto (ссылка в профиле)"
7. "Не является финансовой рекомендацией."
8. 8–12 Russian/English hashtags (#биткоин #криптовалюта #трейдинг #btc …)

## Content rules
- Topics: crypto market news (BTC, ETH, ETF flows, Fed, regulation, big players) and trading
  education (SMC: order blocks, FVG, liquidity, sessions; risk management; psychology; indicators).
- Every news number must come from a fresh web search (same/previous day) — never invent figures.
- No promises of income or guaranteed results ("те же деньги", "70% дохода" etc. are not allowed).
- Russian language, energetic but credible tone.

## Metricool
- Brand (blogId) 7337792, Instagram @romchekcrypto, timezone Europe/Moscow.
- Schedule with createScheduledPost: providers [{"network":"instagram"}], instagramData {"type":"POST"},
  autoPublish true, media = list of raw.githubusercontent URLs in slide order.

## Reels (added 2026-10-12)
- Every carousel also becomes an Instagram Reel, published 2 hours after the carousel (10:00 → 12:00, 18:00 → 20:00).
- Build (2 steps):
  1. Animated cover (hook) with the SAME text as carousel slide 1:
     `python3 tools/make_hook.py <scratch>/cover.mp4 --tag "<slide-1 tag>" --l1 "<white line>" --l2 "<red line>" --sub "<subtitle / intriguing question>" --trend down|up`
     (trend = direction of the topic: down for falls/outflows/risks, up for growth). Look at frames 0 s and 3.5 s.
  2. `python3 tools/make_reel.py posts/<folder> videos/<folder>.mp4 "3.2,4.5" <scratch>/cover.mp4`
     — the animated cover replaces slide 1, other slides 4.5 s each (~25–30 s total, silent MP4). Commit/push the MP4.
- Schedule with createScheduledPost: media = [raw URL of the MP4], instagramData
  {"type":"REEL","showReelOnFeed":true,"audioConfiguration":{"audioId":"<id>","audioVolume":25,"videoVolume":100}}.
- Background music = calm instrumental tracks from the Instagram catalog, rotate in this order
  (pick the next one after the most recently used; check recent scheduled Reels):
  1. 2477944699150252 — Peaceful Piano (Dr. Pheel)
  2. 2697378737086947 — Floods (Trout Recording)
  3. 1704551184273568 — Waves (Instrumental) (Giulio Cercato)
  4. 5513486825393122 — Hidden Beneath (Sam Marshall)
  5. 976299230340697 — Someday (Instrumental) (Cy Curnin)
  6. 592271352837708 — Beautiful (Giulio Cercato)
  If an audioId is rejected, use the next one in the list.
- Reel caption: shorter — title line, hook, 1–2 sentences, "Полный разбор — в карусели в профиле 👆",
  Telegram @romchekcrypto line, "Не является финансовой рекомендацией.", 5–8 hashtags.

## YouTube Shorts (added 2026-10-12)
- The same video as each Reel is also published as a YouTube Short at the same time (12:00 and 20:00), WITH music.
- Music lives in the PRIVATE repo llomkall-ops/rom4ekcrypto-assets (music/*.mp3, rotation order in its README).
  Never copy the mp3 files into this public repo.
- Build: `python3 tools/add_music.py videos/<folder>.mp4 <assets>/music/<track>.mp3 shorts/<folder>.mp4`, commit/push the MP4.
- Schedule with createScheduledPost: providers [{"network":"youtube"}], media = [raw URL of shorts/<folder>.mp4],
  youtubeData {"title": "<≤90 chars, intriguing, Russian, end with #shorts>", "type":"short", "privacy":"public",
  "madeForKids": false, "category":"EDUCATION", "tags":["криптовалюта","биткоин","трейдинг","crypto","bitcoin"]}.
- Description (text): 2–3 sentences, "Полный разбор и аналитика каждый день — Telegram @romchekcrypto",
  "Instagram: @romchekcrypto", "Не является финансовой рекомендацией.",
  "Музыка: <Title> — <Artist> (YouTube Audio Library)", 3–5 hashtags incl. #shorts.
