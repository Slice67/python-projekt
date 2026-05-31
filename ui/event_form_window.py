from __future__ import annotations

from datetime import datetime, timedelta

from tkinter import Text, StringVar, Toplevel, messagebox, ttk

from models.clients import Client
from models.events import Event
from models.programs import Program
from models.room import Room
from models.staff import Staff


class EventFormWindow(Toplevel):
    """Dialog pro vytvoření nové akce."""

    def __init__(
        self,
        master,
        client_service,
        room_service,
        staff_service,
        program_service,
        event_service,
        on_saved=None,
        existing_event: Event | None = None,
    ):
        super().__init__(master)
        self.existing_event = existing_event
        self.title("Upravit akci" if self.existing_event is not None else "Přidat akci")
        self.resizable(False, False)

        self.client_service = client_service
        self.room_service = room_service
        self.staff_service = staff_service
        self.program_service = program_service
        self.event_service = event_service
        self.on_saved = on_saved

        self._clients = self.client_service.list_clients()
        self._rooms = self.room_service.list_rooms()
        self._staff = self.staff_service.list_staff()
        self._programs = self.program_service.list_programs()

        self._client_map = self._build_choice_map(self._clients, "name")
        self._room_map = self._build_choice_map(self._rooms, "name")
        self._staff_map = self._build_choice_map(self._staff, "name")
        self._program_map = self._build_choice_map(self._programs, "name")

        self._build_form()
        self.transient(master)
        self.grab_set()
        self.focus_set()

    def _build_form(self) -> None:
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")

        fields = ttk.Frame(container)
        fields.grid(row=0, column=0, sticky="nsew")

        self.title_var = StringVar()
        self.event_type_var = StringVar()
        self.start_time_var = StringVar()
        self.end_time_var = StringVar()
        self.visitor_count_var = StringVar()
        self.client_var = StringVar()
        self.room_var = StringVar()
        self.staff_var = StringVar()
        self.program_var = StringVar()
        self.status_var = StringVar(value="planned")

        self._add_entry(fields, "Název", self.title_var, 0)
        self._add_combobox(fields, "Typ akce", self.event_type_var, sorted(self.event_service.ALLOWED_EVENT_TYPES), 1)
        self._add_entry(fields, "Začátek (YYYY-MM-DD HH:MM)", self.start_time_var, 2)
        self._add_entry(fields, "Konec (YYYY-MM-DD HH:MM)", self.end_time_var, 3)
        self._add_entry(fields, "Počet návštěvníků", self.visitor_count_var, 4)
        self._add_combobox(fields, "Klient", self.client_var, list(self._client_map.keys()), 5, self._client_map)
        self._add_combobox(fields, "Místnost", self.room_var, list(self._room_map.keys()), 6, self._room_map)
        self._add_combobox(fields, "Zaměstnanec", self.staff_var, list(self._staff_map.keys()), 7, self._staff_map)
        self._add_combobox(fields, "Program", self.program_var, list(self._program_map.keys()), 8, self._program_map)
        self._add_combobox(fields, "Status", self.status_var, sorted(self.event_service.ALLOWED_STATUSES), 9)

        ttk.Label(fields, text="Popis").grid(row=10, column=0, sticky="w", pady=(8, 4))
        self.description_text = Text(fields, width=48, height=5, wrap="word")
        self.description_text.grid(row=10, column=1, sticky="ew", pady=(8, 4))

        button_row = ttk.Frame(container)
        button_row.grid(row=1, column=0, sticky="e", pady=(12, 0))

        ttk.Button(button_row, text="Uložit", command=self.save_event).pack(side="left")
        ttk.Button(button_row, text="Zrušit", command=self.destroy).pack(side="left", padx=(8, 0))

        if self.existing_event is None:
            self._set_default_values()
        else:
            self._fill_existing_data()

        fields.columnconfigure(1, weight=1)

    def _set_default_values(self) -> None:
        start = datetime.now().replace(second=0, microsecond=0)
        end = start + timedelta(hours=1)

        self.start_time_var.set(start.strftime("%Y-%m-%d %H:%M"))
        self.end_time_var.set(end.strftime("%Y-%m-%d %H:%M"))

        if self.event_service.ALLOWED_EVENT_TYPES:
            self.event_type_var.set(sorted(self.event_service.ALLOWED_EVENT_TYPES)[0])
        if self.event_service.ALLOWED_STATUSES:
            self.status_var.set("planned")
        if self._clients:
            self.client_var.set(self._display_value(self._clients[0]))
        if self._rooms:
            self.room_var.set(self._display_value(self._rooms[0]))
        if self._staff:
            self.staff_var.set(self._display_value(self._staff[0]))
        if self._programs:
            self.program_var.set(self._display_value(self._programs[0]))

    def _fill_existing_data(self) -> None:
        self.title_var.set(self.existing_event.title)
        self.event_type_var.set(self.existing_event.event_type)
        self.start_time_var.set(self.existing_event.start_time.strftime("%Y-%m-%d %H:%M"))
        self.end_time_var.set(self.existing_event.end_time.strftime("%Y-%m-%d %H:%M"))
        self.visitor_count_var.set(str(self.existing_event.visitor_count))
        self.status_var.set(self.existing_event.status)
        self.description_text.insert("1.0", self.existing_event.description or "")

        self.client_var.set(self._choice_label(self.existing_event.client_id, self._client_map))
        self.room_var.set(self._choice_label(self.existing_event.room_id, self._room_map))
        self.staff_var.set(self._choice_label(self.existing_event.staff_id, self._staff_map))
        self.program_var.set(self._choice_label(self.existing_event.program_id, self._program_map))

    def _add_entry(self, parent, label: str, variable: StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=40).grid(row=row, column=1, sticky="ew", pady=4)

    def _add_combobox(
        self,
        parent,
        label: str,
        variable: StringVar,
        values,
        row: int,
        mapping: dict[str, int] | None = None,
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)

        if mapping is None:
            options = list(values)
        else:
            options = list(mapping.keys())

        combobox = ttk.Combobox(
            parent,
            textvariable=variable,
            values=options,
            state="readonly",
            width=38,
        )
        combobox.grid(row=row, column=1, sticky="ew", pady=4)

    def save_event(self) -> None:
        try:
            event = Event(
                title=self.title_var.get().strip(),
                event_type=self.event_type_var.get().strip(),
                start_time=datetime.strptime(self.start_time_var.get().strip(), "%Y-%m-%d %H:%M"),
                end_time=datetime.strptime(self.end_time_var.get().strip(), "%Y-%m-%d %H:%M"),
                visitor_count=int(self.visitor_count_var.get().strip()),
                client_id=self._choice_id(self.client_var.get(), self._client_map, "klienta"),
                room_id=self._choice_id(self.room_var.get(), self._room_map, "místnost"),
                staff_id=self._choice_id(self.staff_var.get(), self._staff_map, "zaměstnance"),
                program_id=self._choice_id(self.program_var.get(), self._program_map, "program"),
                status=self.status_var.get().strip(),
                description=self._description_or_none(),
                id=self.existing_event.id if self.existing_event is not None else None,
            )

            if self.existing_event is None:
                event_id = self.event_service.create_event(event)
                info_text = f"Akce byla uložena (ID {event_id})."
            else:
                self.event_service.update_event(event)
                event_id = event.id
                info_text = f"Akce byla aktualizována (ID {event_id})."
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        messagebox.showinfo("Uloženo", info_text, parent=self)

        if self.on_saved is not None:
            self.on_saved()

        self.destroy()

    def _choice_id(self, value: str, mapping: dict[str, int], label: str) -> int:
        if not value:
            raise ValueError(f"Vyberte {label}.")

        if value in mapping:
            return mapping[value]

        try:
            selected_id = int(value.split(" - ", 1)[0])
        except ValueError as error:
            raise ValueError(f"Neplatný výběr pro {label}.") from error

        if selected_id not in mapping.values():
            raise ValueError(f"Neplatný výběr pro {label}.")

        return selected_id

    def _description_or_none(self) -> str | None:
        description = self.description_text.get("1.0", "end").strip()
        return description or None

    @staticmethod
    def _choice_label(entity_id: int, mapping: dict[str, int]) -> str:
        for label, mapped_id in mapping.items():
            if mapped_id == entity_id:
                return label
        return str(entity_id)

    @staticmethod
    def _display_value(entity) -> str:
        return f"{entity.id} - {entity.name}"

    @staticmethod
    def _build_choice_map(items: list[Client | Room | Staff | Program], name_attribute: str) -> dict[str, int]:
        mapping: dict[str, int] = {}
        for item in items:
            label = f"{item.id} - {getattr(item, name_attribute)}"
            mapping[label] = item.id
        return mapping
