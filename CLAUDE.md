# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Oil Optima" (PGS project) — a single-file Flask app that serves an HTML dashboard for a fuel/oil
distribution company and wires several pre-trained ML models behind form endpoints. `README.md` is
accurate as of the 2026 repository audit — read it first. The upstream "ML-Model-Flask-Deployment"
demo leftovers (`model.py`, `request.py`, `model.pkl`) have been deleted; `data/hiring.csv` remains
but nothing loads it.

## Running

```
python app.py          # Flask dev server on http://localhost:5000, debug=True
```

`requirements.txt` exists but is **unpinned** — it was derived from the imports in `app.py`, not from
a known-good environment, so version conflicts are plausible. There is still no test suite, linter,
or build step.

Configuration comes from `.env` (see `.env.example`), loaded via `python-dotenv` at the top of
`app.py`. `GEMINI_API_KEY` and `OPENWEATHER_API_KEY` have no defaults and will fail loudly if unset;
the MySQL settings and `FLASK_SECRET_KEY` fall back to their historical local-dev values.

Requires a local MySQL server, database `oiloptima_pgs` by default. Tables used: `users`, `stations`.
There is no schema file — infer columns from the `cur.execute` calls.

`app.py` is imported/reloaded on every request in debug mode, but the heavy globals (MobileNetV2 for
face embeddings, the Keras safety-stock model, the Gemini chatbot's PDF text extraction over
`data/brocher/`) load at **import time**, so startup is slow and touching `app.py` triggers a full
reload.

## Architecture

Everything lives in `app.py` (~1500 lines), organized into banner-comment sections rather than
modules. Each section is an independent feature owned by a different original author, with its own
imports repeated locally (Flask/pandas/numpy are re-imported several times — harmless, but don't
assume the top-of-file imports are the whole picture).

Sections, in file order:

1. **Auth / face login** (`/`, `/signup`, `/video_feed`) — password login against MySQL plus an
   optional webcam path: `haarcascade_frontalface_default.xml` crops a face from an OpenCV video
   stream into the module-level `detected_face` global, `extract_embeddings` runs MobileNetV2, and
   `face_compare` scores cosine similarity against images in `data/Faces` / `static/faces`.
   The `detected_face` global is shared across requests — it is not per-session.
2. **Static pages** (`/index`, `/about`, `/service`, `/contact`, `/analysis`, …) → `templates/`.
3. **Tank behaviour & injector failure** — `/Tank_Behaviour_Prediction` and
   `/Injector_failure_Prediction` both render `Tank_Behaviour_Prediction.html`, passing `safe` /
   `safe2` respectively. Models: `tank_behavior_model.json` (XGBoost Booster, loaded per request)
   and `injector_failure_model.pkl`.
4. **Demand forecasting / stock-out** — `/Stock_out_Prediction` unpickles `demand_forecasting.pkl`
   (a statsmodels-style object: `.fit()` then `.forecast(n)`) and writes the chart to
   `static/forecast_plot.png`, which the template then references.
5. **Safety stock** — `/Safety_stock`, Keras `modelNN_safety_stock.h5` loaded once at import.
6. **Client feedback** — `/Clients_Feedback` and `/download_excel` pull a live Google Sheet by CSV
   export (`sheet_id` hardcoded), rename the French survey column headers to `date`/`Partner`/
   `Governement`/`Topic`/`Reclamation`/`Rate`, score sentiment with TextBlob, and dump
   `static/database/clients_feedback.xlsx`.
7. **Logistics** — station CRUD on the MySQL `stations` table, Dijkstra / A*-with-haversine-heuristic
   routing over station coordinates (`/createpath/<long1>/<lat1>/<long2>/<lat2>/`), a weather lookup
   by coordinate, and `/resume/<path>` which ranks driver CVs in `static/pdfs/` against a job
   description via CountVectorizer + cosine similarity. Note `path` is passed through the URL and
   parsed with `ast.literal_eval`.
8. **Trailer / tractor forecast** — CSV upload endpoints scoring `terminal1_model.json`,
   `terminal2_model.json`, `tractor_model.json` (XGBoost Boosters).
9. **Chatbot** — `/chatbot`, Google Gemini (`gemini-pro`). The system prompt is built at import time
   from every PDF in `data/brocher/` via pdfplumber; `messages` is a module-level list, so
   conversation history is global across all users and is reset on GET `/chatbot`.

## Model files and notebooks

The `.pkl` / `.h5` / `.json` model artifacts at the repo root are the served versions — they must
match the exact feature order the route builds (see e.g. the mismatched column names in
`Tank_Behaviour_Prediction_form`, where the DataFrame is built in one order and `.columns` assigned
in another; that quirk is baked into the trained model, so don't "fix" it without retraining).

The `.ipynb` training sources now live in `notebooks/`. Five artifacts that no code references were
moved to `archive/` (git-ignored) rather than deleted — they may be newer retrainings that were never
wired up; see `archive/README.md`. Do not assume they are drop-in replacements.

## Known issues to be aware of when editing

- The login queries at lines ~163 and ~197 interpolate `username` directly into SQL; several station
  routes interpolate `index` into DELETE/SELECT. Passwords are stored and compared in plaintext.
  Left as-is deliberately (behaviour change) — don't propagate the pattern; use `%s` params in new code.
- `/` is registered twice (`login`, GET-only; `login_with_face`, GET/POST), so GET never reaches the
  face-compare branch. `app.py` also renders both `'login.html'` and `'Login.html'` while only
  `templates/Login.html` exists — Windows-only luck. Both documented in README, not fixed.
- Secrets are now read from `.env`. Do not reintroduce hardcoded keys.
