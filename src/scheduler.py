from pathlib import Path
from datetime import datetime, date
import json

import config
from logger import Logger

class Scheduler:

    def __init__(self):
        
        self.data_path = (
            Path(__file__).parent.parent
            / "data"
        )

        self.logger = Logger()

    def get_today_campaign(self):

        today = date.today().isoformat()

        current_time = datetime.now().strftime("%H:%M")

        send_time = (
            config.TEST_TIME
            if config.TEST_MODE
            else config.PRODUCTION_TIME
        )
        

        if current_time < send_time:
            print(
                f"⏰ Aún no es hora de enviar. "
                f"Programado para las {send_time}."
            )
            return None

        if self.logger.was_sent_today():
            print("✅ La campaña de hoy ya fue enviada.")
            return None

        schedule_file = (
            self.data_path
            / config.SCHEDULE_FILE
        )

        with open(
            schedule_file,
            "r",
            encoding="utf-8"
        ) as file:

            schedule = json.load(file)

        for campaign in schedule:

            if campaign["date"] == today:
                return campaign

        return None