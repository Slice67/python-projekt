from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from tkinter import messagebox

from tkinter import ttk


@dataclass
class CrudColumn:
    key: str
    label: str
    width: int = 160


class CrudTableFrame(ttk.Frame):
    """Reusable table with refresh/add/delete actions."""

    def __init__(
        self,
        master,
        columns: list[CrudColumn],
        on_refresh: Callable[[], None],
        on_add: Callable[[], None],
        on_delete: Callable[[], None],
        on_edit: Callable[[], None] | None = None,
    ):
        super().__init__(master, padding=12)
        self.columns = columns
        self.on_refresh = on_refresh
        self.on_add = on_add
        self.on_delete = on_delete
        self.on_edit = on_edit

        self._build_toolbar()
        self._build_table()

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 12))

        ttk.Button(toolbar, text="Obnovit", command=self.on_refresh).pack(side="left")
        ttk.Button(toolbar, text="Přidat", command=self.on_add).pack(side="left", padx=(8, 0))

        if self.on_edit is not None:
            ttk.Button(toolbar, text="Upravit", command=self.on_edit).pack(side="left", padx=(8, 0))

        ttk.Button(toolbar, text="Smazat", command=self.on_delete).pack(side="left", padx=(8, 0))

    def _build_table(self) -> None:
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        column_ids = [column.key for column in self.columns]
        self.tree = ttk.Treeview(
            table_frame,
            columns=column_ids,
            show="headings",
            selectmode="browse",
            height=18,
        )

        for column in self.columns:
            self.tree.heading(column.key, text=column.label)
            self.tree.column(column.key, width=column.width, anchor="w", stretch=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_selected_id(self) -> int | None:
        selection = self.tree.selection()
        if not selection:
            return None

        try:
            return int(selection[0])
        except ValueError:
            return None

    def set_rows(self, rows: list[dict[str, object]]) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            item_id = str(row["id"])
            values = [row.get(column.key, "") for column in self.columns]
            self.tree.insert("", "end", iid=item_id, values=values)


class FormField:
    def __init__(self, key: str, label: str, required: bool = True):
        self.key = key
        self.label = label
        self.required = required


def show_no_selection_warning(parent, title: str) -> None:
    messagebox.showwarning(title, "Vyberte prosím záznam v tabulce.", parent=parent)
