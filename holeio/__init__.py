import logging
import os

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.DEBUG)
os.umask(0)  # Files we download should have broad permissions.
