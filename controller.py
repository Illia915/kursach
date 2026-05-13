import datetime
from tkinter import messagebox
from models import CollectionModel, MediaItem
from locales import LOCALES, DEFAULT_LANG, DEFAULT_THEME, THEME, THEMES


class MainController:
    def __init__(self, model: CollectionModel):
        self.model = model
        self.view = None
        self.current_lang = DEFAULT_LANG
        self.current_theme = DEFAULT_THEME
        self._search_query = ""
        self._active_filters: dict = {}

    def set_view(self, view) -> None:
        self.view = view
        self.view.filter_view.on_filter_change = self.on_filter_changed

    # ── Translation ───────────────────────────────────────────────────────────

    def t(self, key: str) -> str:
        return LOCALES[self.current_lang].get(key, key)

    def set_language(self, lang: str) -> None:
        self.current_lang = lang
        self.view.refresh_all_labels(self)

    def toggle_language(self) -> None:
        self.set_language("en" if self.current_lang == "uk" else "uk")

    # ── Theme ─────────────────────────────────────────────────────────────────

    def set_theme(self, theme_name: str) -> None:
        THEME.update(THEMES[theme_name])
        self.current_theme = theme_name
        self.view.refresh_theme()
        self.view.refresh_all_labels(self)

    def toggle_theme(self) -> None:
        self.set_theme("light" if self.current_theme == "dark" else "dark")

    # ── Startup ───────────────────────────────────────────────────────────────

    def startup(self) -> None:
        try:
            self.model.load()
        except ValueError as e:
            messagebox.showerror("Load Error", str(e))
        self._refresh_treeview()
        self._refresh_stats()

    def _apply_filters(self) -> list[MediaItem]:
        items = self.model.get_all()
        if self._search_query:
            items = self.model.search(self._search_query, items)
        f = self._active_filters
        items = self.model.filter_items(
            items,
            media_type=f.get("media_type"),
            status=f.get("status"),
            genre=f.get("genre"),
        )
        items = self.model.sort_items(
            items,
            key=f.get("sort_key", "title"),
            reverse=f.get("sort_reverse", False),
        )
        return items

    def _refresh_treeview(self) -> None:
        items = self._apply_filters()
        self.view.update_treeview([it.to_dict() for it in items])

    def _refresh_stats(self) -> None:
        stats = self.model.get_statistics()
        self.view.stats_view.update_stats(stats)
        self._refresh_analytics()

    def _refresh_analytics(self) -> None:
        year, month = self.view.analytics_view.get_period_selection()
        data = self.model.get_analytics(year=year, month=month)
        self.view.analytics_view.update_analytics({
            "completed_count": data["completed_count"],
            "top5_rated": [it.to_dict() for it in data["top5_rated"]],
        })

    # ── Event handlers ────────────────────────────────────────────────────────

    def on_add(self) -> None:
        result = self.view.open_add_edit_dialog(None)
        if result is None:
            return
        item = self._dict_to_mediaitem(result)
        self.model.add_item(item)
        self._refresh_treeview()
        self._refresh_stats()

    def on_edit(self) -> None:
        item_id = self.view.get_selected_item_id()
        if not item_id:
            messagebox.showwarning("", self.t("err_no_selection"))
            return
        item = self.model.get_by_id(item_id)
        if item is None:
            return
        result = self.view.open_add_edit_dialog(item.to_dict())
        if result is None:
            return
        result["id"] = item_id
        updated = self._dict_to_mediaitem(result, original_item=item)
        self.model.update_item(updated)
        self._refresh_treeview()
        self._refresh_stats()

    def on_delete(self) -> None:
        item_id = self.view.get_selected_item_id()
        if not item_id:
            messagebox.showwarning("", self.t("err_no_selection"))
            return
        item = self.model.get_by_id(item_id)
        if item is None:
            return
        confirm = messagebox.askyesno(
            self.t("btn_delete"),
            self.t("confirm_delete").format(title=item.title),
        )
        if confirm:
            self.model.delete_item(item_id)
            self._refresh_treeview()
            self._refresh_stats()

    def on_search_changed(self, query: str) -> None:
        self._search_query = query.strip()
        self._refresh_treeview()

    def on_filter_changed(self) -> None:
        self._active_filters = self.view.filter_view.get_filter_state()
        self._refresh_treeview()

    def on_sort(self, column: str) -> None:
        current_key = self._active_filters.get("sort_key", "title")
        current_rev = self._active_filters.get("sort_reverse", False)
        if current_key == column:
            self._active_filters["sort_reverse"] = not current_rev
        else:
            self._active_filters["sort_key"] = column
            self._active_filters["sort_reverse"] = False
        self._refresh_treeview()

    def on_export(self, filepath: str) -> None:
        items = self._apply_filters()
        try:
            self.model.export_csv(filepath, items)
            messagebox.showinfo("", self.t("msg_export_success"))
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def on_refresh(self) -> None:
        self._refresh_treeview()
        self._refresh_stats()

    def on_selection_changed(self) -> None:
        pass

    def on_analytics_period_changed(self) -> None:
        self._refresh_analytics()

    # ── Validation ────────────────────────────────────────────────────────────

    def validate_item_form(self, data: dict) -> tuple[bool, str | None]:
        title = data.get("title", "").strip()
        if not title:
            return False, self.t("err_title_empty")

        genre = data.get("genre", "").strip()
        if genre and any(c.isdigit() for c in genre):
            return False, self.t("err_genre_invalid")

        try:
            year_int = int(data.get("year", 0))
            if not (1900 <= year_int <= 2030):
                raise ValueError
            data["year"] = year_int
        except (ValueError, TypeError):
            return False, self.t("err_year_invalid")

        try:
            rating_raw = data.get("rating", 0)
            r = int(rating_raw)
            if not (0 <= r <= 10):
                raise ValueError
            data["rating"] = None if r == 0 else r
        except (ValueError, TypeError):
            return False, self.t("err_rating_invalid")

        return True, None

    # ── Conversion ────────────────────────────────────────────────────────────

    def _dict_to_mediaitem(
        self,
        d: dict,
        original_item: MediaItem | None = None,
    ) -> MediaItem:
        completed_date = d.get("completed_date", "")
        if d.get("status") == "Переглянуто":
            if original_item is None or original_item.status != "Переглянуто":
                completed_date = datetime.date.today().isoformat()
            elif original_item.completed_date:
                completed_date = original_item.completed_date
        elif original_item is not None:
            completed_date = original_item.completed_date

        kwargs = {
            "title":          d.get("title", "").strip(),
            "media_type":     d.get("media_type", "book"),
            "genre":          d.get("genre", "").strip(),
            "year":           int(d.get("year", 0)),
            "description":    d.get("description", "").strip(),
            "rating":         d.get("rating"),
            "status":         d.get("status", "Заплановано"),
            "completed_date": completed_date,
            "added_date":     d.get("added_date", ""),
        }
        if d.get("id"):
            kwargs["id"] = d["id"]
        return MediaItem(**kwargs)
