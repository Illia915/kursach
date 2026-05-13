THEMES = {
    # Nord-inspired: cool neutral darks, no neon, no clashing brights
    "dark": {
        "bg":        "#242933",
        "bg_card":   "#2e3440",
        "accent":    "#3b4252",
        "highlight": "#81a1c1",
        "text":      "#d8dee9",
        "text_dim":  "#677489",
        "success":   "#a3be8c",
        "warning":   "#ebcb8b",
    },
    # Warm morning: cream background, slate-blue accents, terracotta highlights
    "light": {
        "bg":        "#f5f0e8",
        "bg_card":   "#fffef9",
        "accent":    "#8b9dc3",
        "highlight": "#c97b5a",
        "text":      "#2d2a26",
        "text_dim":  "#7a7168",
        "success":   "#4f8f63",
        "warning":   "#b58c30",
    },
}

# Mutable — updated in-place on theme switch
THEME: dict = dict(THEMES["dark"])

MEDIA_TYPES = ["book", "manga", "anime"]
STATUSES = ["Переглянуто", "В процесі", "Заплановано", "Покинуто"]
SORT_KEYS = ["title", "rating", "year"]
DEFAULT_LANG = "uk"
DEFAULT_THEME = "dark"

LOCALES = {
    "uk": {
        "app_title":   "MediaNexus — Медіа Колекція",
        "tab_collection": "Колекція",
        "tab_stats":      "Статистика",
        "tab_analytics":  "Аналітика",

        "btn_add":    "➕ Додати",
        "btn_edit":   "✏️ Редагувати",
        "btn_delete": "🗑 Видалити",
        "btn_export": "📤 Експорт CSV",
        "btn_save":   "Зберегти",
        "btn_cancel": "Скасувати",
        "btn_lang":   "🌐 EN",
        "btn_clear_filters": "Скинути фільтри",
        "btn_show":   "Показати",
        "btn_theme_to_light": "☀️ Світла",
        "btn_theme_to_dark":  "🌙 Темна",

        "menu_file":       "Файл",
        "menu_export_csv": "Експорт у CSV…",
        "menu_exit":       "Вихід",
        "menu_view":       "Вигляд",
        "menu_language":   "Мова",
        "menu_theme":      "Тема",
        "menu_theme_dark":  "🌙 Темна",
        "menu_theme_light": "☀️ Світла",
        "menu_help":       "Довідка",
        "menu_about":      "Про програму",

        "col_title":  "Назва",
        "col_type":   "Тип",
        "col_genre":  "Жанр",
        "col_year":   "Рік",
        "col_rating": "Оцінка",
        "col_status": "Статус",
        "col_added":  "Додано",

        "dlg_add_title":  "Додати запис",
        "dlg_edit_title": "Редагувати запис",
        "lbl_title":      "Назва *",
        "lbl_type":       "Тип",
        "lbl_genre":      "Жанр",
        "lbl_year":       "Рік",
        "lbl_month":      "Місяць виходу",
        "lbl_desc":       "Опис",
        "lbl_rating":     "Оцінка (0 = не оцінено)",
        "lbl_status":     "Статус",

        "lbl_search":        "🔍 Пошук:",
        "lbl_filter_type":   "Тип:",
        "lbl_filter_status": "Статус:",
        "lbl_filter_genre":  "Жанр:",
        "lbl_sort_by":       "Сортування:",
        "lbl_sort_desc":     "↓ За спаданням",
        "opt_all":           "Всі",

        "stats_header":       "Загальна статистика",
        "stats_total":        "Всього записів:",
        "stats_avg_rating":   "Середня оцінка:",
        "stats_by_type":      "Розподіл за типом",
        "stats_by_status":    "Розподіл за статусом",
        "stats_no_data":      "Немає даних",

        "analytics_header":          "Аналітика за періодом",
        "analytics_year":            "Рік:",
        "analytics_month":           "Місяць:",
        "analytics_show":            "Показати",
        "analytics_completed_count": "Завершено за період:",
        "analytics_top5":            "Топ-10 за оцінкою",
        "analytics_no_data":         "Немає даних для обраного періоду",

        "status_watched": "Переглянуто",
        "status_ongoing": "В процесі",
        "status_planned": "Заплановано",
        "status_dropped": "Покинуто",

        "err_title_empty":   "Назва не може бути порожньою.",
        "err_year_invalid":  "Рік має бути числом від 1900 до 2030.",
        "err_rating_invalid":"Оцінка має бути числом від 0 до 10.",
        "err_genre_invalid": "Жанр не може містити цифри.",
        "err_no_selection":  "Оберіть запис у списку.",
        "confirm_delete":    "Видалити «{title}»?",
        "msg_export_success":"Колекцію успішно експортовано.",
        "msg_about": (
            "MediaNexus v1.0\n\n"
            "Десктопний менеджер медіа-колекції.\n"
            "Книги · Манґа · Аніме\n\n"
            "Python + Tkinter · MVC · JSON"
        ),

        "months": [
            "Січень", "Лютий", "Березень", "Квітень",
            "Травень", "Червень", "Липень", "Серпень",
            "Вересень", "Жовтень", "Листопад", "Грудень",
        ],
        "sort_title":  "Назва",
        "sort_rating": "Оцінка",
        "sort_year":   "Рік",
    },

    "en": {
        "app_title":   "MediaNexus — Media Collection",
        "tab_collection": "Collection",
        "tab_stats":      "Statistics",
        "tab_analytics":  "Analytics",

        "btn_add":    "➕ Add",
        "btn_edit":   "✏️ Edit",
        "btn_delete": "🗑 Delete",
        "btn_export": "📤 Export CSV",
        "btn_save":   "Save",
        "btn_cancel": "Cancel",
        "btn_lang":   "🌐 УК",
        "btn_clear_filters": "Clear Filters",
        "btn_show":   "Show",
        "btn_theme_to_light": "☀️ Light",
        "btn_theme_to_dark":  "🌙 Dark",

        "menu_file":       "File",
        "menu_export_csv": "Export to CSV…",
        "menu_exit":       "Exit",
        "menu_view":       "View",
        "menu_language":   "Language",
        "menu_theme":      "Theme",
        "menu_theme_dark":  "🌙 Dark",
        "menu_theme_light": "☀️ Light",
        "menu_help":       "Help",
        "menu_about":      "About",

        "col_title":  "Title",
        "col_type":   "Type",
        "col_genre":  "Genre",
        "col_year":   "Year",
        "col_rating": "Rating",
        "col_status": "Status",
        "col_added":  "Added",

        "dlg_add_title":  "Add Record",
        "dlg_edit_title": "Edit Record",
        "lbl_title":      "Title *",
        "lbl_type":       "Type",
        "lbl_genre":      "Genre",
        "lbl_year":       "Year",
        "lbl_month":      "Release Month",
        "lbl_desc":       "Description",
        "lbl_rating":     "Rating (0 = unrated)",
        "lbl_status":     "Status",

        "lbl_search":        "🔍 Search:",
        "lbl_filter_type":   "Type:",
        "lbl_filter_status": "Status:",
        "lbl_filter_genre":  "Genre:",
        "lbl_sort_by":       "Sort by:",
        "lbl_sort_desc":     "↓ Descending",
        "opt_all":           "All",

        "stats_header":       "Collection Statistics",
        "stats_total":        "Total records:",
        "stats_avg_rating":   "Average rating:",
        "stats_by_type":      "By Type",
        "stats_by_status":    "By Status",
        "stats_no_data":      "No data",

        "analytics_header":          "Analytics by Period",
        "analytics_year":            "Year:",
        "analytics_month":           "Month:",
        "analytics_show":            "Show",
        "analytics_completed_count": "Completed in period:",
        "analytics_top5":            "Top-10 by Rating",
        "analytics_no_data":         "No data for selected period",

        "status_watched": "Watched",
        "status_ongoing": "In Progress",
        "status_planned": "Planned",
        "status_dropped": "Dropped",

        "err_title_empty":   "Title cannot be empty.",
        "err_year_invalid":  "Year must be a number between 1900 and 2030.",
        "err_rating_invalid":"Rating must be a number from 0 to 10.",
        "err_genre_invalid": "Genre must not contain digits.",
        "err_no_selection":  "Please select a record from the list.",
        "confirm_delete":    "Delete \"{title}\"?",
        "msg_export_success":"Collection exported successfully.",
        "msg_about": (
            "MediaNexus v1.0\n\n"
            "Desktop media collection manager.\n"
            "Books · Manga · Anime\n\n"
            "Python + Tkinter · MVC · JSON"
        ),

        "months": [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December",
        ],
        "sort_title":  "Title",
        "sort_rating": "Rating",
        "sort_year":   "Year",
    },
}
