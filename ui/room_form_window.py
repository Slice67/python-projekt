from __future__ import annotations

from tkinter import StringVar, Toplevel, messagebox, ttk

from models.room import Room


class RoomFormWindow(Toplevel):
    def __init__(self, master, room_service, on_saved=None):
        super().__init__(master)
        self.title("Přidat místnost")
        self.resizable(False, False)
        self.room_service = room_service
        self.on_saved = on_saved

        self.name_var = StringVar()
        self.capacity_var = StringVar()
        self.description_var = StringVar()

        self._build_form()
        self.transient(master)
        self.grab_set()
        self.focus_set()

    def _build_form(self) -> None:
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")

        fields = ttk.Frame(container)
        fields.grid(row=0, column=0, sticky="nsew")

        self._add_entry(fields, "Název", self.name_var, 0)
        self._add_entry(fields, "Kapacita", self.capacity_var, 1)
        self._add_entry(fields, "Popis", self.description_var, 2)

        button_row = ttk.Frame(container)
        button_row.grid(row=1, column=0, sticky="e", pady=(12, 0))

        ttk.Button(button_row, text="Uložit", command=self.save_room).pack(side="left")
        ttk.Button(button_row, text="Zrušit", command=self.destroy).pack(side="left", padx=(8, 0))

        fields.columnconfigure(1, weight=1)

    def _add_entry(self, parent, label: str, variable: StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=40).grid(row=row, column=1, sticky="ew", pady=4)

    def save_room(self) -> None:
        try:
            room = Room(
                name=self.name_var.get().strip(),
                capacity=int(self.capacity_var.get().strip()),
                description=self._optional(self.description_var.get()),
            )
            self.room_service.create_room(room)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        if self.on_saved is not None:
            self.on_saved()
        self.destroy()

    @staticmethod
    def _optional(value: str) -> str | None:
        value = value.strip()
        return value or None
