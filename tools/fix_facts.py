# Правки фактов и уютного сетапа
import json, io

P = r"F:\Dima\Documents\Ai\dima404-site\assets\data\data.json"
d = json.load(io.open(P, encoding="utf-8"))

for f in d["facts"]:
    if f[0] == "Зрение":
        f[1] = "правый глаз не видит — реагирует только на очень яркий цвет"

for dev in d["devices"]:
    if "Уютный" in dev["title"]:
        dev["specs"] = [
            ["Докимакура", "тяжёлая подушка-обнимашка"],
            ["Одеяло", "9 кг — способ хоть как-то обниматься"],
            ["Мониторы", "основной + AOC"],
            ["ОС и софт", "Windows 11 Pro, VS Code, Ollama"],
        ]

json.dump(d, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
