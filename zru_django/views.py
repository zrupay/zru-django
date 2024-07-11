from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import json

from . import ZRUClient
from .signals import notification_received


class ZRUNotifyView(View):
    """
    View to receive notification
    """
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ZRUNotifyView, self).dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        body_content = request.body.decode('utf-8')
        json_body = json.loads(body_content)

        zru = ZRUClient()

        check_signature = True

        try:
            check_signature = settings.ZRU_CONFIG['CHECK_SIGNATURE_ON_NOTIFICATION']
        except:
            pass

        notification_data = zru.NotificationData(json_body)

        if not check_signature or notification_data.check_signature():
            notification_received.send(sender=notification_data)

        return HttpResponse('OK')
