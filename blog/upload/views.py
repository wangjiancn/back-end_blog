import os
import uuid

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from acl.auth_wrap import token_required
from utils.api_response import APIResponse
from utils.api_response import APIResponseError
# Create your views here.
from utils.qiniu_tool import get_qiniu_token


def handle_upload_file(file, path):
    with open(path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


@require_POST
@csrf_exempt
def upload_image(r):
    files = r.FILES
    image = files.get('image')
    if not image:
        return APIResponseError(12002)
    name: str = image.name
    try:
        ext = name.rsplit('.')[1]
    except IndexError:
        return APIResponseError(12001)
    file_name = uuid.uuid4().hex + '.' + ext
    path = os.path.join(settings.ENV_UPLOAD_PATH, 'images', file_name)

    url = os.path.join(settings.STATIC_URL, os.path.join('images', file_name))
    handle_upload_file(image, path)

    return APIResponse(url)


@require_GET
@csrf_exempt
@token_required
def get_qiniu_token_view(r):
    token = get_qiniu_token(prefix='')
    return APIResponse(token)
