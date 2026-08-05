from pathlib import Path
from datetime import date
import json

import config


class Scheduler:

    def __init__(self):
        self.data_path = (
            Path(__file__).parent.parent
            / "data"
        )

    def get_today_campaign(self):

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

        today = date.today().isoformat()

        for campaign in schedule:

            if campaign["date"] == today:
                return campaign

        return None