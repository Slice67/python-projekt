from __future__ import annotations

from tkinter import StringVar, messagebox

from models.room import Room
from ui.form_window import BaseFormWindow


class RoomFormWindow(BaseFormWindow):
    def __init__(self, master, room_service, on_saved=None, existing_item: Room | None = None):
        self.existing_item = existing_item
        self.room_service = room_service
        title = "Upravit místnost" if self.existing_item is not None else "Přidat místnost"

        super().__init__(master, title, on_saved)

        self.name_var = StringVar()
        self.capacity_var = StringVar()
        self.description_var = StringVar()

        self._build_form()

    def _build_form(self) -> None:
        self.add_entry("Název", self.name_var, 0)
        self.add_entry("Kapacita", self.capacity_var, 1)
        self.add_entry("Popis", self.description_var, 2)
        self.add_buttons(self.save_room)

        if self.existing_item is not None:
            self._fill_existing_data()

    def _fill_existing_data(self) -> None:
        self.name_var.set(self.existing_item.name)
        self.capacity_var.set(str(self.existing_item.capacity))
        self.description_var.set(self.existing_item.description or "")

    def save_room(self) -> None:
        if not self._validate_form():
            return

        try:
            room = Room(
                name=self.name_var.get().strip(),
                capacity=int(self.capacity_var.get().strip()),
                description=self.optional(self.description_var.get()),
                id=self.existing_item.id if self.existing_item is not None else None,
            )
            if self.existing_item is None:
                self.room_service.create_room(room)
            else:
                self.room_service.update_room(room)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.notify_saved()
        self.destroy()

    def _validate_form(self) -> bool:
        return (
            self.validate_required("Název", self.name_var.get())
            and self.validate_int("Kapacita", self.capacity_var.get(), minimum=1)
        )
