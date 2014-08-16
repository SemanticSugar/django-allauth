import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import AdRollProvider


class AdRollOAuth2Adapter(OAuth2Adapter):
    provider_id = AdRollProvider.id
    # access_token_url = 'https://accounts.adroll.com/o/oauth2/token'
    # authorize_url = 'https://accounts.adroll.com/o/oauth2/auth'
    # profile_url = 'https://www.adrollapis.com/oauth2/v1/userinfo'
    access_token_url = 'https://127.0.0.1:8000/oauth2/token'
    authorize_url = 'https://127.0.0.1:8000/oauth2/auth'
    profile_url = 'https://www.adrollapis.com/oauth2/v1/userinfo'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token,
                                    'alt': 'json'})
        extra_data = resp.json()
        login = self.get_provider() \
            .sociallogin_from_response(request,
                                       extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(AdRollOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AdRollOAuth2Adapter)
