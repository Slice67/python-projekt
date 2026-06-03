from __future__ import annotations

from typing import Callable

from models.events import Event
from ui.crud_widgets import CrudAction, CrudColumn, CrudTableFrame


class EventsView(CrudTableFrame):
    """Tabulka akcí s ovládacími tlačítky."""

    COLUMNS = (
        CrudColumn("id", "ID", 45, anchor="center"),
        CrudColumn("title", "Název", 170),
        CrudColumn("event_type", "Typ", 125),
        CrudColumn("start_time", "Začátek", 125, anchor="center"),
        CrudColumn("end_time", "Konec", 125, anchor="center"),
        CrudColumn("visitor_count", "Návštěvníci", 90, anchor="center"),
        CrudColumn("client", "Klient", 170),
        CrudColumn("room", "Místnost", 140),
        CrudColumn("staff", "Zaměstnanec", 150),
        CrudColumn("program", "Program", 170),
        CrudColumn("status", "Status", 90, anchor="center"),
    )

    def __init__(
        self,
        master,
        on_refresh: Callable[[], None],
        on_add: Callable[[], None],
        on_edit: Callable[[], None] | None,
        on_delete: Callable[[], None],
        on_export: Callable[[], None],
    ):
        super().__init__(
            master,
            columns=list(self.COLUMNS),
            on_refresh=on_refresh,
            on_add=on_add,
            on_delete=on_delete,
            on_edit=on_edit,
            add_label="Přidat akci",
            edit_label="Upravit akci",
            delete_label="Smazat akci",
            extra_actions=[CrudAction("Export CSV", on_export)],
            horizontal_scrollbar=True,
            striped_rows=True,
        )

    def get_selected_event_id(self) -> int | None:
        return self.get_selected_id()

    def set_events(
        self,
        events: list[Event],
        client_names: dict[int, str],
        room_names: dict[int, str],
        staff_names: dict[int, str],
        program_names: dict[int, str],
    ) -> None:
        self.set_rows([
            {
                "id": event.id,
                "title": event.title,
                "event_type": event.event_type,
                "start_time": event.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time": event.end_time.strftime("%Y-%m-%d %H:%M"),
                "visitor_count": event.visitor_count,
                "client": self._label(event.client_id, client_names),
                "room": self._label(event.room_id, room_names),
                "staff": self._label(event.staff_id, staff_names),
                "program": self._label(event.program_id, program_names),
                "status": event.status,
            }
            for event in events
        ])

    @staticmethod
    def _label(entity_id: int, names: dict[int, str]) -> str:
        return names.get(entity_id, str(entity_id))
