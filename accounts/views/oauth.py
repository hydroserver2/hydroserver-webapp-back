import json
from ninja import Router
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from authlib.integrations.django_client import OAuth
from accounts.utils import update_account_to_verified
from hydroserver import settings


user_model = get_user_model()

oauth = OAuth()

oauth.register(
    name='orcid',
    server_metadata_url=settings.AUTHLIB_OAUTH_CLIENTS['orcid']['server_metadata_url'],
    client_kwargs={'scope': 'openid email profile'}
)

orcid_router = Router(tags=['ORCID OAuth 2.0'])


def oauth_response(user: user_model):
    """
    The oauth_response function is used to return a response to the HydroServer client application.
    The response contains information about the user that has just signed in, and it is sent back
    to the client app using postMessage(). The message contains a JSON object with all the
    user's information.

    :param user: user_model: Pass the user object to the function
    :return: The user's information in json format
    """

    response_html = '<html><head><title>HydroServer Sign In</title></head><body></body><script>res = %value%; ' + \
                    'window.opener.postMessage(res, "*");window.close();</script></html>'

    response_html = response_html.replace(
        "%value%", json.dumps({
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'address': user.address,
                'organization': user.organization,
                'type': user.type,
                'is_verified': user.is_verified
            }
        })
    )

    return response_html


@orcid_router.get('/login')
def orcid_login(request):
    redirect_uri = request.build_absolute_uri('/api/account/orcid/auth')

    if 'X-Forwarded-Proto' in request.headers:
        redirect_uri = redirect_uri.replace('http:', request.headers['X-Forwarded-Proto'] + ':')

    return oauth.orcid.authorize_redirect(request, redirect_uri)


@orcid_router.get('/auth')
def orcid_auth(request):

    token = oauth.orcid.authorize_access_token(request)
    user_id = token.get('userinfo', {}).get('sub')

    try:
        user = user_model.objects.get(orcid=user_id)

    except user_model.DoesNotExist:
        user = user_model.objects.create_user(
            first_name=token.get('userinfo', {}).get('given_name'),
            last_name=token.get('userinfo', {}).get('family_name'),
        )

    return HttpResponse(oauth_response(user=user))


oauth.register(
    name='google',
    server_metadata_url=settings.AUTHLIB_OAUTH_CLIENTS['google']['server_metadata_url'],
    client_kwargs={'scope': 'openid email profile'}
)

google_router = Router(tags=['Google OAuth 2.0'])


@google_router.get('/login')
def google_login(request):
    redirect_uri = request.build_absolute_uri('/api/account/google/auth')

    if 'X-Forwarded-Proto' in request.headers:
        redirect_uri = redirect_uri.replace('http:', request.headers['X-Forwarded-Proto'] + ':')

    return oauth.google.authorize_redirect(request, redirect_uri)


@google_router.get('/auth')
def google_auth(request):

    token = oauth.google.authorize_access_token(request)
    user_email = token.get('userinfo', {}).get('email')

    try:
        user = user_model.objects.get(email=user_email)

    except user_model.DoesNotExist:
        user = user_model.objects.create_user(
            email=user_email,
            first_name=token.get('userinfo', {}).get('given_name'),
            last_name=token.get('userinfo', {}).get('family_name')
        )

        user = update_account_to_verified(user)

    return HttpResponse(oauth_response(user=user))
