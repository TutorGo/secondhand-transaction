FROM        gsh2448/usednara_hub
MAINTAINER  gsh2448@gmail.com

COPY        . /srv/UsedNara
WORKDIR     /srv/UsedNara
RUN         /root/.pyenv/versions/UsedNara_env/bin/pip install -r .requirements/deploy.txt
COPY        .config/uwsgi/uwsgi.conf  /etc/uwsgi/sites/uwsgi.conf
COPY        .config/supervisor/supervisor.conf /etc/supervisor/conf.d/

COPY        .config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY        .config/nginx/nginx-app.conf /etc/nginx/sites-available/nginx-app.conf
RUN         rm -rf /etc/nginx/sites-enabled/default
RUN         ln -sf /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.conf

#RUN         /root/.pyenv/versions/UsedNara_env/bin/python /srv/UsedNara/django_app/manage.py collectstatic --settings=config.settings.deploy --noinput

CMD         supervisord -n
EXPOSE      80 8000
