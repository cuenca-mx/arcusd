import logging

logging.basicConfig()

vcr_log = logging.getLogger('vcr')
vcr_log.setLevel(logging.DEBUG)
