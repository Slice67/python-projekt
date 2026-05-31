from __future__ import annotations

from tkinter import messagebox

from ui.crud_widgets import CrudColumn, CrudTableFrame, show_no_selection_warning
from ui.program_form_window import ProgramFormWindow


class ProgramView(CrudTableFrame):
    def __init__(self, master, program_service):
        self.program_service = program_service
        super().__init__(
            master,
            columns=[
                CrudColumn("id", "ID", 60),
                CrudColumn("name", "Název", 240),
                CrudColumn("program_type", "Typ", 140),
                CrudColumn("duration_minutes", "Délka (min)", 110),
                CrudColumn("recommended_age", "Věk", 100),
                CrudColumn("description", "Popis", 320),
            ],
            on_refresh=self.refresh,
            on_add=self.open_add,
            on_delete=self.delete_selected,
        )

    def refresh(self) -> None:
        programs = self.program_service.list_programs()
        self.set_rows([
            {
                "id": program.id,
                "name": program.name,
                "program_type": program.program_type,
                "duration_minutes": program.duration_minutes,
                "recommended_age": program.recommended_age or "",
                "description": program.description or "",
            }
            for program in programs
            if program.id is not None
        ])

    def open_add(self) -> None:
        ProgramFormWindow(self, self.program_service, on_saved=self.refresh)

    def delete_selected(self) -> None:
        selected_id = self.get_selected_id()
        if selected_id is None:
            show_no_selection_warning(self, "Smazat program")
            return

        try:
            self.program_service.delete_program(selected_id)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.refresh()
