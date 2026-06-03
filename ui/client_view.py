from __future__ import annotations

from tkinter import messagebox, ttk

from ui.client_form_window import ClientFormWindow
from ui.crud_widgets import CrudColumn, CrudTableFrame, show_no_selection_warning


class ClientView(CrudTableFrame): # Dědí z CrudTableFrame, který poskytuje základní funkce pro tabulku s CRUD operacemi
    def __init__(self, master, client_service):
        self.client_service = client_service
        super().__init__(
            master,
            columns=[
                CrudColumn("id", "ID", 60, anchor="center"),
                CrudColumn("name", "Název", 220, anchor="center"),
                CrudColumn("client_type", "Typ", 120, anchor="center"),
                CrudColumn("contact_person", "Kontaktní osoba", 180, anchor="center"),
                CrudColumn("email", "Email", 200, anchor="center"),
                CrudColumn("phone", "Telefon", 30, anchor="center"),
            ],
            on_refresh=self.refresh,
            on_add=self.open_add,
            on_delete=self.delete_selected,
            on_edit=self.open_edit,
            add_label="Přidat klienta",
            edit_label="Upravit klienta",
            delete_label="Smazat klienta",
            striped_rows=True,
        )

    def refresh(self) -> None:
        clients = self.client_service.list_clients()
        self.set_rows([
            {
                "id": client.id,
                "name": client.name,
                "client_type": client.client_type,
                "contact_person": client.contact_person or "",
                "email": client.email or "",
                "phone": client.phone or "",
            }
            for client in clients
            if client.id is not None
        ])

    def open_add(self) -> None:
        ClientFormWindow(self, self.client_service, on_saved=self.refresh)

    def open_edit(self) -> None:
        selected_id = self.get_selected_id()
        if selected_id is None:
            show_no_selection_warning(self, "Upravit klienta")
            return

        try:
            client = self.client_service.get_client_by_id(selected_id)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        ClientFormWindow(self, self.client_service, on_saved=self.refresh, existing_item=client)

    def delete_selected(self) -> None:
        selected_id = self.get_selected_id()
        if selected_id is None:
            show_no_selection_warning(self, "Smazat klienta")
            return

        try:
            self.client_service.delete_client(selected_id)
        except ValueError as error:
            messagebox.showerror("Chyba", str(error), parent=self)
            return

        self.refresh()
