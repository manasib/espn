import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler("error.log"),
              logging.StreamHandler(sys.stdout)],
    format="%(levelname)s - %(asctime)s - %(message)s",
)

logging.addLevelName(
    logging.INFO,
    "\033[1;32m%s\033[1;0m" % logging.getLevelName(
        logging.INFO)
)
logging.addLevelName(
    logging.WARNING,
    "\033[1;31m%s\033[1;0m" % logging.getLevelName(
        logging.WARNING)
)
logging.addLevelName(
    logging.ERROR,
    "\033[1;41m%s\033[1;0m" % logging.getLevelName(
        logging.ERROR)
)

logger = logging.getLogger(__name__)
