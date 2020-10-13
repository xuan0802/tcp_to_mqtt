import paho.mqtt.client as mqtt
import json
from tcp_mqtt_gateway import constant
import datetime
import time


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    print("Publish message with ID: ", mid)

class MQTTClient:
    def __init__(self, event_topic, data_topic, user_name, password, broker_IP, broker_port):
        self.data_topic = data_topic
        self.event_topic = event_topic
        self.user_name = user_name
        self.password = password
        self.broker_IP = broker_IP
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.current_lon = 0
        self.current_lat = 0
        self.time_gps    = time.time()
        self.time_bat    = time.time()

    def register_callbacks(self):
        self.client.on_connect = on_connect
        self.client.on_publish = on_publish

    def connect(self):
        print("Connecting to broker IP: ", self.broker_IP, "broker port: ", self.broker_port)
        self.client.username_pw_set(self.user_name, self.password)
        self.client.connect(self.broker_IP, self.broker_port, 1200)
        print("Connected to broker IP: ", self.broker_IP, "broker port: ", self.broker_port)
        self.client.reconnect()

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def publish_sos_message(self, devID, timestamp):
        sos_message = {"Type": "DeviceSoS", "DevID": devID, "CurrentPos": {"Lat": self.current_lat,
                       "Lon": self.current_lon, "TimeStamp": timestamp}}
        sos_message_json = json.dumps(sos_message)
        self.client.publish(self.event_topic, sos_message_json, qos=0)
        print("Device: ", devID, "Published an SOS Message", sos_message)

    def publish_pos_message(self, devID, lat, lon, timestamp):
        position_message = {"Type": "DevicePositionData", "DevID": devID, "CurrentPos":
            {"Lat": lat, "Lon": lon, "TimeStamp": timestamp}}
        position_message_json = json.dumps(position_message)
        self.client.publish(self.data_topic, position_message_json, qos=0)
        print("Device: ", devID, "Published an POSITION Message", position_message)

    def publish_battery_message(self, devID, battery_level, timestamp):
        battery_message = {"Type": "DeviceBatteryData", "DevID": devID, "BatteryLevel": battery_level,
                           "TimeStamp": timestamp}
        battery_message_json = json.dumps(battery_message)
        self.client.publish(self.data_topic, battery_message_json, qos=0)
        print("Device: ", devID, "Published an BATTERY Message", battery_message)

    def publish_data(self, message):
        if message.Data_Type == 'R0':
            self.current_lat = message.Longitude
            self.current_lon = message.Latitude
            if message.Event_ID == 5:
                self.publish_sos_message(message.IMEI, message.Time_Stamp)
            else:
                # Check if need to publish this GPS position message
                curr_time  = time.time()
                diff_time_gps = curr_time - self.time_gps
                if (diff_time_gps >= constant.PUBLISH_GPS_MSG_DURATION):
                    self.publish_pos_message(message.IMEI, message.Latitude, message.Longitude, message.Time_Stamp)
                    self.time_gps = curr_time


                #Check if need to publish this message
                diff_time_bat = curr_time - self.time_bat
                if (diff_time_bat >= constant.PUBLISH_BAT_MSG_DURATION):
                    self.publish_battery_message(message.IMEI, message.Battery_Percent, message.Time_Stamp)
                    self.time_bat = curr_time


        if message.Data_Type == 'R12':
            if message.Event_ID == 5:
                self.publish_sos_message(message.IMEI, message.Time_Stamp)
            else:
                #Check if need to publish this message
                curr_time = time.time()
                diff_time_bat = curr_time - self.time_bat
                if (diff_time_bat >= constant.PUBLISH_BAT_MSG_DURATION):
                    self.publish_battery_message(message.IMEI, message.Battery_Percent, message.Time_Stamp)
                    self.time_bat = curr_time

        if message.Data_Type == "R1":
            if message.Event_ID == 5:
                self.publish_sos_message(message.IMEI, message.Time_Stamp)
            else:
                #Check if need to publish this message
                curr_time = time.time()
                diff_time_bat = curr_time - self.time_bat
                if (diff_time_bat >= constant.PUBLISH_BAT_MSG_DURATION):
                    self.publish_battery_message(message.IMEI, message.Battery_Percent, message.Time_Stamp)
                    self.time_bat = curr_time

        if message.Data_Type == "R13":
            if message.Event_ID == 5:
                self.publish_sos_message(message.IMEI, message.Time_Stamp)
            else:
                #Check if need to publish this message
                curr_time = time.time()
                diff_time_bat = curr_time - self.time_bat
                if (diff_time_bat >= constant.PUBLISH_BAT_MSG_DURATION):
                    self.publish_battery_message(message.IMEI, message.Battery_Percent, message.Time_Stamp)
                    self.time_bat = curr_time

        if message.Data_Type == "R2":
            if message.Event_ID == 5:
                self.publish_sos_message(message.IMEI, message.Time_Stamp)
            else:
                #Check if need to publish this message
                curr_time = time.time()
                diff_time_bat = curr_time - self.time_bat
                if (diff_time_bat >= constant.PUBLISH_BAT_MSG_DURATION):
                    self.publish_battery_message(message.IMEI, message.Battery_Percent, message.Time_Stamp)
                    self.time_bat = curr_time

        if message.Data_Type == "R3":
            if message.Event_ID == 5:
                self.publish_sos_message(message.IMEI, message.Time_Stamp)
            else:
                #Check if need to publish this message
                curr_time = time.time()
                diff_time_bat = curr_time - self.time_bat
                if (diff_time_bat >= constant.PUBLISH_BAT_MSG_DURATION):
                    self.publish_battery_message(message.IMEI, message.Battery_Percent, message.Time_Stamp)
                    self.time_bat = curr_time


        if message.Data_Type == "RH":
            if message.Event_ID == 5:
                self.publish_sos_message(message.IMEI, message.Time_Stamp)
            else:
                #Check if need to publish this message
                curr_time = time.time()
                diff_time_bat = curr_time - self.time_bat
                if (diff_time_bat >= constant.PUBLISH_BAT_MSG_DURATION):
                    self.publish_battery_message(message.IMEI, message.Battery_Percent, message.Time_Stamp)
                    self.time_bat = curr_time