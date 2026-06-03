from __future__ import annotations

from tkinter import messagebox

from ttkbootstrap import Window
from tkinter import ttk

from ui.dashboard_view import DashboardView
from ui.event_form_window import EventFormWindow
from ui.events_view import EventsView
from ui.client_view import ClientView
from ui.room_view import RoomView
from ui.staff_view import StaffView
from ui.program_view import ProgramView


class MainWindow(Window):
    """Hlavní okno aplikace s tabulkou akcí."""

    def __init__(
        self,
        client_service,
        room_service,
        staff_service,
        program_service,
        event_service,
        export_service,
    ):
        super().__init__(themename="flatly")
        self.title("Observatory Event Manager")
        self.geometry("1460x800")
        self.minsize(1200, 650)

        # try:
        #     self.state("zoomed")
        # except Exception:
        #     pass

        self.client_service = client_service
        self.room_service = room_service
        self.staff_service = staff_service
        self.program_service = program_service
        self.event_service = event_service
        self.export_service = export_service

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.dashboard_view = DashboardView(self.notebook)
        self.events_view = EventsView(
            self.notebook,
            on_refresh=self.refresh_events,
            on_add=self.open_add_event_window,
            on_edit=self.open_edit_event_window,
            on_delete=self.delete_selected_event,
            on_export=self.export_csv,
            on_mark_completed=self.mark_selected_event_completed,
        )
        self.client_view = ClientView(self.notebook, self.client_service)
        self.room_view = RoomView(self.notebook, self.room_service)
        self.staff_view = StaffView(self.notebook, self.staff_service)
        self.program_view = ProgramView(self.notebook, self.program_service)

        self.notebook.add(self.dashboard_view, text="Dashboard")
        self.notebook.add(self.events_view, text="Akce")
        self.notebook.add(self.client_view, text="Klienti")
        self.notebook.add(self.room_view, text="Místnosti")
        self.notebook.add(self.staff_view, text="Zaměstnanci")
        self.notebook.add(self.program_view, text="Programy")

        self.after(0, self.refresh_events)
        self.after(0, self.refresh_master_data)

    def refresh_events(self) -> None:
        events = self.event_service.list_events()
        self.dashboard_view.refresh(events)
        self.events_view.set_events(
            events,
            client_names=self._name_map(self.client_service.list_clients()),
            room_names=self._name_map(self.room_service.list_rooms()),
            staff_names=self._name_map(self.staff_service.list_staff()),
            program_names=self._name_map(self.program_service.list_programs()),
        )

    def refresh_master_data(self) -> None:
        self.client_view.refresh()
        self.room_view.refresh()
        self.staff_view.refresh()
        self.program_view.refresh()

    def open_add_event_window(self) -> None:
        EventFormWindow(
            self,
            self.client_service,
            self.room_service,
            self.staff_service,
            self.program_service,
            self.event_service,
            on_saved=self.refresh_events,
        )

    def open_edit_event_window(self) -> None:
        event_id = self.events_view.get_selected_event_id()
        if event_id is None:
            messagebox.showwarning("Upravit akci", "Vyberte prosím akci v tabulce.", parent=self)
            return

        try:
            event = self.event_service.get_event_by_id(event_id)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        EventFormWindow(
            self,
            self.client_service,
            self.room_service,
            self.staff_service,
            self.program_service,
            self.event_service,
            on_saved=self.refresh_events,
            existing_event=event,
        )

    def delete_selected_event(self) -> None:
        event_id = self.events_view.get_selected_event_id()
        if event_id is None:
            messagebox.showwarning("Smazat akci", "Vyberte prosím akci v tabulce.", parent=self)
            return

        if not messagebox.askyesno("Smazat akci", f"Opravdu chcete smazat akci s ID {event_id}?", parent=self):
            return

        try:
            self.event_service.delete_event(event_id)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.refresh_events()
        messagebox.showinfo("Smazáno", f"Akce s ID {event_id} byla smazána.", parent=self)

    def mark_selected_event_completed(self) -> None:
        event_id = self.events_view.get_selected_event_id()
        if event_id is None:
            messagebox.showwarning("Označit dokončeno", "Vyberte prosím akci v tabulce.", parent=self)
            return

        try:
            event = self.event_service.get_event_by_id(event_id)
            if event.status == "completed":
                messagebox.showinfo("Označit dokončeno", "Akce už je označená jako dokončená.", parent=self)
                return
            if event.status == "cancelled":
                messagebox.showwarning("Označit dokončeno", "Zrušenou akci nelze označit jako dokončenou.", parent=self)
                return

            event.status = "completed"
            self.event_service.update_event(event)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.refresh_events()
        messagebox.showinfo("Označit dokončeno", f"Akce s ID {event_id} byla označena jako dokončená.", parent=self)

    def export_csv(self) -> None:
        try:
            events = self.event_service.list_events()
            file_path = self.export_service.export_events_to_csv(
                events,
                client_names=self._name_map(self.client_service.list_clients()),
                room_names=self._name_map(self.room_service.list_rooms()),
                staff_names=self._name_map(self.staff_service.list_staff()),
                program_names=self._name_map(self.program_service.list_programs()),
            )
        except OSError as error:
            messagebox.showerror("Export CSV", f"Export se nepodařil uložit:\n{error}", parent=self)
            return

        messagebox.showinfo("Export CSV", f"Export uložen do {file_path}", parent=self)

    @staticmethod
    def _name_map(items) -> dict[int, str]:
        return {item.id: item.name for item in items if item.id is not None}
