from time import sleep

from ExchangeListGenerator import ExchangeList, send_email

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(name)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logging.basicConfig(level=logging.INFO)

SEND_EMAIL = False

try:
    exchange_list = ExchangeList.from_file('intercambio_configuracion.txt')

    exchange_list.generate_pairs()

    with open('intercambio.txt', 'w') as file:
        file.write(str(exchange_list.matched_participants))

    with open('intercambio_readable.txt', 'w') as file:
        for participant in exchange_list.matched_participants:
            file.write(f'{participant.name} comparte a {participant.matched_participant}\n')

    logging.info(f'Initial list {exchange_list.participants}')
    logging.info(f'Final list: {exchange_list.matched_participants}')

    if SEND_EMAIL:
        logger.info('Sending emails...')

        for participant in exchange_list.matched_participants:
            send_email(participant)
            sleep(30)

except Exception as e:
    logger.error(f'An error occurred: {e}')
