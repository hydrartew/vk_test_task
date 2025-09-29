FROM ubuntu:latest

RUN apt-get update && apt-get install -y cron

# Копируем скрипт
COPY myscript.sh myscript.sh
RUN chmod +x myscript.sh

# Копируем crontab
COPY crontab /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron
RUN echo "" >> /etc/cron.d/mycron

# Запускаем cron
CMD cron && tail -f /var/log/syslog
