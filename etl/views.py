import logging

from django.shortcuts import render, redirect
from huey.contrib.djhuey import HUEY
from huey.exceptions import TaskException

from .models import DataItem
from .tasks import import_items

logger = logging.getLogger(f"django.app.{__name__}")


def all_task_results():
    for key in HUEY.all_results():
        try:
            yield key, False, HUEY.result(key, blocking=False, preserve=True)
        except TaskException as e:
            yield key, True, e


def list_items(request):
    return render(
        request, "etl/list_items.html", {
            "data_items": DataItem.objects.all(),
            "pending_tasks": HUEY.pending(),
            "scheduled_tasks": HUEY.scheduled(),
            "all_task_results": list(all_task_results()),
        },
    )


def manual_import(request):
    logger.info("Launching import task")
    import_items()
    return redirect('list_items')


def clear_items(request):
    logger.info("Clearing all items")
    DataItem.objects.all().delete()
    return redirect('list_items')
