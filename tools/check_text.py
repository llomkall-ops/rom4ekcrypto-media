#!/usr/bin/env python3
"""Check captions / descriptions / scripts for words that trigger bans or reduced reach in the trading niche.
usage: python3 tools/check_text.py <file-or-text> [...]   (rules: growth/SAFETY.md)"""
import re, sys, pathlib
STOP = [r"заработа", r"заработок", r"пассивн\w* доход", r"гарант", r"без риска", r"100\s?% (сделк|профит|прибыл)",
        r"удво", r"\bх\s?\d{2,}\b|\bx\s?\d{2,}\b", r"иксы", r"сигнал\w* (в|на|от|тут|здесь)\b|vip-?(канал|чат|клуб)|платн\w* сигнал", r"покупай сейчас", r"вход здесь",
        r"реферал", r"промокод", r"регистрируй\w* по ссылке", r"whatsapp|ватсап|вотсап", r"доверительн",
        r"инвестирую за", r"управлени\w* (вашими |твоими )?деньг", r"розыгрыш", r"поставь \+", r"отметь \d+",
        r"перешли \d+", r"оплат\w* крипт", r"доход\w* \d+\s?%", r"поднял \$", r"разбогате"]
WARN = [r"сигнал", r"\bvip\b", r"\d+\s?% трейдеров", r"\bкупи", r"прибыл", r"иксов", r"в личку|в директ", r"ссылк", r"токен"]
def scan(s):
    hits = []
    for lvl, pats in (("STOP", STOP), ("WARN", WARN)):
        for p in pats:
            for m in re.finditer(p, s, re.I):
                a = max(0, m.start() - 30); hits.append((lvl, s[a:m.end() + 30].replace("\n", " ")))
    return hits
bad = 0
for arg in sys.argv[1:]:
    p = pathlib.Path(arg)
    try: s = p.read_text() if len(arg) < 250 and p.is_file() else arg
    except OSError: s = arg
    for lvl, ctx in scan(s):
        print(f"{lvl}: …{ctx}…"); bad += lvl == "STOP"
print("OK" if not bad else f"{bad} STOP hit(s) — rewrite (growth/SAFETY.md)")
sys.exit(1 if bad else 0)
