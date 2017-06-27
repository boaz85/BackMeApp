import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from backmeapp.settings import ServicesData
from services.services_helpers.commons import AuthException
from social.apps.django_app.utils import load_strategy
from social.apps.django_app.default.models import UserSocialAuth


#@cache_page(30 * 60)
def services_data(request):

    data = ServicesData.get_serialized()
    return HttpResponse(content=data, content_type='application/json')

@login_required
def user_email_groupers(request):

    email_service_slug = request.GET.get('service')
    user = request.user
    service_data = ServicesData.from_slug(email_service_slug)

    try:
        email_user = user.social_auth.get(provider=email_service_slug)
    except UserSocialAuth.DoesNotExist:
        return HttpResponse(status=400)

    access_token = email_user.extra_data.get('access_token')
    email_client_helper = service_data.helper_class(username=user.email, access_token=access_token)
    try:
        email_client_helper.login()
    except AuthException:
        strategy = load_strategy()
        email_user.refresh_token(strategy)
        try:
            access_token = email_user.extra_data.get('access_token')
            email_client_helper = service_data.helper_class(username=user.email, access_token=access_token)
            email_client_helper.login()
        except AuthException:
            return HttpResponse(status=400)

    all_groupers = email_client_helper.get_groupers()
    chosen_groupers = user.email_groupers.filter(service=service_data.order).values_list('display_name')

    response_data = {'all_groupers': all_groupers,
                     'selected_groupers': list(chosen_groupers)}

    return HttpResponse(content=json.dumps(response_data), content_type='application/json')