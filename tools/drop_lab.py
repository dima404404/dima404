# Удаление неиспользуемой функции renderLab из app.js
import io, re

p = r"F:\Dima\Documents\Ai\dima404-site\assets\js\app.js"
s = io.open(p, encoding="utf-8").read()
s, n = re.subn(r"function renderLab\(d\) \{.*?\n\}\n\n?", "", s, flags=re.S)
io.open(p, "w", encoding="utf-8").write(s)
print("removed:", n, "| renderLab left:", s.count("renderLab"))
