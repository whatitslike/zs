import logging
import sys

logger = logging.getLogger("zhihu-spider")
formatter = logging.Formatter('%(name)-12s %(message)s')
file_handler = logging.FileHandler("spider.log")
file_handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
