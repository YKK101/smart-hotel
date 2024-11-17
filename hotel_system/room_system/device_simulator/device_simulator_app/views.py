from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
import json
from django.views.decorators.csrf import csrf_exempt # FIXME: HANDLE SECURITY

@csrf_exempt # FIXME: HANDLE SECURITY
@require_http_methods('PUT')
def update_iaq_device(request):
    print(f'Receive command from device controller for {settings.DEVICE_ID}, command = {json.loads(request.body)}')

    return JsonResponse({ 'success': True })