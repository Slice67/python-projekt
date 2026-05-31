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
            filename: str= "events_export.csv"
        ) -> Path:
        """Exportuje seznam akcí do CSV souboru a vrací cestu k exportovanému souboru."""

        file_path= self.export_dir / filename # Vytvoření cesty k exportovanému souboru, / je operátor pro spojování cest

        with file_path.open(mode='w', newline='', encoding='utf-8') as file:
            fieldnames =[
                "id",
                "title",
                "event_type",
                "start_time",
                "end_time",
                "visitor_count",
                "client_id",
                "room_id",
                "staff_id",
                "program_id",
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
                    "client_id": event.client_id,
                    "room_id": event.room_id,
                    "staff_id": event.staff_id,
                    "program_id": event.program_id,
                    "status": event.status,
                    "description": event.description or "",
                })

        return file_path