# deploy.ps1 -> переименование параметра Host (конфликт с автоматической $Host)
import io

p = r"F:\Dima\Documents\Ai\dima404-site\deploy.ps1"
s = io.open(p, encoding="utf-8-sig").read()
s = s.replace("$Host", "$Vps")
s = s.replace("-Host 85.209.3.56", "-Vps 85.209.3.56")
io.open(p, "w", encoding="utf-8-sig").write(s)
print(s[:400])
