# Обогащение data.json реальными данными Steam и правками профиля
import json, io, os

P = r"F:\Dima\Documents\Ai\dima404-site\assets\data\data.json"
d = json.load(io.open(P, encoding="utf-8"))

def load(name):
    p = rf"F:\Dima\Documents\Ai\dima404-site\out\steam_{name}.json"
    return json.load(io.open(p, encoding="utf-8"))["response"]["games"]

def top(games, n=10):
    g = sorted(games, key=lambda x: -x["playtime_forever"])[:n]
    return [{"name": x["name"], "hours": round(x["playtime_forever"] / 60, 1), "appid": x["appid"]} for x in g]

main_g, old_g = load("main"), load("old")
d["steam"] = {
    "accounts": [
        {"label": "Основной аккаунт", "url": "https://steamcommunity.com/profiles/76561199569058519/",
         "count": len(main_g), "total": round(sum(x["playtime_forever"] for x in main_g) / 60),
         "games": top(main_g)},
        {"label": "Старый аккаунт", "url": "https://steamcommunity.com/profiles/76561199201374785/",
         "count": len(old_g), "total": round(sum(x["playtime_forever"] for x in old_g) / 60),
         "games": top(old_g)},
    ]
}
d.pop("games", None)

# смягчаем медицинские подробности
d["facts"] = [
    ["Рост / вес", "173 см / ~80 кг"],
    ["Город", "Оренбург"],
    ["Зрение", "ношу очки, правый глаз видит хуже"],
    ["Слух", "левое ухо слышит чуть тише"],
    ["Статус", "учусь на сисадмина, параллельно копаюсь в технике"],
]

# Discord — отображаемое имя из профиля
for s in d["socials"]:
    if s["name"] == "Discord":
        s["handle"] = "_dima404 · VoidCat | Kirby"

# «сейчас» на главной
d["now"] = [
    "🎮 VRChat, Minecraft, CS2",
    "🎧 hardstyle и breakcore",
    "📺 исекай про попаданцев",
    "🛠 ноут на профилактике",
]

json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", len(d["steam"]["accounts"][0]["games"]), d["steam"]["accounts"][1]["total"], "h в старом")
