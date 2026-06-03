from __future__ import annotations

from tkinter import StringVar, messagebox

from models.staff import Staff
from ui.form_window import BaseFormWindow


class StaffFormWindow(BaseFormWindow):
    def __init__(self, master, staff_service, on_saved=None, existing_item: Staff | None = None):
        self.existing_item = existing_item
        self.staff_service = staff_service
        title = "Upravit zaměstnance" if self.existing_item is not None else "Přidat zaměstnance"

        super().__init__(master, title, on_saved)

        self.name_var = StringVar()
        self.role_var = StringVar()
        self.email_var = StringVar()

        self._build_form()

    def _build_form(self) -> None:
        self.add_entry("Jméno", self.name_var, 0)
        self.add_entry("Role", self.role_var, 1)
        self.add_entry("Email", self.email_var, 2)
        self.add_buttons(self.save_staff)

        if self.existing_item is not None:
            self._fill_existing_data()

    def _fill_existing_data(self) -> None:
        self.name_var.set(self.existing_item.name)
        self.role_var.set(self.existing_item.role)
        self.email_var.set(self.existing_item.email or "")

    def save_staff(self) -> None:
        if not self._validate_form():
            return

        try:
            staff = Staff(
                name=self.name_var.get().strip(),
                role=self.role_var.get().strip(),
                email=self.optional(self.email_var.get()),
                id=self.existing_item.id if self.existing_item is not None else None,
            )
            if self.existing_item is None:
                self.staff_service.create_staff(staff)
            else:
                self.staff_service.update_staff(staff)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.notify_saved()
        self.destroy()

    def _validate_form(self) -> bool:
        return (
            self.validate_required("Jméno", self.name_var.get())
            and self.validate_required("Role", self.role_var.get())
            and self.validate_email("Email", self.email_var.get())
        )
