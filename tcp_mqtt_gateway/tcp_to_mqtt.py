#!/usr/bin/env python3

from tcp_mqtt_gateway.server import Server
from tcp_mqtt_gateway import constant
from tcp_mqtt_gateway import mqtt_client


import socket
import selectors
import traceback
import queue

# set up socket to listen packets
sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((constant.HOST, constant.PORT))
lsock.listen()
print("listening on", constant.HOST, constant.PORT)
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


# set up mqtt client for multiple things to publish data
#Thing 3
mqtt_client_T3 = mqtt_client.MQTTClient(constant.EVENTS_TOPIC_T3, constant.DATA_TOPIC_T3, constant.USER_NAME_T3, constant.PASSWORD_T3,
                                     constant.BROKER_IP, constant.BROKER_PORT)
mqtt_client_T3.register_callbacks()
mqtt_client_T3.connect()
mqtt_client_T3.loop_start()


#Thing 4
mqtt_client_T4 = mqtt_client.MQTTClient(constant.EVENTS_TOPIC_T4, constant.DATA_TOPIC_T4, constant.USER_NAME_T4, constant.PASSWORD_T4,
                                     constant.BROKER_IP, constant.BROKER_PORT)
mqtt_client_T4.register_callbacks()
mqtt_client_T4.connect()
mqtt_client_T4.loop_start()

#Thing 5
mqtt_client_T5 = mqtt_client.MQTTClient(constant.EVENTS_TOPIC_T5, constant.DATA_TOPIC_T5, constant.USER_NAME_T5, constant.PASSWORD_T5,
                                     constant.BROKER_IP, constant.BROKER_PORT)
mqtt_client_T5.register_callbacks()
mqtt_client_T5.connect()
mqtt_client_T5.loop_start()

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=Server(sel, conn ))

try:
    while True:
        # check read and write events to perform read and write on sockets
        events = sel.select(timeout=None)
        # if this flag is set, send inform progress packet to sender

        # read from queue and publish to broker server
        if constant.msg_queue.qsize():
            message = constant.msg_queue.get()

            sender_IMEI = message.IMEI

            if (sender_IMEI == constant.IMEI_T3):
                mqtt_client_T3.publish_data(message)
            elif (sender_IMEI == constant.IMEI_T4):
                mqtt_client_T4.publish_data(message)
            elif (sender_IMEI == constant.IMEI_T5):
                mqtt_client_T5.publish_data(message)

        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                data = key.data
                try:
                    data.process_events(mask)
                except Exception:
                    print("main: error: exception for", traceback.format_exc())
                    data.close()

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
