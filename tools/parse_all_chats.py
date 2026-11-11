# Разбор всех экспортов Telegram: сообщения по чатам в отдельные дампы
import io, os, re, html, collections

BASE = r"F:\Dima\Downloads\AyuGram Desktop"
OUT = r"F:\Dima\Documents\Ai\dima404-site\out"

def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()

for folder in sorted(os.listdir(BASE)):
    path = os.path.join(BASE, folder)
    src = os.path.join(path, "messages.html")
    if not os.path.isfile(src):
        continue
    text = open(src, "rb").read().decode("utf-8", "replace")
    blocks = re.findall(r'<div class="message default clearfix[^"]*" id="message(\d+)">(.*?)(?=<div class="message |\Z)', text, re.S)
    rows = []
    for mid, body in blocks:
        m_name = re.search(r'class="from_name">(.*?)</div>', body, re.S)
        m_date = re.search(r'class="pull_right date details" title="([^"]+)"', body)
        m_text = re.search(r'<div class="text">(.*?)</div>', body, re.S)
        rows.append((m_date.group(1) if m_date else "?",
                     strip_tags(m_name.group(1)) if m_name else "?",
                     strip_tags(m_text.group(1)) if m_text else ""))
    cnt = collections.Counter(r[1] for r in rows)
    dst = os.path.join(OUT, "chat_" + folder.replace("ChatExport_", "").replace(" ", "_") + ".txt")
    with io.open(dst, "w", encoding="utf-8") as f:
        f.write("чат: %s\nучастники: %s\n\n" % (folder, cnt.most_common()))
        for date, name, txt in rows:
            f.write("[%s] %s: %s\n" % (date, name, txt))
    print(folder, len(rows), cnt.most_common(4))
