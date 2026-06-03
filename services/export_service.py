import csv
from pathlib import Path

from models.events import Event

class ExportService:
    """Service pro export dat aplikace do CSV"""

    def __init__(self, export_dir: str = "exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_events_to_csv(
            self,
            events: list[Event],
            filename: str = "events_export.csv",
            client_names: dict[int, str] | None = None,
            room_names: dict[int, str] | None = None,
            staff_names: dict[int, str] | None = None,
            program_names: dict[int, str] | None = None,
        ) -> Path:
        """Exportuje seznam akcí do CSV souboru a vrací cestu k exportovanému souboru."""

        file_path = self.export_dir / filename

        with file_path.open(mode='w', newline='', encoding='utf-8') as file:
            fieldnames =[
                "id",
                "title",
                "event_type",
                "start_time",
                "end_time",
                "visitor_count",
                "client_name",
                "room_name",
                "staff_name",
                "program_name",
                "status",
                "description",
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
                delimiter=";"
            )

            writer.writeheader()

            for event in events:
                writer.writerow({
                    "id": event.id,
                    "title": event.title,
                    "event_type": event.event_type,
                    "start_time": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_time": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "visitor_count": event.visitor_count,
                    "client_name": self._resolve_label(event.client_id, client_names),
                    "room_name": self._resolve_label(event.room_id, room_names),
                    "staff_name": self._resolve_label(event.staff_id, staff_names),
                    "program_name": self._resolve_label(event.program_id, program_names),
                    "status": event.status,
                    "description": event.description or "",
                })

        return file_path

    @staticmethod # pro zjednodušení získávání názvů z ID
    def _resolve_label(entity_id: int, names: dict[int, str] | None) -> str:
        if names is None:
            return str(entity_id)

        return names.get(entity_id, str(entity_id))