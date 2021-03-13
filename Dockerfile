FROM python:3.9.1-slim

ADD ./ /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "/app/splatnet2statink.py"]
