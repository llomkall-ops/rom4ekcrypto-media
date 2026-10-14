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

## Reels — ⏸ PAUSED by the owner on 2026-10-13 (do not schedule Instagram Reels until he re-enables). Format (added 2026-10-12) APPROVED by the owner: animated cover + slides 2..N at 4.5 s; base for all Reels and Shorts
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
  Never copy the plain mp3 files into this public repo.
- BACKUP (use whenever the private repo can't be attached/cloned): the same 3 tracks are stored ENCRYPTED in this repo
  as music_enc/<track>.mp3.enc (AES-256-CBC, pbkdf2). The passphrase is given ONLY in the scheduled-task prompt —
  never write it into this repo. Decrypt to scratch (not into the repo):
  `openssl enc -d -aes-256-cbc -pbkdf2 -in music_enc/<track>.mp3.enc -out <scratch>/<track>.mp3 -pass pass:<KEY>`.
  Rotation and credits are the same as in the private repo README:
  1. 01_Lofi_Mallet-Kwon — "Lofi Mallet" — Kwon; 2. 02_Glass_Chinchilla-The_Mini_Vandals — "Glass Chinchilla" — The Mini Vandals;
  3. 03_Chilltronic-RKVC — "Chilltronic" — RKVC.
- A Short WITHOUT music is a failure: verify with ffprobe that shorts/<folder>.mp4 has an audio stream before scheduling.
- Build: `python3 tools/add_music.py videos/<folder>.mp4 <assets>/music/<track>.mp3 shorts/<folder>.mp4`, commit/push the MP4.
- Schedule with createScheduledPost: providers [{"network":"youtube"}], media = [raw URL of shorts/<folder>.mp4],
  youtubeData {"title": "<≤90 chars, intriguing, Russian, contains a key word like «биткоин», ends with #shorts>",
  "type":"short", "privacy":"public", "madeForKids": false, "category":"EDUCATION", "tags": [...]}.
- TAGS (owner's requirement — fill the YouTube tags field COMPLETELY every time, up to YouTube's 500-character limit).
  Count length the YouTube way: tags joined by commas, and every tag that contains a space counts +2 (quotes).
  Build the list in this order and stop adding when the next tag would exceed 500:
  1) MUST tags (always): биткоин, обзор биткоина, альтсезон, трейдинг, обучение трейдингу, криптовалюта, bitcoin
  2) 3–5 topic-specific tags for this video (coins/events/terms: эфириум, ETF, ФРС, инфляция США, ордер блок,
     ликвидность, smart money, технический анализ, альткоины …)
  3) Owner's base pool of popular tags, in this priority order (replace 2026 with the current year when it changes):
     биткоин прогноз, биткоин сегодня, биткоин новости, когда альтсезон, альткоины, биткоин цена, биткоин обзор,
     биткоин когда рост, биткоин когда покупать, биткоин когда продавать, bitcoin прогноз, биткоин прогноз 2026,
     биткоин 2026, криптовалюта 2026, альткоины 2026, альткоины сегодня, альткоины новости, альткоины для иксов,
     альткоины на долгосрок, биткоин прямо сейчас, биткоин криптовалюта, криптовалюта bitcoin
  Never add other channels' or people's names as tags (YouTube treats that as misleading metadata). No duplicates.
- Description (text): 2–3 sentences on the topic that naturally include the key words «биткоин», «обзор биткоина»
  and «альтсезон» where it makes sense; then "Полный разбор и аналитика каждый день — Telegram @romchekcrypto",
  "Instagram: @romchekcrypto", "Не является финансовой рекомендацией.",
  "Музыка: <Title> — <Artist> (YouTube Audio Library)";
  last line = hashtags, MAXIMUM 3–5 in total (owner's rule — don't overdo it): #shorts #биткоин #альтсезон
  + at most 2 topic hashtags (e.g. #обзорбиткоина, #эфириум, #трейдинг).
- Instagram Reels and carousels: also always include #биткоин #обзорбиткоина #альтсезон among their hashtags.

## TikTok carousels — ⏸ PAUSED by the owner on 2026-10-14 (do not schedule anything on TikTok until he re-enables). Format (added 2026-10-12):
- TikTok account @romchekcrypto is connected in the same Metricool brand. Every carousel is ALSO published to TikTok
  as a photo carousel at the same time as on Instagram (10:00 and 18:00), same slide JPGs in the same order.
- Separate createScheduledPost call: providers [{"network":"tiktok"}], media = same raw slide URLs,
  tiktokData {"title": "<≤90 chars, the intriguing headline>", "autoAddMusic": true, "privacyOption": "PUBLIC_TO_EVERYONE",
  "photoCoverIndex": 0, "disableComment": false}, autoPublish true, draft false.
- TikTok caption (text): title line, hook, 1–3 short sentences, "Больше аналитики — Telegram @romchekcrypto",
  "Не является финансовой рекомендацией.", then 3–5 hashtags (#биткоин #альтсезон #криптовалюта + 1–2 by topic).
