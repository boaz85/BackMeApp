import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from backmeapp import settings
from commons.enums import ServiceTypeEnum
from social.apps.django_app.default.models import UserSocialAuth

from users.serializers import UserSerializer

@login_required
def is_authorized(request):

    service_name = request.GET.get('service', None)

    if service_name is None:
        return HttpResponse(status=400)

    is_auth = request.user.social_auth.filter(provider=service_name).exists()
    return HttpResponse(content=str(is_auth))

def user_data(request):

    user = request.user

    if user.is_anonymous() or not user.is_active:
        data = {'isLoggedIn': False}

    else:
        data = UserSerializer(request.user).data

    return HttpResponse(content=json.dumps(data), content_type='application/json')

class MainPage(TemplateView):

    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):

        context = super(MainPage, self).get_context_data(**kwargs)
        context['services_types'] = {item.slug.upper(): item.order for item in ServiceTypeEnum.get_items()}
        return context


@login_required
def auth_popup_complete(request):

    template = "<html><body><script>window.opener.onAuthFinish()</script></body></html>"
    return HttpResponse(content=template, content_type="text/html")