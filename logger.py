import logging


logger = logging.getLogger('nearest_store_logger')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()

logger.setLevel(logging.INFO)
handler.setLevel(logging.DEBUG)

handler.setFormatter(formatter)

logger.addHandler(handler)
