from pathlib import Path
import logging

from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import DataItem
from .tasks import import_items

logger = logging.getLogger(f"django.app.{__name__}")


def list_items(request):
    return render(request, "etl/list_items.html", {"data_items": DataItem.objects.all()})


def manual_import(request):
    logger.info("Launching import task")
    import_items()
    return redirect('list_items')


def clear_items(request):
    logger.info("Clearing all items")
    DataItem.objects.all().delete()
    return redirect('list_items')
