FROM python:latest

WORKDIR /home

ADD ./docker ./docker
RUN pip install -r ./docker/requirements.txt

RUN apt update && \
    apt install -y --no-install-recommends \
    cron rsyslog && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

# RUN apt install rsyslog

# RUN apt install -y \
#     rsyslog && \
#     rm -rf /var/lib/apt/lists/* && \
#     apt clean
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN /etc/init.d/rsyslog restart

ADD ./crontab_autodxx /etc/cron.d/crontab

# RUN chmod 0644 /etc/cron.d/crontab
RUN touch /var/log/cron.log

# CMD cron && tail -f /var/log/cron.log