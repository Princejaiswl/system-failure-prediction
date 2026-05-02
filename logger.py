import logging

def setup_logger():
    logger = logging.getLogger("decision_system")

    if logger.hasHandlers():
        return logger   # ✅ prevents duplicate logs

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # File handler

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
