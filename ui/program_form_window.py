from __future__ import annotations

from tkinter import StringVar, messagebox

from models.programs import Program
from ui.form_window import BaseFormWindow


class ProgramFormWindow(BaseFormWindow):
    def __init__(self, master, program_service, on_saved=None, existing_item: Program | None = None):
        self.existing_item = existing_item
        self.program_service = program_service
        title = "Upravit program" if self.existing_item is not None else "Přidat program"

        super().__init__(master, title, on_saved)

        self.name_var = StringVar()
        self.program_type_var = StringVar()
        self.duration_minutes_var = StringVar()
        self.recommended_age_var = StringVar()
        self.description_var = StringVar()

        self._build_form()

    def _build_form(self) -> None:
        self.add_entry("Název", self.name_var, 0)
        self.add_combobox("Typ programu", self.program_type_var, sorted(self.program_service.ALLOWED_PROGRAM_TYPES), 1)
        self.add_entry("Délka (min)", self.duration_minutes_var, 2)
        self.add_entry("Doporučený věk", self.recommended_age_var, 3)
        self.add_entry("Popis", self.description_var, 4)
        self.add_buttons(self.save_program)

        if self.program_service.ALLOWED_PROGRAM_TYPES:
            self.program_type_var.set(sorted(self.program_service.ALLOWED_PROGRAM_TYPES)[0])

        if self.existing_item is not None:
            self._fill_existing_data()

    def _fill_existing_data(self) -> None:
        self.name_var.set(self.existing_item.name)
        self.program_type_var.set(self.existing_item.program_type)
        self.duration_minutes_var.set(str(self.existing_item.duration_minutes))
        self.recommended_age_var.set(self.existing_item.recommended_age or "")
        self.description_var.set(self.existing_item.description or "")

    def save_program(self) -> None:
        if not self._validate_form():
            return

        try:
            program = Program(
                name=self.name_var.get().strip(),
                program_type=self.program_type_var.get().strip(),
                duration_minutes=int(self.duration_minutes_var.get().strip()),
                recommended_age=self.optional(self.recommended_age_var.get()),
                description=self.optional(self.description_var.get()),
                id=self.existing_item.id if self.existing_item is not None else None,
            )
            if self.existing_item is None:
                self.program_service.create_program(program)
            else:
                self.program_service.update_program(program)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.notify_saved()
        self.destroy()

    def _validate_form(self) -> bool:
        return (
            self.validate_required("Název", self.name_var.get())
            and self.validate_required("Typ programu", self.program_type_var.get())
            and self.validate_int("Délka (min)", self.duration_minutes_var.get(), minimum=1)
        )
