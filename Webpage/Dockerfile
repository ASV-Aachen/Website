FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Install Dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

# install Stuff for the Keycloak service
RUN pip install git+https://github.com/jhuapl-boss/django-oidc.git
RUN pip install git+https://github.com/jhuapl-boss/drf-oidc-auth.git
RUN pip install git+https://github.com/jhuapl-boss/boss-oidc.git


COPY / /



# CMD python manage.py migrate
CMD [ "python3", "-u"," manage.py" , "migrate"]