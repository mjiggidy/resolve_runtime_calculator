"""
Function(s?) for log setup
"""

import logging, pathlib
from os import PathLike

def setup_logging(log_file_path:str|PathLike[str]|None=None):
	"""Establish logging handlers"""


	logging.basicConfig(level=logging.DEBUG)

	if log_file_path is None:

		logging.getLogger(__name__).info("Hello from %s.  No file path provided.  We loggin without logs I guess.", __name__)
		return

	from logging.handlers import RotatingFileHandler

	try:
		
		log_file_path = pathlib.Path(log_file_path)
		log_file_path.parent.mkdir(parents=True, exist_ok=True)

	except Exception as e:
		logging.getLogger(__name__).error("Could not create log path: %s", e, exc_info=True)

	else:
		
		file_handler = RotatingFileHandler(str(log_file_path), maxBytes=128 * 1024, backupCount=5)
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(logging.Formatter("[%(asctime)s]\t%(levelname)s\t%(name)s\t%(message)s"))

		logging.getLogger().addHandler(file_handler)

	logging.getLogger(__name__).info("Hello from %s", __name__)