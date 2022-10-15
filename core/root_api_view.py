from dj_rest_auth.urls import urlpatterns as dj_rest_auth_urlpatterns
from django.conf import settings
from django.urls import include
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


def get_all_dj_rest_auth_urlnames(request):

    """
        dj_rest_auth urls are sourced and combined with respective names in a dictionary -> returned and added to api_root

        urlpatterns = [
        # URLs that do not require a session or valid token
        path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
        path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
        path('login/', LoginView.as_view(), name='rest_login'),
        # URLs that require a user to be logged in with a valid session / token.
        path('logout/', LogoutView.as_view(), name='rest_logout'),
        path('user/', UserDetailsView.as_view(), name='rest_user_details'),
        path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    ]

    if getattr(settings, 'REST_USE_JWT', False):
        from rest_framework_simplejwt.views import TokenVerifyView

        from dj_rest_auth.jwt_auth import get_refresh_view

        urlpatterns += [
            path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
            path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
        ]"""

    dj_rest_auth_url_reverse = {}
    for pattern in dj_rest_auth_urlpatterns:
        dj_rest_auth_url_reverse[pattern.name] = reverse(pattern.name, request=request)

    return dj_rest_auth_url_reverse


@extend_schema(
    description="THis is just an api root with listed urls to respective endpoints",
    responses={
        200: inline_serializer(name="api_root", fields={"endpoint name": serializers.CharField()}, many=True),
    },
    examples=[OpenApiExample(name="example1", value={"endpoint_name": "url_to_endpoint"})],
)
@api_view(["GET"])
def api_root(request, format=None):

    name_links_dictionary = {
        "apps": reverse("api-root", request=request),  # main default router
        "obtain_token": reverse("token_obtain_pair", request=request),
        "register": reverse("rest_register", request=request),
    }

    # complement root url dictionary with the dj-rest-auth endpoints
    dj_rest_auth_links = get_all_dj_rest_auth_urlnames(request)
    name_links_dictionary.update(dj_rest_auth_links)

    # DRF Spectacular overrides DRF's default solution. The main changing point is settings.REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"]
    # depends on the settings root url changes
    if settings.REST_FRAMEWORK.get("DEFAULT_SCHEMA_CLASS") == "drf_spectacular.openapi.AutoSchema":
        name_links_dictionary.update({"schema": reverse("swagger-ui", request=request, format=format)})
    else:
        name_links_dictionary.update({"schema": reverse("openapi-schema-drf", request=request, format=format)})

    return Response(name_links_dictionary)


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
