import logging


def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    return_format = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t %(message)s \n"
    datetime_format = "%d.%m.%Y %I:%M:%S %p"

    filename = f'logs/log.log'

    logging.basicConfig(format=return_format, datefmt=datetime_format, level=level, filename=filename, filemode="w")

    logger = logging.getLogger(name)
    return logger
