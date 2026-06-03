from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from tkinter import StringVar
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
        enable_filter: bool = True,
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
        self.enable_filter = enable_filter
        self.filter_var = StringVar()
        self._rows: list[dict[str, object]] = []
        self._sort_column: str | None = None
        self._sort_reverse = False

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

        if self.enable_filter:
            filter_frame = ttk.Frame(toolbar)
            filter_frame.pack(side="right")

            ttk.Label(filter_frame, text="Filtr").pack(side="left", padx=(0, 6))
            filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=28)
            filter_entry.pack(side="left")
            ttk.Button(filter_frame, text="Vymazat", command=self.clear_filter).pack(side="left", padx=(8, 0))
            self.filter_var.trace_add("write", self._on_filter_changed)

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
            self.tree.heading(
                column.key,
                text=column.label,
                command=lambda key=column.key: self.sort_by_column(key),
            )
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

        self.tree.tag_configure("overdue", background="#fff3cd")

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
        # rows je seznam řádků tabulky.
        # Jeden řádek je dict, např. {"id": 1, "name": "Jan", "email": "..."}.
        # str = název sloupce, object = hodnota může být text, číslo, datum atd.
        self._rows = rows
        self._render_rows(self._filtered_rows())

    def sort_by_column(self, column_key: str) -> None:
        # Klik na stejný sloupec otočí směr řazení.
        # Klik na nový sloupec začne vzestupně.
        if self._sort_column == column_key:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_column = column_key
            self._sort_reverse = False

        self._render_rows(self._filtered_rows())

    def clear_filter(self) -> None:
        self.filter_var.set("")

    def _on_filter_changed(self, *_args) -> None:
        self._render_rows(self._filtered_rows())

    def _filtered_rows(self) -> list[dict[str, object]]:
        filter_text = self.filter_var.get().strip().lower()
        if not filter_text:
            return self._sorted_rows(self._rows)

        # row.values() vrátí jen hodnoty ze slovníku řádku.
        # Filtr tedy nehledá v názvech sloupců, ale v obsahu buněk.
        filtered_rows = [
            row
            for row in self._rows
            if any(filter_text in str(value).lower() for value in row.values())
        ]
        return self._sorted_rows(filtered_rows)

    def _sorted_rows(self, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        if self._sort_column is None:
            return rows

        return sorted(
            rows,
            key=lambda row: self._sort_value(row.get(self._sort_column, "")),
            reverse=self._sort_reverse,
        )

    @staticmethod
    def _sort_value(value: object) -> object:
        if isinstance(value, (int, float)):
            return (0, value)

        text = str(value).strip().lower()
        try:
            return (0, float(text))
        except ValueError:
            return (1, text)

    def _render_rows(self, rows: list[dict[str, object]]) -> None:
        # Treeview neumí jednoduše "přepsat" všechna data najednou,
        # proto nejdřív smažeme staré řádky a pak vložíme nové.
        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in enumerate(rows):
            item_id = str(row["id"])
            # Hodnoty musí být ve stejném pořadí jako sloupce v self.columns.
            values = [row.get(column.key, "") for column in self.columns]
            tags = ()

            if self.striped_rows:
                tags = ("evenrow" if index % 2 == 0 else "oddrow",)

            row_tag = row.get("_tag")
            if row_tag:
                tags = (str(row_tag),)

            self.tree.insert("", "end", iid=item_id, values=values, tags=tags)


class FormField:
    def __init__(self, key: str, label: str, required: bool = True):
        self.key = key
        self.label = label
        self.required = required


def show_no_selection_warning(parent, title: str) -> None:
    messagebox.showwarning(title, "Vyberte prosím záznam v tabulce.", parent=parent)
