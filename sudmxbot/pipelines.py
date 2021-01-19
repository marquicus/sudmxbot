# -*- coding: utf-8 -*-

"""
Save ModelItem's to a local SQLite database.
"""

from sudmxbot.items import *
from sudmxbot.models import *


class ModelPipeline(object):
    "The pipeline stores scraped data in a database."

    def process_item(self, item, spider):
        if isinstance(item, ModelItem):
            item.save()
        return item


class DailyPipeline(object):
    "The pipeline stores scraped daily in a database."

    def process_item(self, item, spider):
        print(f"Processing DailyPipeline {item} from {spider}")
        if isinstance(item, DailyItem):
            item.save()
        return item
