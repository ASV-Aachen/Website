from Django.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "secretKey"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

Host = 'localhost'
ALLOWED_HOSTS = []
ALLOWED_HOSTS.append("." + os.environ["ALLOWED_HOSTS"])

# Conection to Keycloak as OIDC

OIDC_RP_CLIENT_ID = ""
OIDC_RP_CLIENT_SECRET = ""
OIDC_RP_SIGN_ALGO = ""

# OIDC_RP_IDP_SIGN_KEY = '-----BEGIN CERTIFICATE-----  -----END CERTIFICATE-----'

OIDC_OP_JWKS_ENDPOINT = Host + '/sso/auth/realms/ASV/protocol/openid-connect/certs'
OIDC_RP_SCOPES = 'openid email profile'

OIDC_OP_AUTHORIZATION_ENDPOINT =    Host + '/sso/auth/realms/ASV/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT =            Host + '/sso/auth/realms/ASV/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT =             Host + '/sso/auth/realms/ASV/protocol/openid-connect/userinfo'


# App urls
LOGIN_REDIRECT_URL = Host
LOGOUT_REDIRECT_URL = Host + "/auth/realms/ASV/protocol/openid-connect/logout?redirect_uri=" + Host

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}