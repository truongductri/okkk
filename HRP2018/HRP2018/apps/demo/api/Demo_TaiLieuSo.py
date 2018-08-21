# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list(args):
    items = models.Demo_TaiLieuSo().aggregate().project(
        folder_id = 1,
        folder_name = 1,
        parent_code = 1
        )
    
    return items.get_list()

