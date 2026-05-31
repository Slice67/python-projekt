from __future__ import annotations

from tkinter import messagebox

from ui.crud_widgets import CrudColumn, CrudTableFrame, show_no_selection_warning
from ui.staff_form_window import StaffFormWindow


class StaffView(CrudTableFrame):
    def __init__(self, master, staff_service):
        self.staff_service = staff_service
        super().__init__(
            master,
            columns=[
                CrudColumn("id", "ID", 60),
                CrudColumn("name", "Jméno", 220),
                CrudColumn("role", "Role", 180),
                CrudColumn("email", "Email", 240),
            ],
            on_refresh=self.refresh,
            on_add=self.open_add,
            on_delete=self.delete_selected,
        )

    def refresh(self) -> None:
        staff_members = self.staff_service.list_staff()
        self.set_rows([
            {
                "id": member.id,
                "name": member.name,
                "role": member.role,
                "email": member.email or "",
            }
            for member in staff_members
            if member.id is not None
        ])

    def open_add(self) -> None:
        StaffFormWindow(self, self.staff_service, on_saved=self.refresh)

    def delete_selected(self) -> None:
        selected_id = self.get_selected_id()
        if selected_id is None:
            show_no_selection_warning(self, "Smazat zaměstnance")
            return

        try:
            self.staff_service.delete_staff(selected_id)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.refresh()
