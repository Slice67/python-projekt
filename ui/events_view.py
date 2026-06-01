from __future__ import annotations

from typing import Callable

from tkinter import ttk

from models.events import Event


class EventsView(ttk.Frame):
    """Tabulka akcí s ovládacími tlačítky."""

    COLUMNS = (
        "id",
        "title",
        "event_type",
        "start_time",
        "end_time",
        "visitor_count",
        "client",
        "room",
        "staff",
        "program",
        "status",
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
        super().__init__(master, padding=12)
        self.on_refresh = on_refresh
        self.on_add = on_add
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_export = on_export

        self._build_toolbar()
        self._build_table()

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 12))

        ttk.Button(toolbar, text="Obnovit", command=self.on_refresh).pack(side="left")
        ttk.Button(toolbar, text="Přidat akci", command=self.on_add).pack(side="left", padx=(8, 0))

        if self.on_edit is not None:
            ttk.Button(toolbar, text="Upravit akci", command=self.on_edit).pack(side="left", padx=(8, 0))

        ttk.Button(toolbar, text="Smazat akci", command=self.on_delete).pack(side="left", padx=(8, 0))
        ttk.Button(toolbar, text="Export CSV", command=self.on_export).pack(side="left", padx=(8, 0))

    def _build_table(self) -> None:
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.COLUMNS,
            show="headings",
            selectmode="browse",
            height=18,
        )

        headings = {
            "id": "ID",
            "title": "Název",
            "event_type": "Typ",
            "start_time": "Začátek",
            "end_time": "Konec",
            "visitor_count": "Návštěvníci",
            "client": "Klient",
            "room": "Místnost",
            "staff": "Zaměstnanec",
            "program": "Program",
            "status": "Status",
        }

        widths = {
            "id": 45,
            "title": 170,
            "event_type": 125,
            "start_time": 125,
            "end_time": 125,
            "visitor_count": 90,
            "client": 170,
            "room": 140,
            "staff": 150,
            "program": 170,
            "status": 90,
        }

        anchors = {
            "id": "center",
            "title": "w",
            "event_type": "w",
            "start_time": "center",
            "end_time": "center",
            "visitor_count": "center",
            "client": "w",
            "room": "w",
            "staff": "w",
            "program": "w",
            "status": "center",
        }

        for column in self.COLUMNS:
            self.tree.heading(column, text=headings[column])
            self.tree.column(
                column,
                width=widths[column],
                minwidth=widths[column],
                anchor=anchors[column],
                stretch=True,
            )

        self.tree.tag_configure("evenrow", background="#f8f9fa")
        self.tree.tag_configure("oddrow", background="#ffffff")

        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
        )

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

    def get_selected_event_id(self) -> int | None:
        selection = self.tree.selection()
        if not selection:
            return None

        try:
            return int(selection[0])
        except ValueError:
            return None

    def set_events(
        self,
        events: list[Event],
        client_names: dict[int, str],
        room_names: dict[int, str],
        staff_names: dict[int, str],
        program_names: dict[int, str],
    ) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, event in enumerate(events):
            row_tag = "evenrow" if index % 2 == 0 else "oddrow"

            self.tree.insert(
                "",
                "end",
                iid=str(event.id),
                values=(
                    event.id,
                    event.title,
                    event.event_type,
                    event.start_time.strftime("%Y-%m-%d %H:%M"),
                    event.end_time.strftime("%Y-%m-%d %H:%M"),
                    event.visitor_count,
                    self._label(event.client_id, client_names),
                    self._label(event.room_id, room_names),
                    self._label(event.staff_id, staff_names),
                    self._label(event.program_id, program_names),
                    event.status,
                ),
                tags=(row_tag,),
            )
            
    @staticmethod
    def _label(entity_id: int, names: dict[int, str]) -> str:
        return names.get(entity_id, str(entity_id))
