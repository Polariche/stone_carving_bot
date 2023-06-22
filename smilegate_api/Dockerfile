FROM python:3.10.6
EXPOSE 8080
COPY . /smilegate_api
WORKDIR /smilegate_api
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "-u", "query_server.py"]
