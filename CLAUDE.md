# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Name**: MediaNexus — desktop app for managing a personal media collection (books, manga, anime).  
**Course work**: Lviv Polytechnic National University, CAD Systems dept.  
**Stack**: Python 3.10+ · Tkinter (ttk) · JSON local storage · MVC pattern  
**Deadline**: Archive submission by 10:00, 18 May 2026.

## Non-Negotiable Constraints

- **Only Python standard library** — zero external packages, no pip installs.
- **Entry point must be `main.py`**.
- **MVC pattern is mandatory** — Model, View, Controller in clearly separate modules.
- **No internet required** — all data stored locally in `data/collection.json`.
- **No `venv`, `__pycache__`, `.idea`, `.vscode`** in the final zip (≤ 5 MB).

## Running the App

```bash
python main.py
```

## Architecture (MVC)

```
main.py                  # Instantiates Model → Controller → View, starts mainloop
models/
  media_item.py          # MediaItem dataclass (fields below)
  collection_model.py    # CRUD logic + JSON persistence
views/
  main_view.py           # Main window: Treeview list, toolbar, search bar
  add_edit_dialog.py     # Toplevel dialog for add / edit
  stats_view.py          # Statistics & analytics tab/frame
  filter_view.py         # Filter / sort panel
controllers/
  main_controller.py     # Wires all View events → Model calls → View updates
data/
  collection.json        # Persisted collection (auto-created on first run)
```

**Rules:**
- View never imports from `models/` — only calls `self.controller.*`.
- Model never imports from `tkinter`.
- Controller handles all validation before calling Model.

## Data Model

`MediaItem` fields:
| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` | UUID |
| `title` | `str` | required |
| `media_type` | `str` | `"book"` / `"manga"` / `"anime"` |
| `genre` | `str` | |
| `year` | `int` | release year |
| `description` | `str` | |
| `rating` | `int` | 1–10, nullable |
| `status` | `str` | `"Переглянуто"` / `"В процесі"` / `"Заплановано"` / `"Покинуто"` |
| `completed_date` | `str` | ISO date; **auto-set when status → "Переглянуто"** |

## Functional Requirements

| ID | Description | Priority |
|----|-------------|----------|
| FR-01 | Add media record (title, type, genre, year, description) | High |
| FR-02 | Edit any field of an existing record | High |
| FR-03 | Delete record with confirmation dialog | High |
| FR-04 | Rate media 1–10; editable at any time | High |
| FR-05 | Set status: Переглянуто / В процесі / Заплановано / Покинуто | High |
| FR-06 | Real-time search by title or genre | High |
| FR-07 | Filter by type/status/genre; sort by rating or title | Medium |
| FR-08 | Collection stats: total count, type breakdown, avg rating, status counts | Medium |
| FR-09 | Analytics: completed items by month/year; top-5 rated for a period | Medium |
| FR-10 | Export collection (full or filtered) to CSV | Low |

## Non-Functional Requirements

| ID | Description | Priority |
|----|-------------|----------|
| NFR-01 | Search/filter on ≤1000 records completes in < 1 s | High |
| NFR-02 | All data stored locally in JSON, no internet needed | High |
| NFR-03 | Works on Windows 10/11, Python 3.10+ | Medium |
| NFR-04 | Basic ops (add, search, stats) reachable in ≤ 3 clicks | Medium |

## Mandatory UI Features (Graded 2 pts each — 30 pts total, Appendix B)

1. **Bilingual UI** — Ukrainian / English toggle on main window.
2. **Button click reactions** — every button visibly responds.
3. **Correct layout & stretching** — all widgets resize with window (`grid`/`pack` weights set).
4. **Window title & centering** — main window centred on screen with a descriptive title.
5. **UI styling** — custom colours, fonts, padding (not default grey).
6. **Selection input widgets** — `Combobox` for media type/status/genre; rating `Scale` or `Spinbox`.
7. **Input validation** — block empty title, invalid year/rating before saving.
8. **Standard dialogs** — `messagebox` for confirmations/errors; `filedialog` for CSV export.
9. **Custom dialog window** — `Toplevel` add/edit form.
10. **Menu** — main menu bar with File / View / Help or right-click context menu on list.
11. **Persist data** — save/load `data/collection.json` via `json` stdlib.
12. **Scrollable list** — `ttk.Treeview` with vertical `Scrollbar`.
13. **CRUD + sort** — add, edit, delete, sort all implemented.
14. **Mouse/keyboard interaction** — keyboard shortcuts (e.g. `Delete` key, `Ctrl+N`) or drag-to-reorder.
15. **Tabs / panels / progress** — `ttk.Notebook` for Collection / Statistics / Analytics tabs.

## Code Style Rules

- `PascalCase` for classes, `snake_case` for files and functions.
- View classes only call `self.controller.*` — no direct model access.
- Model classes have zero Tkinter imports.
- One class per file; tiny helpers may share a file.
