from __future__ import annotations

from datetime import datetime
import re

from tkinter import Text, Toplevel
from tkinter import messagebox
from tkinter import Variable
from tkinter import ttk


class BaseFormWindow(Toplevel):
    """Společná šablona pro formulářová okna."""

    def __init__(self, master, title: str, on_saved=None):
        super().__init__(master)
        self.on_saved = on_saved

        self.title(title)
        self.resizable(False, False)

        self.container = ttk.Frame(self, padding=16)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.fields = ttk.Frame(self.container)
        self.fields.grid(row=0, column=0, sticky="nsew")

        self.button_row = ttk.Frame(self.container)
        self.button_row.grid(row=1, column=0, sticky="e", pady=(12, 0))

        self.transient(master)
        self.grab_set()
        self.focus_set()

    def add_entry(self, label: str, variable: Variable, row: int, width: int = 40) -> None:
        ttk.Label(self.fields, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(self.fields, textvariable=variable, width=width).grid(row=row, column=1, sticky="ew", pady=4)

    def add_combobox(self, label: str, variable: Variable, values, row: int, width: int = 38) -> ttk.Combobox:
        ttk.Label(self.fields, text=label).grid(row=row, column=0, sticky="w", pady=4)
        combobox = ttk.Combobox(
            self.fields,
            textvariable=variable,
            values=list(values),
            state="readonly",
            width=width,
        )
        combobox.grid(row=row, column=1, sticky="ew", pady=4)
        return combobox

    def add_text(self, label: str, row: int, width: int = 48, height: int = 5) -> Text:
        ttk.Label(self.fields, text=label).grid(row=row, column=0, sticky="w", pady=(8, 4))
        text = Text(self.fields, width=width, height=height, wrap="word")
        text.grid(row=row, column=1, sticky="ew", pady=(8, 4))
        return text

    def add_buttons(self, save_command) -> None:
        ttk.Button(self.button_row, text="Uložit", command=save_command).pack(side="left")
        ttk.Button(self.button_row, text="Zrušit", command=self.destroy).pack(side="left", padx=(8, 0))
        self.fields.columnconfigure(1, weight=1)

    def notify_saved(self) -> None:
        if self.on_saved is not None:
            self.on_saved()

    def validate_required(self, label: str, value: str) -> bool:
        if value.strip():
            return True

        messagebox.showwarning("Validace", f"Vyplňte pole {label}.", parent=self)
        return False

    def validate_email(self, label: str, value: str, required: bool = False) -> bool:
        value = value.strip()
        if not value:
            if required:
                return self.validate_required(label, value)
            return True

        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            return True

        messagebox.showwarning("Validace", f"Pole {label} musí obsahovat platný email.", parent=self)
        return False

    def validate_int(self, label: str, value: str, minimum: int | None = None) -> bool:
        value = value.strip()
        if not self.validate_required(label, value):
            return False

        try:
            number = int(value)
        except ValueError:
            messagebox.showwarning("Validace", f"Pole {label} musí být celé číslo.", parent=self)
            return False

        if minimum is not None and number < minimum:
            messagebox.showwarning("Validace", f"Pole {label} musí být alespoň {minimum}.", parent=self)
            return False

        return True

    def validate_datetime(self, label: str, value: str, date_format: str = "%Y-%m-%d %H:%M") -> bool:
        value = value.strip()
        if not self.validate_required(label, value):
            return False

        try:
            datetime.strptime(value, date_format)
        except ValueError:
            messagebox.showwarning("Validace", f"Pole {label} musí být ve formátu YYYY-MM-DD HH:MM.", parent=self)
            return False

        return True

    @staticmethod
    def optional(value: str) -> str | None:
        value = value.strip()
        return value or None
