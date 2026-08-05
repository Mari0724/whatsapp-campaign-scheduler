from sender import WhatsAppSender
from scheduler import Scheduler
from logger import Logger


def main():

    scheduler = Scheduler()

    campaign = scheduler.get_today_campaign()

    if campaign is None:
        print("📅 Hoy no hay campaña programada.")
        return

    sender = WhatsAppSender()

    logger = Logger()

    try:

        sender.start(campaign)

        logger.log_success(campaign)

    except Exception as e:

        logger.log_error(
            campaign,
            e
        )

        raise


if __name__ == "__main__":
    main()