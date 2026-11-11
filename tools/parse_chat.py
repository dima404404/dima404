# Парсит HTML-экспорт Telegram (AyuGram) и выгружает сообщения в текстовый дамп
import io, re, html, sys, collections

SRC = r"F:\Dima\Downloads\AyuGram Desktop\ChatExport_2026-11-11\messages.html"
OUT = r"F:\Dima\Documents\Ai\dima404-site\out\chat_dump.txt"

raw = open(SRC, "rb").read()
text = raw.decode("utf-8", "replace")

# каждый блок сообщения
blocks = re.findall(r'<div class="message default clearfix[^"]*" id="message(\d+)">(.*?)(?=<div class="message |\Z)', text, re.S)

def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()

rows = []
for mid, body in blocks:
    m_name = re.search(r'class="from_name">(.*?)</div>', body, re.S)
    m_date = re.search(r'class="pull_right date details" title="([^"]+)"', body)
    m_text = re.search(r'<div class="text">(.*?)</div>', body, re.S)
    name = strip_tags(m_name.group(1)) if m_name else "?"
    date = m_date.group(1) if m_date else "?"
    txt = strip_tags(m_text.group(1)) if m_text else ""
    rows.append((mid, date, name, txt))

cnt = collections.Counter(r[2] for r in rows)
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("Участники: %s\n\n" % cnt.most_common())
    for mid, date, name, txt in rows:
        f.write("[%s] %s: %s\n" % (date, name, txt))

print("messages:", len(rows))
print(cnt.most_common())
