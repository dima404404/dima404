# Открывает PR в is-a-dev/register с доменом dima404.is-a.dev
import subprocess, base64, json, sys

DOMAIN = "dima404"
GH_USER = "dima404404"
CNAME = "dima404404.github.io"
BRANCH = "add-dima404"

record = {
    "owner": {"username": GH_USER},
    "records": {"CNAME": CNAME},
}

def gh(*args, check=True):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        print("FAIL:", args, r.stderr[:500])
        sys.exit(1)
    return r.stdout.strip()

# 1. SHA главной ветки форка
sha = gh("api", f"repos/{GH_USER}/register/git/ref/heads/main", "--jq", ".object.sha")

# 2. Ветка (если уже есть — ок)
gh("api", "-X", "POST", f"repos/{GH_USER}/register/git/refs",
   "-f", f"ref=refs/heads/{BRANCH}", "-f", f"sha={sha}", check=False)

# 3. Файл домена
content = base64.b64encode(json.dumps(record, indent=4).encode()).decode()
body = json.dumps({
    "message": f"Add {DOMAIN}.is-a.dev",
    "content": content,
    "branch": BRANCH,
})
r = subprocess.run(["gh", "api", "-X", "PUT",
                    f"repos/{GH_USER}/register/contents/domains/{DOMAIN}.json",
                    "--input", "-"],
                   input=body, capture_output=True, text=True, encoding="utf-8")
print("file:", "ok" if r.returncode == 0 else r.stderr[:300])

# 4. PR
pr = subprocess.run(["gh", "pr", "create",
                     "--repo", "is-a-dev/register",
                     "--head", f"{GH_USER}:{BRANCH}",
                     "--title", f"Add {DOMAIN}.is-a.dev",
                     "--body",
                     f"Personal site of @{GH_USER}, hosted on GitHub Pages ({CNAME}).\n\n"
                     f"- record: CNAME -> {CNAME}\n- proxied: false\n"],
                    capture_output=True, text=True, encoding="utf-8")
print("pr:", pr.stdout.strip() or pr.stderr[:500])
