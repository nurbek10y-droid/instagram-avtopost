# -*- coding: utf-8 -*-
"""Бугунги постни Instagram'га жойлайди.

GitHub Actions ҳар куни ишга туширади:
 1) бугун кампаниянинг нечанчи куни эканини ҳисоблайди (1..60)
 2) расмни чизади (JPEG) ва репозиторийга сақлайди
 3) расм очиқ ҳаволаси орқали Instagram'га жойлайди
Махфий калит: IG_ACCESS_TOKEN (GitHub Secrets)
"""
import datetime as dt, json, os, pathlib, subprocess, sys, time
import urllib.parse, urllib.request
from content import POSTS, caption, COLLAB

ROOT = pathlib.Path(__file__).parent
START = dt.date.fromisoformat(os.environ.get("START_DATE", "2026-10-17"))
TZ = dt.timezone(dt.timedelta(hours=5))  # Тошкент
API = "https://graph.instagram.com"
REPO = os.environ.get("GITHUB_REPOSITORY", "nurbek10y-droid/instagram-avtopost")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
LOG = ROOT / "state" / "posted.json"


def api(method, path, **params):
    token = os.environ["IG_ACCESS_TOKEN"].strip()
    url = f"{API}/{path}"
    data = None
    if method == "GET":
        params["access_token"] = token
        url += "?" + urllib.parse.urlencode(params)
    else:
        params["access_token"] = token
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"API хатоси {e.code} ({path}): {body}")


def day_number(today=None):
    today = today or dt.datetime.now(TZ).date()
    return (today - START).days + 1


def load_log():
    return json.loads(LOG.read_text()) if LOG.exists() else {}


def git_push(paths, msg):
    subprocess.run(["git", "config", "user.name", "avtopost-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "avtopost-bot@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", *map(str, paths)], check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", msg], check=True)
    subprocess.run(["git", "pull", "--rebase", "-q"], check=True)
    subprocess.run(["git", "push", "-q"], check=True)


def main():
    log = load_log()
    if os.environ.get("FORCE_DAY"):
        day = int(os.environ["FORCE_DAY"])
    else:
        # навбатдаги ҳали жойланмаган пост (тартиб билан)
        left = [d for d in range(1, len(POSTS) + 1) if str(d) not in log]
        if not left:
            print("60 та постнинг ҳаммаси жойланган. Кампания тугади.")
            return
        day = left[0]
    if not 1 <= day <= len(POSTS):
        print(f"Нотўғри кун рақами: {day}")
        return

    # 1) юқори сифатли Reels (1080x1920, анимация)
    import reel
    mp4 = reel.make(day)
    git_push([mp4], f"{day}-кун reels")
    sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    video_url = f"https://raw.githubusercontent.com/{REPO}/{sha}/reels/{mp4.name}"
    for _ in range(10):  # ҳавола очилгунча кутамиз
        try:
            urllib.request.urlopen(video_url, timeout=30).read(10); break
        except Exception:
            time.sleep(6)

    # 2) Instagram
    me = api("GET", "me", fields="user_id,username")
    ig = me["user_id"]
    params = dict(media_type="REELS", video_url=video_url, share_to_feed="true", caption=caption(POSTS[day - 1]))
    try:
        cont = api("POST", f"{ig}/media", collaborators=json.dumps(COLLAB), **params)
    except SystemExit as e:
        print("Ҳамкор билан бўлмади, оддий пост қилинади:", e)
        cont = api("POST", f"{ig}/media", **params)
    cid = cont["id"]
    for _ in range(40):  # видео ишланиши 5 дақиқагача
        st = api("GET", cid, fields="status_code").get("status_code")
        if st == "FINISHED":
            break
        if st in ("ERROR", "EXPIRED"):
            raise SystemExit(f"Instagram видеони қабул қилмади: {st}")
        time.sleep(8)
    pub = api("POST", f"{ig}/media_publish", creation_id=cid)
    print(f"✅ {day}-кун жойланди @{me['username']}: media id {pub['id']}")

    log[str(day)] = {"media_id": pub["id"], "at": dt.datetime.now(TZ).isoformat(timespec="minutes")}
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1))
    git_push([LOG], f"{day}-кун жойланди")


if __name__ == "__main__":
    main()
