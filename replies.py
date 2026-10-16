# -*- coding: utf-8 -*-
"""Охирги постлардаги янги изоҳларга автоматик жавоб қайтаради.
GitHub Actions уни ҳар соатда ишга туширади.
Керакли рухсат: instagram_business_manage_comments
"""
import json, pathlib, re, zlib
from post import api, git_push, ROOT
from content import TG

STATE = ROOT / "state" / "replied.json"

QUIZ = [
    "Жавобингиз учун раҳмат! 👍 Тўғри жавоб ва батафсил тушунтиришни Telegram'да ёзаман: {tg}",
    "Зўр, фикрингиз қабул қилинди! 🙌 Бу мавзуда саволингиз бўлса — {tg} га ёзинг",
    "Раҳмат, қизиқ танлов! 😊 Нима учун айнан шундай эканини {tg} да тушунтириб бераман",
]
GENERAL = [
    "Фикрингиз учун катта раҳмат! 🙏 Батафсил гаплашамиз — Telegram: {tg}",
    "Раҳмат! 🙌 Сизнинг бизнесингизда қандай ишлашини кўрсатиб бераман — {tg} га ёзинг",
    "Зўр савол! 👍 Тўлиқ жавобни Telegram'да бераман: {tg}",
    "Изоҳингиз учун раҳмат! 😊 Бу мавзуда ҳар куни янги пост бўлади — обуна бўлинг. Саволлар учун: {tg}",
]
THANKS = [
    "Сизга ҳам раҳмат! 🙏 Обуна бўлинг — ҳар куни янги бизнес ғоялари",
    "Раҳмат! 😊 Фойдали бўлганидан хурсандман",
]


def pick(options, key):
    return options[zlib.crc32(key.encode()) % len(options)].format(tg=TG)


def answer_for(text, cid):
    t = (text or "").strip().lower()
    if re.fullmatch(r"[abcdабвгд]\W*|[1-5]\W*", t):
        return pick(QUIZ, cid)
    if any(w in t for w in ("раҳмат", "рахмат", "rahmat", "спасибо", "👍", "❤", "🔥", "зўр", "zo'r", "zor")) and len(t) < 40:
        return pick(THANKS, cid)
    return pick(GENERAL, cid)


def main():
    done = set(json.loads(STATE.read_text())) if STATE.exists() else set()
    me = api("GET", "me", fields="user_id,username")
    my = me["username"].lower()
    media = api("GET", "me/media", fields="id,timestamp", limit=10).get("data", [])
    new = 0
    for m in media:
        comments = api("GET", f"{m['id']}/comments", fields="id,text,username,replies{username}", limit=50).get("data", [])
        for c in comments:
            if c["id"] in done or (c.get("username") or "").lower() == my:
                continue
            replied = any((r.get("username") or "").lower() == my for r in c.get("replies", {}).get("data", []))
            if not replied:
                api("POST", f"{c['id']}/replies", message=answer_for(c.get("text"), c["id"]))
                new += 1
            done.add(c["id"])
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(sorted(done)))
    print(f"Янги жавоблар: {new}")
    if new:
        git_push([STATE], f"{new} та изоҳга жавоб")


if __name__ == "__main__":
    main()
