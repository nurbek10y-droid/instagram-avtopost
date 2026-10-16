# -*- coding: utf-8 -*-
from .posts_1 import POSTS_1
from .posts_2 import POSTS_2
from .posts_3 import POSTS_3
from .posts_4 import POSTS_4
from .posts_5 import POSTS_5
from .posts_6 import POSTS_6

POSTS = POSTS_1 + POSTS_2 + POSTS_3 + POSTS_4 + POSTS_5 + POSTS_6

TG = "@NurbekRBA"
IG = "@nurbek62.62"

HASHTAGS = {
    "crm": "#bitrix24 #crm #бизнес #сотув #тадбиркор",
    "dash": "#дашборд #bitrix24 #бизнес #ҳисобот #раҳбар",
    "ai": "#ai #aiсотувчи #bitrix24 #бизнес #автоматлаштириш",
    "biz": "#бизнес #тадбиркор #сотув #bitrix24 #ўзбекистон",
}


def tags_for(p):
    t = p["tag"].lower()
    if "ai" in t:
        return HASHTAGS["ai"]
    if "дашборд" in t:
        return HASHTAGS["dash"]
    if p["type"] in ("quiz", "list") and "bitrix" not in t:
        return HASHTAGS["biz"]
    return HASHTAGS["crm"]


def caption(p):
    """Пост остидаги матн (кириллча)."""
    ask = [] if "изоҳ" in p["q"].lower() else ["Изоҳда ёзинг 👇"]
    parts = [p["hook"], "", p["caption"], "", "❓ " + p["q"], *ask, "",
             f"💬 Саволингиз бўлса — Telegram: {TG}",
             "👉 Telegram'га ўтиш ҳаволаси — профилимда",
             "🔔 Фойдали бўлса, обуна бўлинг — ҳар куни янги бизнес ғоя", "",
             tags_for(p)]
    return "\n".join(parts)
