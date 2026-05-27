import logging
from pathlib import Path

def setup_logger() -> None:
    """Nastaví logování appky do konzole a do souboru"""

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)  # Vytvoří složku pro logy, pokud neexistuje

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )