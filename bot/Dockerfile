FROM python:3.10.6
EXPOSE 8080
COPY . /bot
WORKDIR /bot
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "discord_bot.py"]