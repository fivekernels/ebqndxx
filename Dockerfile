FROM python:latest

WORKDIR /home

ADD ./docker ./docker

RUN pip install -r ./docker/requirements.txt

# 修改默认源为中国大陆
RUN cp /etc/apt/sources.list /etc/apt/sources.list.backup && \
    sed -i 's/deb.debian.org/ftp.cn.debian.org/g' /etc/apt/sources.list
# RUN echo "# deb http://snapshot.debian.org/archive/debian/20211115T000000Z bullseye main" > /etc/apt/sources.list && \
#     echo "deb http://ftp.cn.debian.org/debian bullseye main" >> /etc/apt/sources.list && \
#     echo "# deb http://snapshot.debian.org/archive/debian-security/20211115T000000Z bullseye-security main" >> /etc/apt/sources.list && \
#     echo "deb http://security.debian.org/debian-security bullseye-security main" >> /etc/apt/sources.list && \
#     echo "# deb http://snapshot.debian.org/archive/debian/20211115T000000Z bullseye-updates main" >> /etc/apt/sources.list && \
#     echo "deb http://ftp.cn.debian.org/debian bullseye-updates main" >> /etc/apt/sources.list

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN apt update && \
    apt install -y --no-install-recommends \
    cron rsyslog && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean


# RUN /etc/init.d/rsyslog restart

# ADD ./crontab_autodxx /etc/cron.d/crontab

# RUN chmod 0644 /etc/cron.d/crontab
RUN touch /var/log/cron.log

# CMD cron && tail -f /var/log/cron.log