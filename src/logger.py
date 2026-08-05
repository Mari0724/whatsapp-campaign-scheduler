from pathlib import Path
from datetime import datetime


class Logger:

    def __init__(self):
        self.logs_path = (
            Path(__file__).parent.parent
            / "logs"
        )

        self.logs_path.mkdir(
            exist_ok=True
        )

    def log_success(self, campaign):

        log_file = (
            self.logs_path
            / f"{campaign['date']}.log"
        )

        with open(
            log_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                f"Fecha: {campaign['date']}\n"
            )

            file.write(
                f"Hora: {datetime.now().strftime('%H:%M:%S')}\n"
            )

            file.write(
                f"Template: {campaign['template']}\n"
            )

            file.write(
                f"Imagen: {campaign['image']}\n"
            )

            file.write(
                "Estado: SUCCESS\n"
            )

    def log_error(
        self,
        campaign,
        error
    ):

        log_file = (
            self.logs_path
            / f"{campaign['date']}.log"
        )

        with open(
            log_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                f"Fecha: {campaign['date']}\n"
            )

            file.write(
                f"Hora: {datetime.now().strftime('%H:%M:%S')}\n"
            )

            file.write(
                "Estado: ERROR\n\n"
            )

            file.write(
                str(error)
            )

    def was_sent_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = (
            self.logs_path
            / f"{today}.log"
        )
        if not log_file.exists():
            return False
        with open(
            log_file,
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()
        return "Estado: SUCCESS" in content