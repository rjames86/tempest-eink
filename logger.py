import logging
import sys
from os import environ

LOGLEVEL = environ.get("LOGLEVEL", "INFO").upper()

logging.basicConfig(
    level=LOGLEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("tempest.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)