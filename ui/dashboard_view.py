from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta

from tkinter import Canvas
from tkinter import ttk

from models.events import Event


class DashboardView(ttk.Frame):
    """Jednoduchý přehled statistik akcí."""

    def __init__(self, master):
        super().__init__(master, padding=16) 
        # Konstruktor rodičovské třídy ttk.Frame, nastaví vnitřní odsazení 16 pixelů, 
        # master je rodičovský widget, do kterého bude tento DashboardView vložen.

        self.cards_frame = ttk.Frame(self)
        self.cards_frame.pack(fill="x")

        self.chart_frame = ttk.LabelFrame(self, text="Návštěvníci za posledních 7 dní", padding=12)
        self.chart_frame.pack(fill="both", expand=True, pady=(16, 0))

        self.chart = Canvas(self.chart_frame, height=280, background="white", highlightthickness=1, highlightbackground="#d9dee3")
        self.chart.pack(fill="both", expand=True)

        self.card_values: dict[str, ttk.Label] = {}
        self._build_cards()
        self.chart.bind("<Configure>", lambda _event: self._redraw_chart())

        self._events: list[Event] = []
        self._visitor_days: dict[date, int] = {}

    def _build_cards(self) -> None:
        # Karty jsou malé souhrnné statistiky nad seznamem akcí.
        # Hodnoty se doplňují později v metodě refresh().
        cards = [
            ("active_events", "Aktivní akce"),
            ("planned_events", "Naplánované"),
            ("confirmed_events", "Potvrzené"),
            ("overdue_events", "K uzavření"),
            ("week_visitors", "Návštěvníci za 7 dní"),
        ]

        for index, (key, label) in enumerate(cards):
            card = ttk.Frame(self.cards_frame, padding=12, relief="solid", borderwidth=1)
            card.grid(row=0, column=index, sticky="ew", padx=(0, 12))

            ttk.Label(card, text=label).pack(anchor="w")
            value_label = ttk.Label(card, text="0", font=("Segoe UI", 18, "bold"))
            value_label.pack(anchor="w", pady=(6, 0))
            self.card_values[key] = value_label

            self.cards_frame.columnconfigure(index, weight=1)

    def refresh(self, events: list[Event]) -> None:
        # Dashboard nedělá vlastní SQL dotazy.
        # Dostane už načtený seznam Event objektů a nad ním spočítá statistiky.
        self._events = events
        now = datetime.now()
        today = datetime.now().date()
        week_start = today - timedelta(days=6)

        # Aktivní akce jsou všechny kromě zrušených.
        active_events = [event for event in events if event.status != "cancelled"]
        # K uzavření jsou akce, které časově skončily,
        # ale uživatel je ještě ručně neoznačil jako dokončené.
        overdue_events = [
            event
            for event in events
            if event.end_time < now and event.status in {"planned", "confirmed"}
        ]

        # Pro graf bereme jen aktivní akce za posledních 7 dní včetně dneška.
        week_events = [
            event
            for event in active_events
            if week_start <= event.start_time.date() <= today
        ]

        # Slovník má jako klíč konkrétní datum a jako hodnotu součet návštěvníků v daný den.
        # defaultdict(int) automaticky začne od 0, když datum ještě ve slovníku není.
        self._visitor_days = defaultdict(int)
        for event in week_events:
            self._visitor_days[event.start_time.date()] += event.visitor_count

        # Odkazuje na label v kartě "Aktivní akce" a nastavuje jeho text na počet aktivních akcí
        self.card_values["active_events"].configure(text=str(len(active_events)))
        self.card_values["planned_events"].configure(text=str(sum(1 for event in events if event.status == "planned")))
        self.card_values["confirmed_events"].configure(text=str(sum(1 for event in events if event.status == "confirmed")))
        self.card_values["overdue_events"].configure(text=str(len(overdue_events)))
        self.card_values["week_visitors"].configure(text=str(sum(event.visitor_count for event in week_events)))

        self._redraw_chart()

    def _redraw_chart(self) -> None:
        # Graf se překresluje při refreshi i při změně velikosti okna.
        self.chart.delete("all")

        width = max(self.chart.winfo_width(), 400)
        height = max(self.chart.winfo_height(), 240)
        padding_left = 48
        padding_right = 24
        padding_top = 24
        padding_bottom = 46
        chart_width = width - padding_left - padding_right
        chart_height = height - padding_top - padding_bottom

        today = datetime.now().date()
        # Seznam posledních 7 dní ve správném pořadí zleva doprava.
        days = [today - timedelta(days=6 - offset) for offset in range(7)]
        values = [self._visitor_days.get(day, 0) for day in days]
        max_value = max(values) if values else 0
        scale_max = max(max_value, 1)

        self.chart.create_line( # osa X
            padding_left,
            padding_top + chart_height,
            padding_left + chart_width,
            padding_top + chart_height,
            fill="#9aa4af",
        )
        self.chart.create_line( # osa Y
            padding_left,
            padding_top,
            padding_left,
            padding_top + chart_height,
            fill="#9aa4af",
        )

        bar_gap = 12
        bar_width = max((chart_width - bar_gap * 6) / 7, 12) # 7 sloupců, 6 mezer mezi nimi, minimální šířka 12 pixelů

        for index, day in enumerate(days):
            # Výška sloupce je poměr návštěvníků daného dne k maximu v grafu.
            value = values[index]
            bar_height = (value / scale_max) * chart_height if scale_max else 0
            x1 = padding_left + index * (bar_width + bar_gap)
            x2 = x1 + bar_width
            y1 = padding_top + chart_height - bar_height
            y2 = padding_top + chart_height

            self.chart.create_rectangle(x1, y1, x2, y2, fill="#2f80ed", outline="")
            self.chart.create_text((x1 + x2) / 2, y1 - 10, text=str(value), fill="#1f2933")
            self.chart.create_text(
                (x1 + x2) / 2,
                padding_top + chart_height + 18,
                text=day.strftime("%d.%m."),
                fill="#1f2933",
            )

        self.chart.create_text(
            padding_left,
            padding_top - 8,
            text=f"max {max_value}",
            anchor="w",
            fill="#52616f",
        )
