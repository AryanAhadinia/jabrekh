from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden

from .models import FileMaterial


def ping(request):
    return HttpResponse("pong")


def file(request, file_name):
    user = request.user
    if not file_name:
        return HttpResponseBadRequest()
    file = FileMaterial.objects.get(name=file_name)
    if not file.has_access(user):
        return HttpResponseForbidden()
    response = HttpResponse(file.file, content_type="application/octet-stream")
    response["Content-Disposition"] = f"attachment; filename={file.get_file_name()}"
    return response
