import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from locales import MEDIA_ANIME, MEDIA_BOOK, MEDIA_MANGA, SORT_KEYS, STATUSES, THEME, MEDIA_TYPES

# Window and column geometry constants
_WIN_WIDTH = 1150
_WIN_HEIGHT = 720
_WIN_MIN_W = 850
_WIN_MIN_H = 550

_COL_W_TITLE = 200
_COL_W_TYPE = 70
_COL_W_GENRE = 100
_COL_W_YEAR = 75
_COL_W_RATING = 60
_COL_W_STATUS = 120
_COL_W_ADDED = 90


def _bind_hover(widget: ttk.Button) -> None:
    """Apply hover style bindings to a ttk.Button."""
    widget.bind("<Enter>", lambda e, w=widget: w.configure(style="Hover.TButton"))
    widget.bind("<Leave>", lambda e, w=widget: w.configure(style="TButton"))


# ── AddEditDialog ─────────────────────────────────────────────────────────────

class AddEditDialog:
    def __init__(self, parent, controller, item_data: dict | None = None):
        self.controller = controller
        self.item_data = item_data
        self.result: dict | None = None
        self._build_window(parent)
        self._build_form()
        self._build_buttons()
        if item_data is not None:
            self._populate(item_data)
        self.window.update_idletasks()
        self._center_on_parent(parent) 

    def _build_window(self, parent):
        self.window = tk.Toplevel(parent)
        key = "dlg_edit_title" if self.item_data else "dlg_add_title"
        self.window.title(self.controller.t(key))
        self.window.configure(bg=THEME["bg"])
        self.window.resizable(False, False)
        self.window.grab_set() # Робить інші вікна недоступними поки не закриєш 
        self.window.focus_set()

    def _center_on_parent(self, parent): 
        """ Центрує вікно """
        w, h = self.window.winfo_width(), self.window.winfo_height()
        px = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.window.geometry(f"+{px}+{py}")

    def _build_form(self):
        self._form = ttk.Frame(self.window, padding=15)
        self._form.pack(fill="both", expand=True)
 
        # Змінні прив'язані до віджетів 
        self.title_var = tk.StringVar() 
        self.type_var = tk.StringVar(value=MEDIA_TYPES[0])
        self.genre_var = tk.StringVar()
        self.year_var = tk.StringVar(value=str(datetime.date.today().year))
        self.rating_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value=STATUSES[2])

        # створення полів введення 
        rows = [
            (self.controller.t("lbl_title"), self._make_entry(self.title_var)),
            (self.controller.t("lbl_type"), self._make_type_combo()),
            (self.controller.t("lbl_genre"), self._make_entry(self.genre_var)),
            (self.controller.t("lbl_year"), self._make_year_spin()),
            (self.controller.t("lbl_rating"), self._make_rating_spin()),
            (self.controller.t("lbl_status"), self._make_status_combo()),
        ]
        for r, (label_text, widget) in enumerate(rows):
            lbl = ttk.Label(self._form, text=label_text,
                            foreground=THEME["text_dim"])
            lbl.grid(row=r, column=0, sticky="w", padx=(0, 10), pady=5) #Назва полів 
            widget.grid(row=r, column=1, sticky="ew", pady=5) # Розставлення кожного поля на фреймі

        desc_row = len(rows)
        lbl_desc = ttk.Label(self._form, text=self.controller.t("lbl_desc"),
                             foreground=THEME["text_dim"])
        lbl_desc.grid(row=desc_row, column=0, sticky="nw", padx=(0, 10), pady=5)
        self.desc_text = tk.Text(
            self._form, height=4, width=30,
            bg=THEME["bg_card"], fg=THEME["text"],
            insertbackground=THEME["text"],
            relief="flat", padx=6, pady=4,
            font=("Segoe UI", 10),
        )
        self.desc_text.grid(row=desc_row, column=1, sticky="ew", pady=5)

        self._form.columnconfigure(1, weight=1)

    def _make_entry(self, var: tk.StringVar) -> ttk.Entry:
        return ttk.Entry(self._form, textvariable=var, width=30)

    def _make_type_combo(self) -> ttk.Combobox:
        return ttk.Combobox(self._form, textvariable=self.type_var,
                            values=MEDIA_TYPES, state="readonly", width=28)

    def _make_status_combo(self) -> ttk.Combobox:
        return ttk.Combobox(self._form, textvariable=self.status_var,
                            values=STATUSES, state="readonly", width=28)

    def _make_year_spin(self) -> ttk.Spinbox:
        return ttk.Spinbox(self._form, from_=1900, to=2030,
                           textvariable=self.year_var, width=10)

    def _make_rating_spin(self) -> ttk.Spinbox:
        return ttk.Spinbox(self._form, from_=0, to=10,
                           textvariable=self.rating_var, width=10)

    def _build_buttons(self):
        btn_frame = ttk.Frame(self.window, padding=(15, 0, 15, 15))
        btn_frame.pack(fill="x")

        self.btn_save = ttk.Button(
            btn_frame, text=self.controller.t("btn_save"),
            command=self._on_save, style="Accent.TButton",
        )
        self.btn_save.pack(side="right", padx=(5, 0))
        _bind_hover(self.btn_save)

        btn_cancel = ttk.Button(
            btn_frame, text=self.controller.t("btn_cancel"),
            command=self.window.destroy,
        )
        btn_cancel.pack(side="right")
        _bind_hover(btn_cancel)

    # Параметри по дефолту 
    def _populate(self, data: dict):
        self.title_var.set(data.get("title", ""))
        self.type_var.set(data.get("media_type", MEDIA_TYPES[0]))
        self.genre_var.set(data.get("genre", ""))
        self.year_var.set(str(data.get("year", datetime.date.today().year)))
        rating = data.get("rating")
        self.rating_var.set(str(rating) if rating is not None else "0")
        self.status_var.set(data.get("status", STATUSES[2]))
        desc = data.get("description", "")
        if desc:
            self.desc_text.insert("1.0", desc)
    # Збереження результау 
    def _on_save(self):
        data = {
            "id": self.item_data.get("id", "") if self.item_data else "",
            "title": self.title_var.get(),
            "media_type": self.type_var.get(),
            "genre": self.genre_var.get(),
            "year": self.year_var.get(),
            "rating": self.rating_var.get(),
            "status": self.status_var.get(),
            "description": self.desc_text.get("1.0", "end-1c"),
            "completed_date": self.item_data.get("completed_date", "") if self.item_data else "",
            "added_date": self.item_data.get("added_date", "") if self.item_data else "",
        }
        ok, err, coerced = self.controller.validate_item_form(data)
        if not ok:
            messagebox.showerror(self.window.title(), err, parent=self.window)
            return
        data.update(coerced)
        self.result = data
        self.window.destroy()

    def get_result(self) -> dict | None:
        return self.result


# ── FilterView ────────────────────────────────────────────────────────────────

class FilterView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.on_filter_change = None
        self.frame = ttk.Frame(parent)
        self._build()

    def _build(self):
        pad = {"padx": 4, "pady": 4}

        # ---
        self.lbl_type = ttk.Label(self.frame, text=self.controller.t("lbl_filter_type"),
                                  foreground=THEME["text_dim"])
        self.lbl_type.grid(row=0, column=0, sticky="w", **pad)
        
        self.type_var = tk.StringVar(value="")
        self.type_cb = ttk.Combobox(
            self.frame, textvariable=self.type_var,
            values=[""] + list(MEDIA_TYPES), state="readonly", width=10,
        )
        self.type_cb.grid(row=0, column=1, sticky="w", **pad)
        self.type_cb.bind("<<ComboboxSelected>>", self._on_change)

        # --- 
        self.lbl_status = ttk.Label(self.frame, text=self.controller.t("lbl_filter_status"),
                                    foreground=THEME["text_dim"])
        self.lbl_status.grid(row=0, column=2, sticky="w", **pad)
        self.status_var = tk.StringVar(value="")
        self.status_cb = ttk.Combobox(
            self.frame, textvariable=self.status_var,
            values=[""] + list(STATUSES), state="readonly", width=14,
        )
        self.status_cb.grid(row=0, column=3, sticky="w", **pad)
        self.status_cb.bind("<<ComboboxSelected>>", self._on_change)
        
        
        
        # --- 
        self.lbl_genre = ttk.Label(self.frame, text=self.controller.t("lbl_filter_genre"),
                                   foreground=THEME["text_dim"])
        self.lbl_genre.grid(row=0, column=4, sticky="w", **pad)
        self.genre_var = tk.StringVar()
        self.genre_entry = ttk.Entry(self.frame, textvariable=self.genre_var, width=12)
        self.genre_entry.grid(row=0, column=5, sticky="ew", **pad)
        self.genre_entry.bind("<KeyRelease>", self._on_change)

        # --- 
        self.lbl_sort = ttk.Label(self.frame, text=self.controller.t("lbl_sort_by"),
                                  foreground=THEME["text_dim"])
        self.lbl_sort.grid(row=0, column=6, sticky="w", **pad)
        self.sort_var = tk.StringVar(value=SORT_KEYS[0])
        self.sort_cb = ttk.Combobox(
            self.frame, textvariable=self.sort_var,
            values=SORT_KEYS, state="readonly", width=9,
        )
        self.sort_cb.grid(row=0, column=7, sticky="w", **pad)
        self.sort_cb.bind("<<ComboboxSelected>>", self._on_change)
        
    
        # --- 
        self.sort_reverse_var = tk.BooleanVar(value=False)
        self.chk_desc = ttk.Checkbutton(
            self.frame, text=self.controller.t("lbl_sort_desc"),
            variable=self.sort_reverse_var, command=self._on_change,
        )
        self.chk_desc.grid(row=0, column=8, sticky="w", **pad)

        self.btn_clear = ttk.Button(
            self.frame, text=self.controller.t("btn_clear_filters"),
            command=self.clear,
        )
        self.btn_clear.grid(row=0, column=9, sticky="w", **pad)

        # Allow genre entry column to absorb spare horizontal space.
        self.frame.columnconfigure(5, weight=1)

    # Відслідковує чи щось змінилось 
    def _on_change(self, event=None):
        if self.on_filter_change:
            self.on_filter_change()

    def get_filter_state(self) -> dict:
        return {
            "media_type": self.type_var.get() or None,
            "status": self.status_var.get() or None,
            "genre": self.genre_var.get().strip() or None,
            "sort_key": self.sort_var.get() or "title",
            "sort_reverse": self.sort_reverse_var.get(),
        }

    
    def refresh_labels(self, controller):
        self.lbl_type.configure(text=controller.t("lbl_filter_type"))
        self.lbl_status.configure(text=controller.t("lbl_filter_status"))
        self.lbl_genre.configure(text=controller.t("lbl_filter_genre"))
        self.lbl_sort.configure(text=controller.t("lbl_sort_by"))
        self.chk_desc.configure(text=controller.t("lbl_sort_desc"))
        self.btn_clear.configure(text=controller.t("btn_clear_filters"))

    def refresh_theme(self):
        for lbl in (self.lbl_type, self.lbl_status, self.lbl_genre, self.lbl_sort):
            lbl.configure(foreground=THEME["text_dim"])

    def clear(self):
        self.type_var.set("")
        self.status_var.set("")
        self.genre_var.set("")
        self.sort_var.set(SORT_KEYS[0])
        self.sort_reverse_var.set(False)
        self._on_change()


# ── StatsView ─────────────────────────────────────────────────────────────────

class StatsView:
    # Mapping from internal media type key to locale key.
    _TYPE_LOCALE_KEYS: dict[str, str] = {
        MEDIA_BOOK: "type_book",
        MEDIA_MANGA: "type_manga",
        MEDIA_ANIME: "type_anime",
    }

    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent, padding=20)
        self._build()

    def _build(self):
        frame = self.frame

        self.lbl_header = tk.Label(
            frame, text=self.controller.t("stats_header"),
            bg=THEME["bg"], fg=THEME["text"],
            font=("Segoe UI", 14, "bold"),
        )
        self.lbl_header.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        self.lbl_total_key = self._lbl(frame, "stats_total", dim=True)
        self.lbl_total_key.grid(row=1, column=0, sticky="w", padx=(0, 8))
        self.lbl_total_val = self._big_label(frame, "—")
        self.lbl_total_val.grid(row=1, column=1, sticky="w", padx=(0, 30))

        self.lbl_avg_key = self._lbl(frame, "stats_avg_rating", dim=True)
        self.lbl_avg_key.grid(row=1, column=2, sticky="w", padx=(0, 8))
        self.lbl_avg_val = self._big_label(frame, "—")
        self.lbl_avg_val.grid(row=1, column=3, sticky="w")

        self.lbl_by_type = self._lbl(frame, "stats_by_type")
        self.lbl_by_type.grid(row=2, column=0, columnspan=4, sticky="w", pady=(20, 5))

        self._type_labels: dict[str, tk.Label] = {}
        self._type_bars: dict[str, ttk.Progressbar] = {}
        self._type_counts: dict[str, tk.Label] = {}
        for i, media_key in enumerate((MEDIA_BOOK, MEDIA_MANGA, MEDIA_ANIME)):
            display = self.controller.t(self._TYPE_LOCALE_KEYS[media_key])
            lbl = tk.Label(frame, text=display, bg=THEME["bg"], fg=THEME["text"],
                           font=("Segoe UI", 10), width=12, anchor="w")
            lbl.grid(row=3 + i, column=0, sticky="w", pady=3)
            bar = ttk.Progressbar(frame, orient="horizontal", length=220,
                                  mode="determinate", maximum=100,
                                  style="green.Horizontal.TProgressbar")
            bar.grid(row=3 + i, column=1, columnspan=2, sticky="ew", padx=8, pady=3)
            cnt = tk.Label(frame, text="0", bg=THEME["bg"], fg=THEME["text_dim"],
                           font=("Segoe UI", 10), width=6, anchor="w")
            cnt.grid(row=3 + i, column=3, sticky="w")
            self._type_labels[media_key] = lbl
            self._type_bars[media_key] = bar
            self._type_counts[media_key] = cnt

        self.lbl_by_status = self._lbl(frame, "stats_by_status")
        self.lbl_by_status.grid(row=6, column=0, columnspan=4, sticky="w", pady=(20, 5))

        self._status_color_keys = {
            "Переглянуто": "success",
            "В процесі": "warning",
            "Заплановано": "text_dim",
            "Покинуто": "highlight",
        }
        self._status_locale_keys = {
            "Переглянуто": "status_watched",
            "В процесі": "status_ongoing",
            "Заплановано": "status_planned",
            "Покинуто": "status_dropped",
        }
        self._status_name_labels: dict[str, tk.Label] = {}
        self._status_labels: dict[str, tk.Label] = {}
        for i, (status, color_key) in enumerate(self._status_color_keys.items()):
            name_lbl = tk.Label(frame, text=status, bg=THEME["bg"], fg=THEME[color_key],
                                font=("Segoe UI", 10), width=16, anchor="w")
            name_lbl.grid(row=7 + i, column=0, sticky="w", pady=2)
            cnt = tk.Label(frame, text="0", bg=THEME["bg"], fg=THEME[color_key],
                           font=("Segoe UI", 10, "bold"), width=6, anchor="w")
            cnt.grid(row=7 + i, column=1, sticky="w")
            self._status_name_labels[status] = name_lbl
            self._status_labels[status] = cnt

        frame.columnconfigure(1, weight=1)

    def _lbl(self, parent, key: str, dim: bool = False) -> tk.Label:
        color = THEME["text_dim"] if dim else THEME["text"]
        return tk.Label(parent, text=self.controller.t(key),
                        bg=THEME["bg"], fg=color, font=("Segoe UI", 10))

    def _big_label(self, parent, text: str) -> tk.Label:
        return tk.Label(parent, text=text, bg=THEME["bg"],
                        fg=THEME["highlight"], font=("Segoe UI", 16, "bold"))

    def update_stats(self, stats: dict):
        total = stats.get("total", 0)
        self.lbl_total_val.configure(text=str(total))
        avg = stats.get("avg_rating")
        self.lbl_avg_val.configure(text=f"{avg:.1f}" if avg is not None else "—")

        by_type = stats.get("by_type", {})
        for key, bar in self._type_bars.items():
            count = by_type.get(key, 0)
            pct = int(count / total * 100) if total else 0
            bar["value"] = pct
            self._type_counts[key].configure(text=f"{count} ({pct}%)")

        by_status = stats.get("by_status", {})
        for status, lbl in self._status_labels.items():
            lbl.configure(text=str(by_status.get(status, 0)))

    def refresh_labels(self, controller):
        self.lbl_header.configure(text=controller.t("stats_header"))
        self.lbl_total_key.configure(text=controller.t("stats_total"))
        self.lbl_avg_key.configure(text=controller.t("stats_avg_rating"))
        self.lbl_by_type.configure(text=controller.t("stats_by_type"))
        self.lbl_by_status.configure(text=controller.t("stats_by_status"))
        for media_key, lbl in self._type_labels.items():
            lbl.configure(text=controller.t(self._TYPE_LOCALE_KEYS[media_key]))
        for status, lbl in self._status_name_labels.items():
            lbl.configure(text=controller.t(self._status_locale_keys[status]))

    def refresh_theme(self):
        for w in self.frame.winfo_children():
            if isinstance(w, tk.Label):
                w.configure(bg=THEME["bg"])
        self.lbl_header.configure(fg=THEME["text"])
        self.lbl_total_key.configure(fg=THEME["text_dim"])
        self.lbl_avg_key.configure(fg=THEME["text_dim"])
        self.lbl_total_val.configure(bg=THEME["bg"], fg=THEME["highlight"])
        self.lbl_avg_val.configure(bg=THEME["bg"], fg=THEME["highlight"])
        self.lbl_by_type.configure(fg=THEME["text"])
        self.lbl_by_status.configure(fg=THEME["text"])
        for lbl in self._type_labels.values():
            lbl.configure(bg=THEME["bg"], fg=THEME["text"])
        for cnt in self._type_counts.values():
            cnt.configure(bg=THEME["bg"], fg=THEME["text_dim"])
        for status, color_key in self._status_color_keys.items():
            self._status_name_labels[status].configure(bg=THEME["bg"], fg=THEME[color_key])
            self._status_labels[status].configure(bg=THEME["bg"], fg=THEME[color_key])


# ── AnalyticsView ─────────────────────────────────────────────────────────────

class AnalyticsView:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ttk.Frame(parent, padding=20)
        self._build()

    def _build(self):
        frame = self.frame

        self.lbl_top5 = tk.Label(frame, text=self.controller.t("analytics_top5"),
                                 bg=THEME["bg"], fg=THEME["text"],
                                 font=("Segoe UI", 14, "bold"))
        self.lbl_top5.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        tree_frame.columnconfigure(1, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.top5_tree = ttk.Treeview(
            tree_frame,
            columns=("rank", "title", "type", "rating"),
            show="headings", height=12,
        )
        self.top5_tree.heading("rank", text="#")
        self.top5_tree.heading("title", text=self.controller.t("col_title"))
        self.top5_tree.heading("type", text=self.controller.t("col_type"))
        self.top5_tree.heading("rating", text=self.controller.t("col_rating"))
        self.top5_tree.column("rank", width=40, anchor="center", minwidth=30)
        self.top5_tree.column("title", width=700, anchor="w", minwidth=120)
        self.top5_tree.column("type", width=90, anchor="center", minwidth=60)
        self.top5_tree.column("rating", width=70, anchor="center", minwidth=50)

        sb = ttk.Scrollbar(tree_frame, orient="vertical",
                           command=self.top5_tree.yview)
        self.top5_tree.configure(yscrollcommand=sb.set)
        self.top5_tree.grid(row=0, column=0, columnspan=2, sticky="nsew")
        sb.grid(row=0, column=2, sticky="ns")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

    def get_period_selection(self) -> tuple[int | None, int | None]:
        return None, None

    def update_analytics(self, data: dict):
        self.top5_tree.delete(*self.top5_tree.get_children())
        for i, d in enumerate(data.get("top_rated", []), start=1):
            rating = d.get("rating")
            self.top5_tree.insert("", "end", values=(
                i,
                d.get("title", ""),
                d.get("media_type", ""),
                str(rating) if rating is not None else "—",
            ))

    def refresh_labels(self, controller):
        self.lbl_top5.configure(text=controller.t("analytics_top5"))
        self.top5_tree.heading("title", text=controller.t("col_title"))
        self.top5_tree.heading("type", text=controller.t("col_type"))
        self.top5_tree.heading("rating", text=controller.t("col_rating"))

    def refresh_theme(self):
        self.lbl_top5.configure(bg=THEME["bg"], fg=THEME["text"])


# ── MainView ──────────────────────────────────────────────────────────────────

class MainView:
    def __init__(self, root: tk.Tk, controller):
        self.root = root
        self.controller = controller
        self._setup_window()
        self._setup_styles()
        self._build_menu()
        self._build_notebook()
        self._bind_shortcuts()

    def _setup_window(self):
        self.root.title(self.controller.t("app_title"))
        self.root.configure(bg=THEME["bg"])
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(
            f"{_WIN_WIDTH}x{_WIN_HEIGHT}"
            f"+{(sw - _WIN_WIDTH) // 2}+{(sh - _WIN_HEIGHT) // 2}"
        )
        self.root.minsize(_WIN_MIN_W, _WIN_MIN_H)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Фон
        style.configure(".", background=THEME["bg"], foreground=THEME["text"],
                        font=("Segoe UI", 10))
        style.configure("TFrame", background=THEME["bg"])
        # Підписи заголовки бек для всіх/  пошук
        style.configure("TLabel", background=THEME["bg"], foreground=THEME["text"])
        
        #butt back
        style.configure("TButton", background=THEME["accent"], foreground=THEME["text"],
                        padding=(10, 5), relief="flat", borderwidth=0)
        
        style.map("TButton",
                  background=[("active", THEME["highlight"]), ("pressed", THEME["highlight"])],
                  foreground=[("active", THEME["text"])])
        style.configure("Hover.TButton", background=THEME["highlight"],
                        foreground=THEME["text"])
        
        #button Зберегти
        style.configure("Accent.TButton", background=THEME["highlight"],
                        foreground=THEME["text"])

        #Фон поля введу 
        style.configure("TEntry", fieldbackground=THEME["bg_card"],
                        foreground=THEME["text"], insertcolor=THEME["text"],
                        bordercolor=THEME["accent"])
        style.configure("TSpinbox", fieldbackground=THEME["bg_card"],
                        foreground=THEME["text"], arrowcolor=THEME["text"])
        style.configure("TCombobox", fieldbackground=THEME["bg_card"],
                        foreground=THEME["text"], selectbackground=THEME["accent"],
                        arrowcolor=THEME["text"])
        style.map("TCombobox", fieldbackground=[("readonly", THEME["bg_card"])])

        style.configure("TCheckbutton", background=THEME["bg"],
                        foreground=THEME["text_dim"])
        style.map("TCheckbutton", background=[("active", THEME["bg"])])

        style.configure("TNotebook", background=THEME["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=THEME["accent"],
                        foreground=THEME["text"], padding=(14, 7), font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", THEME["highlight"])],
                  foreground=[("selected", THEME["text"])])

        style.configure("Treeview", background=THEME["bg_card"],
                        foreground=THEME["text"], fieldbackground=THEME["bg_card"],
                        rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background=THEME["accent"],
                        foreground=THEME["text"], font=("Segoe UI", 10, "bold"),
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", THEME["highlight"])],
                  foreground=[("selected", THEME["text"])])

        style.configure("TScrollbar", background=THEME["accent"],
                        troughcolor=THEME["bg_card"], arrowcolor=THEME["text"])
        style.configure("green.Horizontal.TProgressbar",
                        troughcolor=THEME["bg_card"], background=THEME["success"],
                        borderwidth=0)

    def _build_menu(self):
        self.menubar = tk.Menu(self.root, tearoff=0, bg=THEME["bg_card"], fg=THEME["text"],
                               activebackground=THEME["highlight"],
                               activeforeground=THEME["text"], relief="flat")

        self.file_menu = tk.Menu(self.menubar, tearoff=0,
                                 bg=THEME["bg_card"], fg=THEME["text"],
                                 activebackground=THEME["highlight"],
                                 activeforeground=THEME["text"])
        self.file_menu.add_command(label=self.controller.t("menu_export_csv"),
                                   command=self._on_export)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.controller.t("menu_exit"),
                                   command=self.root.quit)
        self.menubar.add_cascade(label=self.controller.t("menu_file"),
                                 menu=self.file_menu)

        self.view_menu = tk.Menu(self.menubar, tearoff=0,
                                 bg=THEME["bg_card"], fg=THEME["text"],
                                 activebackground=THEME["highlight"],
                                 activeforeground=THEME["text"])
        self.view_menu.add_command(label="Українська",
                                   command=lambda: self.controller.set_language("uk"))
        self.view_menu.add_command(label="English",
                                   command=lambda: self.controller.set_language("en"))
        self.view_menu.add_separator()

        self.theme_menu = tk.Menu(self.view_menu, tearoff=0,
                                  bg=THEME["bg_card"], fg=THEME["text"],
                                  activebackground=THEME["highlight"],
                                  activeforeground=THEME["text"])
        self.theme_menu.add_command(label=self.controller.t("menu_theme_dark"),
                                    command=lambda: self.controller.set_theme("dark"))
        self.theme_menu.add_command(label=self.controller.t("menu_theme_light"),
                                    command=lambda: self.controller.set_theme("light"))
        self.view_menu.add_cascade(label=self.controller.t("menu_theme"),
                                   menu=self.theme_menu)
        self.menubar.add_cascade(label=self.controller.t("menu_view"),
                                 menu=self.view_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff=0,
                                 bg=THEME["bg_card"], fg=THEME["text"],
                                 activebackground=THEME["highlight"],
                                 activeforeground=THEME["text"])
        self.help_menu.add_command(label=self.controller.t("menu_about"),
                                   command=self._show_about)
        self.menubar.add_cascade(label=self.controller.t("menu_help"),
                                 menu=self.help_menu)
        self.root.config(menu=self.menubar)

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        
        
        self.collection_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.collection_frame,
                          text=f"  {self.controller.t('tab_collection')}  ")
        self._build_collection_tab()



        self.stats_view = StatsView(self.notebook, self.controller)
        self.notebook.add(self.stats_view.frame,
                          text=f"  {self.controller.t('tab_stats')}  ")


        self.analytics_view = AnalyticsView(self.notebook, self.controller)
        self.notebook.add(self.analytics_view.frame,
                          text=f"  {self.controller.t('tab_analytics')}  ")

    def _build_collection_tab(self):
        tab = self.collection_frame
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

        toolbar = ttk.Frame(tab)
        toolbar.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 0))

        self.btn_add = self._make_button(toolbar, "btn_add", self.controller.on_add)
        self.btn_edit = self._make_button(toolbar, "btn_edit", self.controller.on_edit)
        self.btn_delete = self._make_button(toolbar, "btn_delete", self.controller.on_delete)
        self.btn_export_tb = self._make_button(toolbar, "btn_export", self._on_export)

        self.btn_lang = ttk.Button(toolbar, text=self.controller.t("btn_lang"),
                                   command=self.controller.toggle_language)
        self.btn_lang.pack(side="right", padx=4)
        _bind_hover(self.btn_lang)

        theme_key = ("btn_theme_to_light" if self.controller.current_theme == "dark"
                     else "btn_theme_to_dark")
        self.btn_theme = ttk.Button(toolbar, text=self.controller.t(theme_key),
                                    command=self.controller.toggle_theme)
        self.btn_theme.pack(side="right", padx=4)
        _bind_hover(self.btn_theme)

        search_frame = ttk.Frame(tab)
        search_frame.grid(row=1, column=0, sticky="ew", padx=6, pady=4)
        self.lbl_search = ttk.Label(search_frame, text=self.controller.t("lbl_search"))
        self.lbl_search.pack(side="left", padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left")
        # Live time відстеження оновлення 
        self.search_var.trace_add( 
            "write",
            lambda *_: self.controller.on_search_changed(self.search_var.get()),
        )

        self.filter_view = FilterView(tab, self.controller)
        self.filter_view.frame.grid(row=2, column=0, sticky="ew", padx=6, pady=2)

        tree_frame = ttk.Frame(tab)
        tree_frame.grid(row=3, column=0, sticky="nsew", padx=6, pady=6)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = ("title", "type", "genre", "year", "rating", "status", "added")
        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                 show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=self.controller.t(f"col_{col}"),
                              command=lambda c=col: self.controller.on_sort(c))
        # Клонки
        self.tree.column("title", width=_COL_W_TITLE, anchor="w", minwidth=100)
        self.tree.column("type", width=_COL_W_TYPE, anchor="center", minwidth=55)
        self.tree.column("genre", width=_COL_W_GENRE, anchor="w", minwidth=65)
        self.tree.column("year", width=_COL_W_YEAR, anchor="center", minwidth=60)
        self.tree.column("rating", width=_COL_W_RATING, anchor="center", minwidth=50)
        self.tree.column("status", width=_COL_W_STATUS, anchor="center", minwidth=85)
        self.tree.column("added", width=_COL_W_ADDED, anchor="center", minwidth=75)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # дабл клік, пкм, 
        self.tree.bind("<Double-1>", lambda e: self.controller.on_edit())
        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<<TreeviewSelect>>", lambda e: self.controller.on_selection_changed())

        self.context_menu = tk.Menu(self.root, tearoff=0,
                                    bg=THEME["bg_card"], fg=THEME["text"],
                                    activebackground=THEME["highlight"],
                                    activeforeground=THEME["text"])
        self.context_menu.add_command(label=self.controller.t("btn_edit"),
                                      command=self.controller.on_edit)
        self.context_menu.add_command(label=self.controller.t("btn_delete"),
                                      command=self.controller.on_delete)

    def _bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.controller.on_add())
        self.root.bind("<Control-N>", lambda e: self.controller.on_add())
        self.root.bind("<Control-e>", lambda e: self.controller.on_edit())
        self.root.bind("<Control-E>", lambda e: self.controller.on_edit())
        self.root.bind("<Delete>", lambda e: self._on_delete_key(e))
        self.root.bind("<F5>", lambda e: self.controller.on_refresh())

    def _on_delete_key(self, event):
        if event.widget not in (self.search_entry,):
            self.controller.on_delete()

    def _make_button(self, parent, key: str, command) -> ttk.Button:
        btn = ttk.Button(parent, text=self.controller.t(key), command=command)
        btn.pack(side="left", padx=3, pady=3)
        _bind_hover(btn)
        return btn
    
    # Визначення на який саме рядок було нажато пкм 
    def _show_context_menu(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.selection_set(row)
            self.context_menu.tk_popup(event.x_root, event.y_root)
    # Отримання шляху від користувачу 
    def _on_export(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title=self.controller.t("menu_export_csv"),
        )
        if filepath:
            self.controller.on_export(filepath)

    def _show_about(self):
        messagebox.showinfo("MediaNexus", self.controller.t("msg_about"))

    # Колір 
    def _update_tree_tags(self):
        self.tree.tag_configure("watched", foreground=THEME["success"])
        self.tree.tag_configure("ongoing", foreground=THEME["warning"])
        self.tree.tag_configure("dropped", foreground=THEME["highlight"])
        self.tree.tag_configure("planned", foreground=THEME["text"])

    @staticmethod
    def _fmt_date(iso: str) -> str:
        try:
            return datetime.date.fromisoformat(iso).strftime("%d.%m.%Y")
        except (ValueError, TypeError):
            return iso

    def update_treeview(self, items: list[dict]):
        self._update_tree_tags()
        self.tree.delete(*self.tree.get_children())
        status_tag = {
            "Переглянуто": "watched",
            "В процесі": "ongoing",
            "Покинуто": "dropped",
            "Заплановано": "planned",
        }
        for d in items:
            rating = d.get("rating")
            tag = status_tag.get(d.get("status", ""), "planned")
            added = self._fmt_date(d.get("added_date", ""))
            self.tree.insert(
                "", "end", iid=d["id"],
                tags=(tag,),
                values=(
                    d.get("title", ""),
                    d.get("media_type", ""),
                    d.get("genre", ""),
                    d.get("year", ""),
                    str(rating) if rating is not None else "—",
                    d.get("status", ""),
                    added,
                ),
            )

    def get_selected_item_id(self) -> str | None:
        sel = self.tree.selection()
        return sel[0] if sel else None

    def open_add_edit_dialog(self, item_data: dict | None) -> dict | None:
        dialog = AddEditDialog(self.root, self.controller, item_data)
        self.root.wait_window(dialog.window)
        return dialog.get_result()

    # ── Delegation methods (hide internal sub-view structure from controller) ──

    def update_stats(self, stats: dict) -> None:
        self.stats_view.update_stats(stats)

    def get_period_selection(self) -> tuple[int | None, int | None]:
        return self.analytics_view.get_period_selection()

    def update_analytics(self, data: dict) -> None:
        self.analytics_view.update_analytics(data)

    # Перекладає все через віджети 
    def refresh_all_labels(self, controller):
        self.root.title(controller.t("app_title"))
        self.btn_add.configure(text=controller.t("btn_add"))
        self.btn_edit.configure(text=controller.t("btn_edit"))
        self.btn_delete.configure(text=controller.t("btn_delete"))
        self.btn_export_tb.configure(text=controller.t("btn_export"))
        self.btn_lang.configure(text=controller.t("btn_lang"))
        self.lbl_search.configure(text=controller.t("lbl_search"))

        theme_key = ("btn_theme_to_light" if controller.current_theme == "dark"
                     else "btn_theme_to_dark")
        self.btn_theme.configure(text=controller.t(theme_key))

        self.menubar.entryconfigure(0, label=controller.t("menu_file"))
        self.menubar.entryconfigure(1, label=controller.t("menu_view"))
        self.menubar.entryconfigure(2, label=controller.t("menu_help"))
        self.file_menu.entryconfigure(0, label=controller.t("menu_export_csv"))
        self.file_menu.entryconfigure(2, label=controller.t("menu_exit"))
        self.help_menu.entryconfigure(0, label=controller.t("menu_about"))
        self.theme_menu.entryconfigure(0, label=controller.t("menu_theme_dark"))
        self.theme_menu.entryconfigure(1, label=controller.t("menu_theme_light"))

        self.notebook.tab(self.collection_frame,
                          text=f"  {controller.t('tab_collection')}  ")
        self.notebook.tab(self.stats_view.frame,
                          text=f"  {controller.t('tab_stats')}  ")
        self.notebook.tab(self.analytics_view.frame,
                          text=f"  {controller.t('tab_analytics')}  ")

        for col in ("title", "type", "genre", "year", "rating", "status", "added"):
            self.tree.heading(col, text=controller.t(f"col_{col}"),
                              command=lambda c=col: self.controller.on_sort(c))

        self.context_menu.entryconfigure(0, label=controller.t("btn_edit"))
        self.context_menu.entryconfigure(1, label=controller.t("btn_delete"))

        self.filter_view.refresh_labels(controller)
        self.stats_view.refresh_labels(controller)
        self.analytics_view.refresh_labels(controller)

    # Міняє тему
    def refresh_theme(self):
        self._setup_styles()
        self.root.configure(bg=THEME["bg"])

        for menu in (self.menubar, self.file_menu, self.view_menu,
                     self.theme_menu, self.help_menu):
            menu.configure(bg=THEME["bg_card"], fg=THEME["text"],
                           activebackground=THEME["highlight"],
                           activeforeground=THEME["text"])
        self.context_menu.configure(bg=THEME["bg_card"], fg=THEME["text"],
                                    activebackground=THEME["highlight"],
                                    activeforeground=THEME["text"])

        self.lbl_search.configure(foreground=THEME["text"])
        self._update_tree_tags()

        self.filter_view.refresh_theme()
        self.stats_view.refresh_theme()
        self.analytics_view.refresh_theme()
