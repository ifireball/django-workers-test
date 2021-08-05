from pathlib import Path
import logging

from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import DataItem


logger = logging.getLogger(f"django.app.{__name__}")


def list_items(request):
    return render(request, "etl/list_items.html", {"data_items": DataItem.objects.all()})


def manual_import(request):
    raw_item_file = Path('raw_items.txt')
    logger.info("Importing data items from file: %s", str(raw_item_file.absolute()))
    try:
        with raw_item_file.open() as f:
            for line in f:
                item_name = line.strip()
                logger.info("Seeing raw data item: `%s`", item_name)
                try:
                    DataItem(name=item_name).save()
                except IntegrityError:
                    logger.error("Not importing item `%s`, because it probably already in the database", item_name)
    except FileNotFoundError:
        logger.error("Raw data items file not found")
    return redirect('list_items')

