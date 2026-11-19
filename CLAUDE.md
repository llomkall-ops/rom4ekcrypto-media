# rom4ekcrypto-media — Instagram content pipeline

This repo hosts images for the Instagram account **@romchekcrypto** (crypto / trading).
The Telegram channel is called **«РОМЧЕК И КРИПТА»** (link @romchekcrypto) — never write «Ромчик Крипто» as the channel name.
Images are public via `https://raw.githubusercontent.com/llomkall-ops/rom4ekcrypto-media/main/<path>`
and are passed by URL to Metricool, which publishes them to Instagram.

Only post images go here (plus the growth notes in `growth/`). Nothing else.

**Before making any post, read `growth/PLAYBOOK.md` and apply its "Current rules" — they override the older
caption/hashtag rules below where they conflict.**

## Layout
- `posts/YYYY-MM-DD-HHMM-<slug>/slide_N.jpg` — one folder per carousel, JPG, 1080×1350.
- `tools/example_carousel_build.py` — reference implementation of the visual style
  (HTML/CSS rendered with Playwright + Chromium, fonts "Inter Display"/"Inter" which are installed).
  Copy it, change the slide content, keep the CSS, components, cover and CTA slide.
  Run: `python3 tools/example_carousel_build.py <out_dir>`.
- `posts/2026-10-10-btc-ma50w/` — approved reference carousel. Match its look.

## Schedule (owner's rule since 2026-11-18 evening: 1 carousel + 1 reel per day)
- Published automatically (no review by the owner):
  - **10:00 MSK** — crypto market news digest CAROUSEL (folder `posts/YYYY-MM-DD-1000-<slug>`).
  - **18:00 MSK** — trading education REEL (see «Educational Reels» below; video `videos/YYYY-MM-DD-1800-<slug>.mp4`,
    sources `reels/lessons/YYYY-MM-DD-<slug>/`): imbalance/FVG, gaps, order blocks, trend break (BOS/CHoCH),
    support/resistance, breakouts, liquidity, liquidation maps, RSI and other indicators, risk management, psychology…
    Before choosing a topic list `reels/lessons/*`, `posts/*-1800-*` and `posts/*-1900-*`; don't repeat a topic from the last 30 days.
- Before scheduling, check getScheduledPosts for that slot so a post is never scheduled twice.

## Educational Reels — 18:00 (APPROVED by the owner 2026-11-18; reference: reels/lessons/2026-11-18-liquidity-hunt)
- **LENGTH: the whole reel MUST be longer than 1 minute** (owner's rule — such reels get more views): lesson voice
  ~50–55 s (~120–135 words) + standard outro 13.3 s ≈ 63–70 s. make_edu_reel.py warns if < 61 s — then extend the script.
- Motion infographics (lime #c6f432 on dark #141414, red #e5484d only for negative), 1080×1920, 30 fps, everything inside
  the safe zone (x 60–1010, headline from y≈360, subtitles at y≈1385). Word-by-word subtitles (current word on lime). Copy
  `reels/lessons/2026-11-18-liquidity-hunt/page.html`, keep the engine (W, GROUPS, I/T/E, show, candles, line, subtitles),
  rewrite the scenes. T('word') / T('two words', occurrence) finds the time of a spoken word.
- Script structure: 1) hook = pain of the viewer in 1 sentence (+ «Знакомо?»); 2) the twist/name of the concept;
  3) how it works on a candle schematic (animated); 4) consequence for the viewer; 5) «Как защититься / Как использовать?»
  with 3 numbered tips (#1/#2/#3 header with progress dots), each with its own animated schematic; 6) «Сохрани… и перешли
  другу, который…». Then the standard outro (appended automatically: «напиши „обучение“ — 13 видеоуроков + чат»).
  No promises of income, no invented experience/results of Ромчик, schematic charts have no price numbers.
- Voice: ElevenLabs creative_generate_speech, model eleven_v4, voice_id dePhkRzAG2xmWcT92bn3 («romchek»),
  generations_count 1, prompt starts with «[confident, energetic] ». Then creative_transcribe_audio (eleven_scribe_v1,
  connect_from = the speech node, same flow). Download content_url (voice.mp3) and words_download_url (words.json) with curl
  (elevenlabsusercontent.com is allowed). Never re-run a generation to "retry" — it charges again.
- SFX: reels/sfx/* (owner's sounds) — quiet (volume 0.08–0.15), only at scene changes and when a plaque/marker appears
  (whoosh/swipe on scene change, pop on plaques, ding on ✓, impact_short on «стоп»/key number). Music: reels/music/edu_bg_01.mp3
  (looped, −18 dB under voice) — added by the script.
- Build: put page.html, voice.mp3, words.json, phrases.json (subtitle groups 1–4 words, covering every word in order),
  sfx.json ([[t, "pop/pop_soft", 0.14], …], t = word start + 0.25) into reels/lessons/<date>-<slug>/; check stills with
  `python3 tools/make_edu_reel.py <dir> x --stills 1.0,5.0,…` (Read them! fix overflowing/overlapping text), then
  `python3 tools/make_edu_reel.py <dir> videos/<date>-1800-<slug>.mp4`. Commit + push (not the _build folder).
- Schedule: createScheduledPost, providers [{"network":"instagram"}], instagramData {"type":"REEL","showReelOnFeed":true},
  media = [raw URL of the mp4], autoPublish true. NO audioConfiguration (music is inside the video).
- **YouTube Short (owner's rule 2026-11-18): the SAME mp4 is also published as a YouTube Short at the same time (18:00).**
  Separate createScheduledPost: providers [{"network":"youtube"}], media = [same raw mp4 URL], youtubeData {"title": "<CAPS hook
  word(s) + topic, ≤90 chars, ends with #shorts>", "type":"short", "privacy":"public", "madeForKids":false, "category":"PEOPLE_BLOGS",
  "tags":[…filled to 500 chars by the TAGS rule in the «YouTube Shorts» section below: MUST tags + 3–5 topic tags + base pool…]}.
  Description: 2–3 SEO sentences with «биткоин», «обзор биткоина», «альтсезон»; «Напиши в комментариях «обучение» — пришлю
  13 авторских видеоуроков по трейдингу и добавлю в чат сообщества.»; «Полный разбор и аналитика каждый день — Telegram
  @romchekcrypto»; «Instagram: @romchekcrypto»; «Не является финансовой рекомендацией.»; last line 3 hashtags
  (#shorts #трейдинг + 1 topic, see PLAYBOOK). No «Музыка:» line (music is our own ElevenLabs track). Check getScheduledPosts so
  the Short is not scheduled twice.
- **Titles/captions/hashtags/keywords: follow growth/PLAYBOOK.md «Titles, captions, hashtags, keywords» (overrides the lines
  below): one primary keyword first in title/caption + on screen + in voice; short caption, never retell the script;
  Instagram 3–5 hashtags; YouTube title 40–70 chars without hashtags, description 2–3 sentences + 3 hashtags.**
- Reel caption: title line with emoji + keywords, hook, 2 short paragraphs, «💾 Сохрани…», «📤 Перешли другу, который…»,
  «💬 Напиши «обучение» — пришлю 13 авторских видеоуроков по трейдингу и добавлю в чат сообщества», «Подписывайся…»,
  Telegram line, «Не является финансовой рекомендацией.», max 5 hashtags (#биткоин #альтсезон #трейдинг + 1–2 topic; NO #обзорбиткоина in education reels — owner 2026-11-18).

## Visual style (approved by the owner; accent changed to LIME on 2026-11-18 — owner finds red off-putting)
- ACCENT COLORS: dark slides → lime #c6f432 for accent words/numbers; cream slides → NO green text (owner dislikes it):
  accent words are black #141414 with a lime MARKER highlight under them (class `.red` in the reference builder),
  lime #c6f432 plaques/labels/highlights (text on lime = #141414). Red #c62a2f ONLY for negative
  meaning (falling candles, losses, "ошибка", "стоп", "не делай так") — class `.neg` in the reference builder.
- Format: Instagram carousel, 4:5, 1080×1350, usually 5–7 slides. Counter "N/total" top-right.
- **Slide 1 (cover):** dark background (#1b1b1b), huge full-width intriguing headline in heavy condensed
  uppercase (Inter Display Black, scaleX .8), white + lime (#c6f432) words; a short subtitle line;
  a candlestick chart (green/red candles, optional blue MA line) in the lower half; a pill tag top-left
  that makes the crypto topic obvious ("₿ Разбор биткоина", "Ξ Эфириум", "Новости крипты" …);
  "@romchekcrypto" bottom-left, "Листай →" bottom-right.
- **Middle slides:** light cream background (#f6f1eb), pill tag top-left ("База 🧠", "История 📜",
  "Шпаргалка ✅", "Сделка 🎯" …), big bold black headline with lime marker highlight on the key words, infographic content: cards, timelines,
  tables, checklists, schematic candle charts. End cheat-sheet slides with "Сохрани это."
- **Last slide — ALWAYS:** "ВСТУПАЙ В ТГ-КАНАЛ" CTA with @romchekcrypto and "ССЫЛКА В ПРОФИЛЕ",
  four round icons row, rising candle chart (copy slide 5 from the example as is).
- Charts that are illustrative (not real data) must not show fake price axis numbers.

## Caption format
1. Line 1: post title with emoji (e.g. "📈 Биткоин и 50-недельная средняя")
2. Line 2: intriguing hook/headline question
3. 2–4 short paragraphs with the substance
4. "Листай карусель 👉 …" line
5. "💾 Сохрани…", "📤 Отправь другу, который…" and "💬 <easy question to the audience>"
6. "Больше аналитики каждый день — в Telegram @romchekcrypto (ссылка в профиле)"
7. "Не является финансовой рекомендацией."
8. MAX 5 hashtags (Instagram limit): #биткоин #обзорбиткоина #альтсезон + 2 by topic

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

## OLD carousel→Reel conversion — ⏸ PAUSED since 2026-10-13 (replaced by «Educational Reels» above; do not use). Format (added 2026-10-12) APPROVED by the owner: animated cover + slides 2..N at 4.5 s; base for all Reels and Shorts
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


## Shorts from long YouTube reviews (owner's rule since 2026-11-09)
- After each long review video Claude edits, cut 2 vertical Shorts (owner's rule 2026-11-10; was 4) (1080x1920, LONGER THAN 1 MINUTE — 61–90 s, owner's rule 2026-11-18; one complete thought from start to finish) from it:
  hook title on top, chart crop in a frame, karaoke subtitles, camera + Telegram CTA box. STYLE = brand LIME (owner's rule
  2026-11-18, replaces orange/blue): dark #141414 background, title = white line + lime #c6f432 line (Inter Display Black,
  uppercase), chart frame and camera/Telegram boxes with lime rounded borders, subtitles white with the current word on a
  lime plaque (dark text), red #e5484d only for negative meaning; all content inside the
  phone safe zone (x 40–900, y 220–1490) so YouTube/Instagram UI never covers chart, camera or subtitles.
- Store in shorts/YYYY-MM-DD/<n>-<slug>.mp4, push, then schedule in Metricool every 2 hours after the review goes out
  (first Short at the review time): YouTube Short + the same file as an Instagram Reel (showReelOnFeed true;
  avoid the daily slots: never within ±60 min of the 10:00 carousel or the 18:00 education reel/Short on EITHER platform —
  if a slot collides, shift that review Short to the next free time ≥60 min away; check getScheduledPosts first).
- These 2 review Shorts are ON TOP of the daily 10:00 carousel and 18:00 education reel (owner reminded 2026-11-18);
  quality first: each must be a complete, valuable thought with a strong hook in the first 2 s.
- YouTube: SHORT CAPS title of 2–4 words (e.g. «ГДЕ Я КУПЛЮ БИТКОИН»), 2–3 SEO sentences with «обзор биткоина»/«альтсезон»,
  Telegram line, disclaimer, 3–5 hashtags incl. #shorts; tags filled to 500 chars per the rule below.
  The «related video» link to the latest long video can't be set via Metricool — the owner sets it in YouTube Studio.
- YouTube category for these Shorts = PEOPLE_BLOGS («Люди и блоги»), video language = Russian (owner's rule 2026-11-09).
- **ALL Shorts/Reels on YouTube — education, news, review cuts — ALWAYS category PEOPLE_BLOGS («Люди и блоги») (owner's rule 2026-11-19).**
  Metricool has no language field: language comes from the channel's upload defaults (YouTube Studio → Настройки →
  Загрузка видео по умолчанию → Язык видео = русский); if a Short still shows no language, set it in Studio.
- NO MUSIC in these Shorts (owner's rule 2026-11-14): voice only — run mkshort.py without the music argument and drop the «Музыка: …» line from the description.
- TikTok stays off.

## Long review editing — quality rules (owner's feedback 2026-11-13)
- Re-recorded thoughts: when the owner says the same idea twice (often with different numbers, e.g. "-10%… / -7%…"),
  he is re-recording it — keep ONLY the last take and cut the earlier one completely. Read the transcript for such
  restatements, not just word-level stutters, before rendering.
- After cutting, re-listen (ASR the final audio) around every manual cut to make sure no fragment of a dropped word remains.
- Shorts must end on a COMPLETE thought: never stop right before an explanation ("да то есть посмотрите…").
  End at the end of the sentence that closes the idea; check the last subtitle line before publishing.

## YouTube Shorts (auto, from carousels) — ⏸ PAUSED by the owner on 2026-10-29 (do not build or schedule YouTube Shorts until he re-enables). Format (added 2026-10-12):
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
  "type":"short", "privacy":"public", "madeForKids": false, "category":"PEOPLE_BLOGS", "tags": [...]}.
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
- Instagram carousels (news): always include #биткоин #обзорбиткоина #альтсезон. Education reels: #биткоин #альтсезон #трейдинг + topic (no #обзорбиткоина).

## TikTok carousels — ⏸ PAUSED by the owner on 2026-10-14 (do not schedule anything on TikTok until he re-enables). Format (added 2026-10-12):
- TikTok account @romchekcrypto is connected in the same Metricool brand. Every carousel is ALSO published to TikTok
  as a photo carousel at the same time as on Instagram (10:00 and 18:00), same slide JPGs in the same order.
- Separate createScheduledPost call: providers [{"network":"tiktok"}], media = same raw slide URLs,
  tiktokData {"title": "<≤90 chars, the intriguing headline>", "autoAddMusic": true, "privacyOption": "PUBLIC_TO_EVERYONE",
  "photoCoverIndex": 0, "disableComment": false}, autoPublish true, draft false.
- TikTok caption (text): title line, hook, 1–3 short sentences, "Больше аналитики — Telegram @romchekcrypto",
  "Не является финансовой рекомендацией.", then 3–5 hashtags (#биткоин #альтсезон #криптовалюта + 1–2 by topic).
