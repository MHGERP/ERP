# -*- coding: UTF-8 -*-
#TODO Singleton for logging

from django.utils.log import getLogger

logger = getLogger('django')


def loginfo(p="", label=""):
    logger.info("***"*10)
    logger.info(label)
    logger.info(p)
    logger.info("---"*10)
