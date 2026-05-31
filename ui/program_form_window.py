from __future__ import annotations

from tkinter import StringVar, Toplevel, messagebox, ttk

from models.programs import Program


class ProgramFormWindow(Toplevel):
    def __init__(self, master, program_service, on_saved=None):
        super().__init__(master)
        self.title("Přidat program")
        self.resizable(False, False)
        self.program_service = program_service
        self.on_saved = on_saved

        self.name_var = StringVar()
        self.program_type_var = StringVar()
        self.duration_minutes_var = StringVar()
        self.recommended_age_var = StringVar()
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
        self._add_combobox(fields, "Typ programu", self.program_type_var, sorted(self.program_service.ALLOWED_PROGRAM_TYPES), 1)
        self._add_entry(fields, "Délka (min)", self.duration_minutes_var, 2)
        self._add_entry(fields, "Doporučený věk", self.recommended_age_var, 3)
        self._add_entry(fields, "Popis", self.description_var, 4)

        button_row = ttk.Frame(container)
        button_row.grid(row=1, column=0, sticky="e", pady=(12, 0))

        ttk.Button(button_row, text="Uložit", command=self.save_program).pack(side="left")
        ttk.Button(button_row, text="Zrušit", command=self.destroy).pack(side="left", padx=(8, 0))

        if self.program_service.ALLOWED_PROGRAM_TYPES:
            self.program_type_var.set(sorted(self.program_service.ALLOWED_PROGRAM_TYPES)[0])

        fields.columnconfigure(1, weight=1)

    def _add_entry(self, parent, label: str, variable: StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=40).grid(row=row, column=1, sticky="ew", pady=4)

    def _add_combobox(self, parent, label: str, variable: StringVar, values, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(parent, textvariable=variable, values=list(values), state="readonly", width=38).grid(
            row=row, column=1, sticky="ew", pady=4
        )

    def save_program(self) -> None:
        try:
            program = Program(
                name=self.name_var.get().strip(),
                program_type=self.program_type_var.get().strip(),
                duration_minutes=int(self.duration_minutes_var.get().strip()),
                recommended_age=self._optional(self.recommended_age_var.get()),
                description=self._optional(self.description_var.get()),
            )
            self.program_service.create_program(program)
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
