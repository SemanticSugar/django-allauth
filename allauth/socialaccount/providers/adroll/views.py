import logging

import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import AdRollProvider


class AdRollOAuth2Adapter(OAuth2Adapter):
    provider_id = AdRollProvider.id
    access_token_url = 'https://login.adroll.com/oauth2/access_token'
    authorize_url = 'https://login.adroll.com/oauth2/authorize'
    profile_url = 'https://login.adroll.com/api/users/profile/'

    def complete_login(self, request, app, token, **kwargs):
        auth = (app.client_id, token.token)
        resp = requests.get(self.profile_url,
                            params={'format': 'json'},
                            auth=auth)
        extra_data = resp.json()
        login = self.get_provider() \
            .sociallogin_from_response(request,
                                       extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(AdRollOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AdRollOAuth2Adapter)
