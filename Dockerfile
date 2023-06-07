FROM python:3.10.6
EXPOSE 8080
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "discord_bot.py"]