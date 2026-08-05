from sender import WhatsAppSender
from scheduler import Scheduler


def main():

    scheduler = Scheduler()

    campaign = scheduler.get_today_campaign()

    if campaign is None:
        print("📅 Hoy no hay campaña programada.")
        return

    sender = WhatsAppSender()

    sender.start(campaign)


if __name__ == "__main__":
    main()