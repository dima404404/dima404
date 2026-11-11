/* Dima404 — личный сайт. Загрузка данных и рендер разделов. */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* ---------- Тема ---------- */
const THEMES = ["retro"];
function applyTheme(id) {
  document.documentElement.dataset.theme = id;
  try { localStorage.setItem("dima404-theme", id); } catch (e) {}
  $$(".theme-btn").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.theme === id)));
}
(function initTheme() {
  const fromUrl = new URLSearchParams(location.search).get("theme");
  applyTheme(THEMES.includes(fromUrl) ? fromUrl : "retro");
  document.addEventListener("click", e => {
    const b = e.target.closest(".theme-btn");
    if (b) applyTheme(b.dataset.theme);
  });
})();

/* ---------- Утилиты ---------- */
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const ytSearch = q => "https://www.youtube.com/results?search_query=" + encodeURIComponent(q);
const cover = (appid, name) => appid
  ? `https://cdn.cloudflare.steamstatic.com/steam/apps/${appid}/capsule_231x87.jpg`
  : `https://placehold.co/231x87/1b1b2f/8888aa?text=${encodeURIComponent(name.slice(0, 18))}`;

/* ---------- Рендер ---------- */
function renderHero(d) {
  const p = d.profile;
  $("#hero-name").textContent = p.name;
  $("#hero-nick").textContent = p.nick;
  $("#hero-tagline").textContent = p.tagline;
  $("#hero-about").textContent = p.about;
  $("#hero-city").textContent = p.city;
  $("#hero-born").textContent = p.born;
  const age = Math.floor((Date.now() - new Date(2008, 4, 14)) / 3.15576e10);
  $("#stat-age").textContent = age;
  const music = d.music.length, watch = d.watch.length;
  const games = d.steam.accounts.reduce((n, a) => n + a.count, 0);
  $("#stat-music").textContent = music;
  $("#stat-watch").textContent = watch;
  $("#stat-games").textContent = games;
  $("#now").innerHTML = (d.now || []).map(x => `<span class="chip">${esc(x)}</span>`).join("");
}

function renderTimeline(d) {
  $("#timeline").innerHTML = d.timeline.map(i => `
    <div class="tl-item">
      <div class="tl-year">${esc(i.year)}</div>
      <h3>${esc(i.title)}</h3>
      <p>${esc(i.text)}</p>
    </div>`).join("");
}

function renderMusic(d) {
  const box = $("#tracks");
  const genres = d.genres;
  $("#music-filters").innerHTML = Object.entries(genres).map(([k, v], i) =>
    `<button class="fbtn" data-g="${k}" aria-pressed="${i === 0}">${esc(v)} <span style="opacity:.55">${k === "all" ? d.music.length : d.music.filter(t => t.g === k).length}</span></button>`).join("");

  let cur = "all", q = "";
  const draw = () => {
    const list = d.music.filter(t => (cur === "all" || t.g === cur) &&
      (!q || (t.t + " " + t.a).toLowerCase().includes(q)));
    $("#music-count").textContent = list.length + " треков";
    box.innerHTML = list.map(t => `
      <a class="track" href="${ytSearch(t.t + " " + t.a)}" target="_blank" rel="noopener">
        <div class="tt"><b>${esc(t.t)}</b><span>${esc(t.a)}</span></div>
        <div class="dur">${esc(t.d)}</div>
        <div class="yt">YouTube ↗</div>
      </a>`).join("") || `<p style="color:var(--muted)">Ничего не найдено.</p>`;
  };
  $("#music-filters").addEventListener("click", e => {
    const b = e.target.closest("[data-g]"); if (!b) return;
    cur = b.dataset.g;
    $$("#music-filters .fbtn").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    draw();
  });
  $("#music-search").addEventListener("input", e => { q = e.target.value.trim().toLowerCase(); draw(); });
  draw();
}

function renderGames(d) {
  $("#games-grid").innerHTML = d.steam.accounts.map(a => {
    const max = a.games[0].hours;
    return `
      <div class="card acct">
        <h3>${esc(a.label)}</h3>
        <p style="margin-bottom:14px">
          <b>${a.total.toLocaleString("ru-RU")} ч</b> в играх · ${a.count} игр в библиотеке ·
          <a href="${esc(a.url)}" target="_blank" rel="noopener">профиль ↗</a>
        </p>
        ${a.games.map(g => `
          <div class="game">
            <img src="${cover(g.appid, g.name)}" alt="" loading="lazy" onerror="this.style.visibility='hidden'">
            <div style="flex:1;min-width:0">
              <div class="h">${esc(g.name)}</div>
              <div class="bar"><i style="width:${Math.round(g.hours / max * 100)}%"></i></div>
            </div>
            <div class="sub" style="white-space:nowrap">${g.hours} ч</div>
          </div>`).join("")}
      </div>`;
  }).join("");
}

function renderWatch(d) {
  const K = { movie: "фильм", series: "сериал", anime: "аниме" };
  const counts = { all: d.watch.length, movie: 0, series: 0, anime: 0 };
  d.watch.forEach(w => counts[w.k]++);
  $("#watch-filters").innerHTML = [["all", "всё"], ["anime", "аниме"], ["series", "сериалы"], ["movie", "фильмы"]]
    .map(([k, v], i) => `<button class="fbtn" data-k="${k}" aria-pressed="${i === 0}">${v} <span style="opacity:.55">${counts[k]}</span></button>`).join("");

  let cur = "all", q = "";
  const draw = () => {
    const list = d.watch.filter(w => (cur === "all" || w.k === cur) && (!q || w.t.toLowerCase().includes(q)));
    list.sort((a, b) => b.d.split(".").reverse().join("").localeCompare(a.d.split(".").reverse().join("")));
    $("#watch-count").textContent = list.length + " записей";
    $("#watch-grid").innerHTML = list.map(w => {
      const hue = [...w.t].reduce((h, c) => (h * 31 + c.charCodeAt(0)) % 360, 7);
      return `
      <div class="card poster">
        <div class="ptile" style="background:linear-gradient(135deg,hsl(${hue} 70% 55%),hsl(${(hue + 55) % 360} 75% 45%))">${esc(w.t.slice(0, 1))}</div>
        <div style="flex:1;min-width:0">
          <div><b>${esc(w.t)}</b></div>
          <div class="meta">${esc(w.y)} · ${K[w.k]}${w.e ? " · " + esc(w.e) : ""}${w.tr ? " · " + esc(w.tr) : ""}</div>
          <div class="meta" style="opacity:.7">${esc(w.d)}</div>
        </div>
      </div>`;
    }).join("") || `<p style="color:var(--muted)">Ничего не найдено.</p>`;
  };
  $("#watch-filters").addEventListener("click", e => {
    const b = e.target.closest("[data-k]"); if (!b) return;
    cur = b.dataset.k;
    $$("#watch-filters .fbtn").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    draw();
  });
  $("#watch-search").addEventListener("input", e => { q = e.target.value.trim().toLowerCase(); draw(); });
  draw();
}

function renderHobbies(d) {
  $("#hobbies-grid").innerHTML = d.hobbies.map(h => `
    <div class="card"><div style="font-size:26px">${h.icon}</div>
      <h3>${esc(h.title)}</h3><p>${esc(h.text)}</p></div>`).join("");
}

function renderDevices(d) {
  $("#devices-grid").innerHTML = d.devices.map(v => `
    <div class="card">
      <div class="device-ico">${v.icon}</div>
      <h3>${esc(v.title)}</h3>
      <ul class="specs">${v.specs.map(([k, x]) => `<li><span>${esc(k)}</span><span>${esc(x)}</span></li>`).join("")}</ul>
    </div>`).join("");
  $("#facts").innerHTML = d.facts.map(([k, v]) => `<li><span>${esc(k)}</span><span>${esc(v)}</span></li>`).join("");
}

function renderSocials(d) {
  $("#socials-list").innerHTML = d.socials.map(s => `
    <a class="card social" href="${esc(s.url)}" target="_blank" rel="noopener">
      <div class="ico">${s.icon}</div>
      <div><b>${esc(s.name)}</b><small>${esc(s.handle)}</small></div>
    </a>`).join("");
}

/* ---------- Пасхалка ---------- */
const KONAMI = ["ArrowUp","ArrowUp","ArrowDown","ArrowDown","ArrowLeft","ArrowRight","ArrowLeft","ArrowRight","b","a"];
let pos = 0;
document.addEventListener("keydown", e => {
  pos = e.key === KONAMI[pos] ? pos + 1 : (e.key === KONAMI[0] ? 1 : 0);
  if (pos === KONAMI.length) {
    pos = 0;
    document.body.style.transition = "filter .4s";
    document.body.style.filter = "hue-rotate(180deg) saturate(1.6)";
    setTimeout(() => { document.body.style.filter = ""; }, 2600);
  }
});

/* ---------- Старт ---------- */
fetch("assets/data/data.json")
  .then(r => r.json())
  .then(d => {
    [renderHero, renderTimeline, renderMusic, renderGames,
     renderWatch, renderHobbies, renderDevices, renderSocials]
      .forEach(fn => {
        try { fn(d); }
        catch (err) { console.error("render " + fn.name, err); }
      });
  })
  .catch(err => {
    console.error(err);
    document.querySelector("#hero-tagline").textContent = "Не удалось загрузить data.json — открой сайт через локальный сервер.";
  });
