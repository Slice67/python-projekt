from __future__ import annotations

from datetime import datetime, timedelta

from tkinter import StringVar, messagebox

from models.clients import Client
from models.events import Event
from models.programs import Program
from models.room import Room
from models.staff import Staff
from ui.form_window import BaseFormWindow


class EventFormWindow(BaseFormWindow):
    """Dialog pro vytvoření nebo úpravu akce."""

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
        self.existing_event = existing_event
        self.client_service = client_service
        self.room_service = room_service
        self.staff_service = staff_service
        self.program_service = program_service
        self.event_service = event_service
        title = "Upravit akci" if self.existing_event is not None else "Přidat akci"

        super().__init__(master, title, on_saved)

        self._clients = self.client_service.list_clients()
        self._rooms = self.room_service.list_rooms()
        self._staff = self.staff_service.list_staff()
        self._programs = self.program_service.list_programs()

        self._client_map = self._build_choice_map(self._clients, "name")
        self._room_map = self._build_choice_map(self._rooms, "name")
        self._staff_map = self._build_choice_map(self._staff, "name")
        self._program_map = self._build_choice_map(self._programs, "name")

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

        self._build_form()

    def _build_form(self) -> None:
        self.add_entry("Název", self.title_var, 0)
        self.add_combobox("Typ akce", self.event_type_var, sorted(self.event_service.ALLOWED_EVENT_TYPES), 1)
        self.add_entry("Začátek (YYYY-MM-DD HH:MM)", self.start_time_var, 2)
        self.add_entry("Konec (YYYY-MM-DD HH:MM)", self.end_time_var, 3)
        self.add_entry("Počet návštěvníků", self.visitor_count_var, 4)
        self.add_combobox("Klient", self.client_var, self._client_map.keys(), 5)
        self.add_combobox("Místnost", self.room_var, self._room_map.keys(), 6)
        self.add_combobox("Zaměstnanec", self.staff_var, self._staff_map.keys(), 7)
        self.add_combobox("Program", self.program_var, self._program_map.keys(), 8)
        self.add_combobox("Status", self.status_var, sorted(self.event_service.ALLOWED_STATUSES), 9)
        self.description_text = self.add_text("Popis", 10)
        self.add_buttons(self.save_event)

        if self.existing_event is None:
            self._set_default_values()
        else:
            self._fill_existing_data()

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

    def save_event(self) -> None:
        if not self._validate_form():
            return

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
        self.notify_saved()
        self.destroy()

    def _validate_form(self) -> bool:
        if not (
            self.validate_required("Název", self.title_var.get())
            and self.validate_required("Typ akce", self.event_type_var.get())
            and self.validate_datetime("Začátek", self.start_time_var.get())
            and self.validate_datetime("Konec", self.end_time_var.get())
            and self.validate_int("Počet návštěvníků", self.visitor_count_var.get(), minimum=0)
            and self.validate_required("Klient", self.client_var.get())
            and self.validate_required("Místnost", self.room_var.get())
            and self.validate_required("Zaměstnanec", self.staff_var.get())
            and self.validate_required("Program", self.program_var.get())
            and self.validate_required("Status", self.status_var.get())
        ):
            return False

        start_time = datetime.strptime(self.start_time_var.get().strip(), "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(self.end_time_var.get().strip(), "%Y-%m-%d %H:%M")
        if end_time <= start_time:
            messagebox.showwarning("Validace", "Konec akce musí být později než začátek.", parent=self)
            return False

        return True

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
