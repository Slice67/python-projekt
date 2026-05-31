from __future__ import annotations

from tkinter import StringVar, Toplevel, messagebox, ttk

from models.clients import Client


class ClientFormWindow(Toplevel):
    def __init__(self, master, client_service, on_saved=None):
        super().__init__(master)
        self.title("Přidat klienta")
        self.resizable(False, False)
        self.client_service = client_service
        self.on_saved = on_saved

        self.name_var = StringVar()
        self.client_type_var = StringVar()
        self.contact_person_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()
        self.street_var = StringVar()
        self.city_var = StringVar()
        self.postal_code_var = StringVar()
        self.note_var = StringVar()

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
        self._add_combobox(fields, "Typ klienta", self.client_type_var, sorted(self.client_service.ALLOWED_CLIENT_TYPES), 1)
        self._add_entry(fields, "Kontaktní osoba", self.contact_person_var, 2)
        self._add_entry(fields, "Email", self.email_var, 3)
        self._add_entry(fields, "Telefon", self.phone_var, 4)
        self._add_entry(fields, "Ulice", self.street_var, 5)
        self._add_entry(fields, "Město", self.city_var, 6)
        self._add_entry(fields, "PSČ", self.postal_code_var, 7)
        self._add_entry(fields, "Poznámka", self.note_var, 8)

        button_row = ttk.Frame(container)
        button_row.grid(row=1, column=0, sticky="e", pady=(12, 0))

        ttk.Button(button_row, text="Uložit", command=self.save_client).pack(side="left")
        ttk.Button(button_row, text="Zrušit", command=self.destroy).pack(side="left", padx=(8, 0))

        if self.client_service.ALLOWED_CLIENT_TYPES:
            self.client_type_var.set(sorted(self.client_service.ALLOWED_CLIENT_TYPES)[0])

        fields.columnconfigure(1, weight=1)

    def _add_entry(self, parent, label: str, variable: StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=40).grid(row=row, column=1, sticky="ew", pady=4)

    def _add_combobox(self, parent, label: str, variable: StringVar, values, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(parent, textvariable=variable, values=list(values), state="readonly", width=38).grid(
            row=row, column=1, sticky="ew", pady=4
        )

    def save_client(self) -> None:
        try:
            client = Client(
                name=self.name_var.get().strip(),
                client_type=self.client_type_var.get().strip(),
                contact_person=self._optional(self.contact_person_var.get()),
                email=self._optional(self.email_var.get()),
                phone=self._optional(self.phone_var.get()),
                street=self._optional(self.street_var.get()),
                city=self._optional(self.city_var.get()),
                postal_code=self._optional(self.postal_code_var.get()),
                note=self._optional(self.note_var.get()),
            )
            self.client_service.create_client(client)
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
