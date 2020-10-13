FROM python:3.6-alpine

ADD ./ tcp_to_mqtt/

WORKDIR tcp_to_mqtt

ENV PATH=$PATH:/tcp_to_mqtt
ENV PYTHONPATH /tcp_to_mqtt

CMD ["python3", "tcp_mqtt_gateway/tcp_to_mqtt.py"]

