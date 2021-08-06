import logging
from pathlib import Path

from django.db import IntegrityError
from huey.contrib.djhuey import db_task, task

from etl.models import DataItem

logger = logging.getLogger(f"django.app.{__name__}")


@task()
def import_items():
    raw_item_file = Path('raw_items.txt')
    logger.info("Importing data items from file: %s", str(raw_item_file.absolute()))
    try:
        with raw_item_file.open() as f:
            for line in f:
                item_name = line.strip()
                if not item_name:
                    continue
                logger.info("Seeing raw data item: `%s`", item_name)
                import_item(item_name)
    except FileNotFoundError:
        logger.error("Raw data items file not found")


@db_task()
def import_item(item_name: str) -> None:
    logger.error("Attempting to import item `%s`", item_name)
    try:
        DataItem(name=item_name).save()
    except IntegrityError:
        logger.error("Not importing item `%s`, because it probably already in the database", item_name)