from dataclasses import dataclass, field
import uuid
import json
import csv
import os
import datetime


@dataclass
class MediaItem:
    title: str
    media_type: str
    genre: str = ""
    year: int = 0
    description: str = ""
    rating: int | None = None
    status: str = "Заплановано"
    completed_date: str = ""
    added_date: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "media_type": self.media_type,
            "genre": self.genre,
            "year": self.year,
            "description": self.description,
            "rating": self.rating,
            "status": self.status,
            "completed_date": self.completed_date,
            "added_date": self.added_date,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "MediaItem":
        rating = d.get("rating")
        if rating is not None:
            try:
                rating = int(rating)
            except (ValueError, TypeError):
                rating = None
        year = d.get("year", 0)
        try:
            year = int(year)
        except (ValueError, TypeError):
            year = 0
        return cls(
            id=d.get("id", str(uuid.uuid4())),
            title=d.get("title", ""),
            media_type=d.get("media_type", "book"),
            genre=d.get("genre", ""),
            year=year,
            description=d.get("description", ""),
            rating=rating,
            status=d.get("status", "Заплановано"),
            completed_date=d.get("completed_date", ""),
            added_date=d.get("added_date", ""),
        )


class CollectionModel:
    def __init__(self, filepath: str = "collection.json"):
        self.filepath = filepath
        self._items: list[MediaItem] = []

    # ── Persistence ───────────────────────────────────────────────────────────

    def load(self) -> None:
        dir_ = os.path.dirname(self.filepath)
        if dir_:
            os.makedirs(dir_, exist_ok=True)
        if not os.path.exists(self.filepath):
            self._items = []
            return
        try:
            with open(self.filepath, encoding="utf-8") as f:
                data = json.load(f)
            self._items = [MediaItem.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            self._items = []
            raise ValueError(f"Не вдалося завантажити колекцію: {e}") from e

    def save(self) -> None:
        dir_ = os.path.dirname(self.filepath)
        if dir_:
            os.makedirs(dir_, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in self._items],
                      f, ensure_ascii=False, indent=2)

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def add_item(self, item: MediaItem) -> None:
        if not item.added_date:
            item.added_date = datetime.date.today().isoformat()
        self._items.append(item)
        self.save()

    def update_item(self, item: MediaItem) -> None:
        for i, existing in enumerate(self._items):
            if existing.id == item.id:
                self._items[i] = item
                self.save()
                return
        raise KeyError(f"Item with id={item.id} not found")

    def delete_item(self, item_id: str) -> None:
        before = len(self._items)
        self._items = [it for it in self._items if it.id != item_id]
        if len(self._items) == before:
            raise KeyError(f"Item with id={item_id} not found")
        self.save()

    def get_by_id(self, item_id: str) -> MediaItem | None:
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def get_all(self) -> list[MediaItem]:
        return list(self._items)

    # ── Query ─────────────────────────────────────────────────────────────────

    def search(self, query: str, items: list[MediaItem] | None = None) -> list[MediaItem]:
        if items is None:
            items = self._items
        q = query.lower().strip()
        if not q:
            return list(items)
        return [it for it in items
                if q in it.title.lower() or q in it.genre.lower()]

    def filter_items(
        self,
        items: list[MediaItem],
        media_type: str | None = None,
        status: str | None = None,
        genre: str | None = None,
    ) -> list[MediaItem]:
        result = items
        if media_type:
            result = [it for it in result if it.media_type == media_type]
        if status:
            result = [it for it in result if it.status == status]
        if genre:
            result = [it for it in result if genre.lower() in it.genre.lower()]
        return result

    def sort_items(
        self,
        items: list[MediaItem],
        key: str = "title",
        reverse: bool = False,
    ) -> list[MediaItem]:
        if key == "title":
            return sorted(items, key=lambda it: it.title.lower(), reverse=reverse)
        if key == "rating":
            return sorted(
                items,
                key=lambda it: (it.rating is None, -(it.rating or 0) if reverse else (it.rating or 0)),
                reverse=False,
            )
        if key == "year":
            return sorted(items, key=lambda it: it.year, reverse=reverse)
        return list(items)

    # ── Aggregations ──────────────────────────────────────────────────────────

    def get_statistics(self) -> dict:
        total = len(self._items)
        by_type = {"book": 0, "manga": 0, "anime": 0}
        by_status = {
            "Переглянуто": 0,
            "В процесі":   0,
            "Заплановано": 0,
            "Покинуто":    0,
        }
        rated = [it.rating for it in self._items if it.rating is not None]
        for it in self._items:
            if it.media_type in by_type:
                by_type[it.media_type] += 1
            if it.status in by_status:
                by_status[it.status] += 1
        avg_rating = round(sum(rated) / len(rated), 1) if rated else None
        return {
            "total": total,
            "by_type": by_type,
            "avg_rating": avg_rating,
            "by_status": by_status,
        }

    def get_analytics(
        self,
        year: int | None = None,
        month: int | None = None,
    ) -> dict:
        if year is None and month is None:
            completed_count = sum(
                1 for it in self._items if it.status == "Переглянуто"
            )
            rated = [it for it in self._items if it.rating is not None]
            top10 = sorted(rated, key=lambda it: it.rating, reverse=True)[:10]
            return {"completed_count": completed_count, "top5_rated": top10}

        completed = [
            it for it in self._items
            if it.status == "Переглянуто" and it.completed_date
        ]
        filtered = []
        for it in completed:
            try:
                d = datetime.date.fromisoformat(it.completed_date)
            except ValueError:
                continue
            if year is not None and d.year != year:
                continue
            if month is not None and d.month != month:
                continue
            filtered.append(it)

        rated = [it for it in filtered if it.rating is not None]
        top10 = sorted(rated, key=lambda it: it.rating, reverse=True)[:10]
        return {
            "completed_count": len(filtered),
            "top5_rated": top10,
        }

    # ── Export ────────────────────────────────────────────────────────────────

    def export_csv(self, filepath: str, items: list[MediaItem] | None = None) -> None:
        if items is None:
            items = self._items
        headers = ["ID", "Title", "Type", "Genre", "Year",
                   "Description", "Rating", "Status", "Completed Date", "Added Date"]
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for it in items:
                writer.writerow([
                    it.id, it.title, it.media_type, it.genre, it.year,
                    it.description,
                    it.rating if it.rating is not None else "",
                    it.status, it.completed_date, it.added_date,
                ])
