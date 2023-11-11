FROM python:3.11.4
ADD ./server /server
WORKDIR /server
EXPOSE 5001
RUN pip install -r requirements.txt
ENTRYPOINT ["python3","server.py"]
