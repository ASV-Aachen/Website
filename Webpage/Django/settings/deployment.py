from Django.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ["DEBUG"] == "True"

Host = os.environ["Host"]
ALLOWED_HOSTS = []
ALLOWED_HOSTS.append("." + os.environ["ALLOWED_HOSTS"])

# Conection to Keycloak as OIDC

OIDC_RP_CLIENT_ID = os.environ["OIDC_RP_CLIENT_ID"]
OIDC_RP_CLIENT_SECRET = os.environ["OIDC_RP_CLIENT_SECRET"]
OIDC_RP_SIGN_ALGO = os.environ["OIDC_RP_SIGN_ALGO"]

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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'websiteDB',
        'USER': os.environ["MYSQL_USER"],
        'PASSWORD': os.environ["MYSQL_PASSWORD"],
        'HOST': 'db',   # Or an IP Address that your DB is hosted on
        'PORT': 3306,
    }
}