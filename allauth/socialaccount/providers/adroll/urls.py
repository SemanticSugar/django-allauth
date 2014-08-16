from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import AdRollProvider

urlpatterns = default_urlpatterns(AdRollProvider)
