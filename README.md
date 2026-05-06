# ✈️ DFS IFR Katalog — GitHub Pages

Automatisch aktualisierter Katalog aller deutschen IFR-Flugplätze mit Anflugkarten aus dem DFS BasicIFR AIP.

**URL:** `https://jscepik-source.github.io/dfs-ifr-katalog/`

---

## 🌐 Seiten

| Seite | URL | Beschreibung | Datenquelle |
|---|---|---|---|
| [DFS IFR Katalog](index.html) | [/](https://jscepik-source.github.io/dfs-ifr-katalog/) | Deutsche IFR-Flugplätze mit Anflugkarten, SIDs, STARs aus dem DFS BasicIFR AIP | DFS AIP BasicIFR |

---

## 🤖 Bot

| Bot | Aktualisiert | Intervall |
|---|---|---|
| `ifr_bot.py` | `ifr_katalog_export.json` → index.html | Alle 6h via GitHub Actions |

---

## 📁 Dateistruktur

```
📦 dfs-ifr-katalog/
├── 🌐 index.html                  ← DFS IFR Flughafen-Katalog
├── 📊 ifr_katalog_export.json     ← Daten für index.html
├── 🤖 ifr_bot.py                  ← Scrapt DFS BasicIFR
└── ⚙️ .github/workflows/
    └── update-ifr.yml             ← GitHub Actions (alle 6h)
```

---

## ⚙️ GitHub Actions

Der Workflow `.github/workflows/update-ifr.yml` läuft automatisch **alle 6 Stunden** und scrapt den DFS BasicIFR AIP neu.
