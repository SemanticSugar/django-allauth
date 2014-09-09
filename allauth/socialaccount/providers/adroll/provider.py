from allauth.account.models import EmailAddress
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import (ProviderAccount,
                                                  AuthAction)
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.app_settings import QUERY_EMAIL
from allauth.account.utils import user_email


class Scope(object):
    EMAIL = 'email'
    PROFILE = 'profile'


class AdRollAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('link')

    def get_avatar_url(self):
        return self.account.extra_data.get('picture')

    def to_str(self):
        dflt = super(AdRollAccount, self).to_str()
        return self.account.extra_data.get('name', dflt)


class AdRollProvider(OAuth2Provider):
    id = 'adroll'
    name = 'AdRoll'
    package = 'allauth.socialaccount.providers.adroll'
    account_class = AdRollAccount

    def get_default_scope(self):
        return ['read']

    def get_auth_params(self, request, action):
        ret = super(AdRollProvider, self).get_auth_params(request,
                                                          action)
        if action == AuthAction.REAUTHENTICATE:
            ret['approval_prompt'] = 'force'
        return ret

    def extract_uid(self, data):
        return str(data['eid'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    username=data.get('username'),
                    last_name=data.get('first_name'),
                    first_name=data.get('last_name'))

    def extract_email_addresses(self, data):
        ret = []
        email = data.get('email')
        if email and data.get('verified_email', False):
            ret.append(EmailAddress(email=email,
                       verified=True,
                       primary=True))
        return ret


providers.registry.register(AdRollProvider)
