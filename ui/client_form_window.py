from __future__ import annotations

from tkinter import StringVar, messagebox

from models.clients import Client
from ui.form_window import BaseFormWindow


class ClientFormWindow(BaseFormWindow):
    def __init__(self, master, client_service, on_saved=None, existing_item: Client | None = None):
        self.existing_item = existing_item
        self.client_service = client_service
        title = "Upravit klienta" if self.existing_item is not None else "Přidat klienta"

        super().__init__(master, title, on_saved)

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

    def _build_form(self) -> None:
        self.add_entry("Název", self.name_var, 0)
        self.add_combobox("Typ klienta", self.client_type_var, sorted(self.client_service.ALLOWED_CLIENT_TYPES), 1)
        self.add_entry("Kontaktní osoba", self.contact_person_var, 2)
        self.add_entry("Email", self.email_var, 3)
        self.add_entry("Telefon", self.phone_var, 4)
        self.add_entry("Ulice", self.street_var, 5)
        self.add_entry("Město", self.city_var, 6)
        self.add_entry("PSČ", self.postal_code_var, 7)
        self.add_entry("Poznámka", self.note_var, 8)
        self.add_buttons(self.save_client)

        if self.client_service.ALLOWED_CLIENT_TYPES:
            self.client_type_var.set(sorted(self.client_service.ALLOWED_CLIENT_TYPES)[0])

        if self.existing_item is not None:
            self._fill_existing_data()

    def _fill_existing_data(self) -> None:
        self.name_var.set(self.existing_item.name)
        self.client_type_var.set(self.existing_item.client_type)
        self.contact_person_var.set(self.existing_item.contact_person or "")
        self.email_var.set(self.existing_item.email or "")
        self.phone_var.set(self.existing_item.phone or "")
        self.street_var.set(self.existing_item.street or "")
        self.city_var.set(self.existing_item.city or "")
        self.postal_code_var.set(self.existing_item.postal_code or "")
        self.note_var.set(self.existing_item.note or "")

    def save_client(self) -> None:
        if not self._validate_form():
            return

        try:
            client = Client(
                name=self.name_var.get().strip(),
                client_type=self.client_type_var.get().strip(),
                contact_person=self.optional(self.contact_person_var.get()),
                email=self.optional(self.email_var.get()),
                phone=self.optional(self.phone_var.get()),
                street=self.optional(self.street_var.get()),
                city=self.optional(self.city_var.get()),
                postal_code=self.optional(self.postal_code_var.get()),
                note=self.optional(self.note_var.get()),
                id=self.existing_item.id if self.existing_item is not None else None,
            )
            if self.existing_item is None:
                self.client_service.create_client(client)
            else:
                self.client_service.update_client(client)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.notify_saved()
        self.destroy()

    def _validate_form(self) -> bool:
        return (
            self.validate_required("Název", self.name_var.get())
            and self.validate_required("Typ klienta", self.client_type_var.get())
            and self.validate_email("Email", self.email_var.get())
        )
