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
    anchor: str = "w"
    minwidth: int | None = None


@dataclass
class CrudAction:
    label: str
    command: Callable[[], None]


class CrudTableFrame(ttk.Frame):
    """Template pro tabulky s CRUD tlačítky"""

    def __init__(
        self,
        master,
        columns: list[CrudColumn],
        on_refresh: Callable[[], None],
        on_add: Callable[[], None],
        on_delete: Callable[[], None],
        on_edit: Callable[[], None] | None = None,
        add_label: str = "Přidat",
        edit_label: str = "Upravit",
        delete_label: str = "Smazat",
        extra_actions: list[CrudAction] | None = None,
        horizontal_scrollbar: bool = False,
        striped_rows: bool = False,
        stretch_columns: bool = True,
    ):
        super().__init__(master, padding=12)
        self.columns = columns
        self.on_refresh = on_refresh
        self.on_add = on_add
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.add_label = add_label
        self.edit_label = edit_label
        self.delete_label = delete_label
        self.extra_actions = extra_actions or []
        self.horizontal_scrollbar = horizontal_scrollbar
        self.striped_rows = striped_rows

        self._build_toolbar()
        self._build_table()

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 12))

        ttk.Button(toolbar, text="Obnovit", command=self.on_refresh).pack(side="left")
        ttk.Button(toolbar, text=self.add_label, command=self.on_add).pack(side="left", padx=(8, 0))

        if self.on_edit is not None:
            ttk.Button(toolbar, text=self.edit_label, command=self.on_edit).pack(side="left", padx=(8, 0))

        ttk.Button(toolbar, text=self.delete_label, command=self.on_delete).pack(side="left", padx=(8, 0))

        for action in self.extra_actions:
            ttk.Button(toolbar, text=action.label, command=action.command).pack(side="left", padx=(8, 0))

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
            self.tree.column(
                column.key,
                width=column.width,
                minwidth=column.minwidth or column.width,
                anchor=column.anchor,
                stretch=True,
            )

        if self.striped_rows:
            self.tree.tag_configure("evenrow", background="#f8f9fa")
            self.tree.tag_configure("oddrow", background="#ffffff")

        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_scrollbar.set)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")

        if self.horizontal_scrollbar:
            x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=x_scrollbar.set)
            x_scrollbar.grid(row=1, column=0, sticky="ew")

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

        for index, row in enumerate(rows):
            item_id = str(row["id"])
            values = [row.get(column.key, "") for column in self.columns]
            tags = ()

            if self.striped_rows:
                tags = ("evenrow" if index % 2 == 0 else "oddrow",)

            self.tree.insert("", "end", iid=item_id, values=values, tags=tags)


class FormField:
    def __init__(self, key: str, label: str, required: bool = True):
        self.key = key
        self.label = label
        self.required = required


def show_no_selection_warning(parent, title: str) -> None:
    messagebox.showwarning(title, "Vyberte prosím záznam v tabulce.", parent=parent)
