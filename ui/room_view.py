from __future__ import annotations

from tkinter import messagebox

from ui.crud_widgets import CrudColumn, CrudTableFrame, show_no_selection_warning
from ui.room_form_window import RoomFormWindow


class RoomView(CrudTableFrame):
    def __init__(self, master, room_service):
        self.room_service = room_service
        super().__init__(
            master,
            columns=[
                CrudColumn("id", "ID", 60),
                CrudColumn("name", "Název", 240),
                CrudColumn("capacity", "Kapacita", 100),
                CrudColumn("description", "Popis", 320),
            ],
            on_refresh=self.refresh,
            on_add=self.open_add,
            on_delete=self.delete_selected,
        )

    def refresh(self) -> None:
        rooms = self.room_service.list_rooms()
        self.set_rows([
            {
                "id": room.id,
                "name": room.name,
                "capacity": room.capacity,
                "description": room.description or "",
            }
            for room in rooms
            if room.id is not None
        ])

    def open_add(self) -> None:
        RoomFormWindow(self, self.room_service, on_saved=self.refresh)

    def delete_selected(self) -> None:
        selected_id = self.get_selected_id()
        if selected_id is None:
            show_no_selection_warning(self, "Smazat místnost")
            return

        try:
            self.room_service.delete_room(selected_id)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.refresh()
