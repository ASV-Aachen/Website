FROM python:3.9
ENV PYTHONUNBUFFERED=1

# Install Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY Webpage/ /opt/Webpage/

# Add our custom crt
ADD InitFiles/traefik/server.crt /usr/local/share/ca-certificates/foo.crt
RUN chmod 644 /usr/local/share/ca-certificates/foo.crt && update-ca-certificates

WORKDIR /opt/Webpage/

# CMD python manage.py migrate
CMD [ "python3", "manage.py", "migrate"]
