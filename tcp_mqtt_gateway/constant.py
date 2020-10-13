import queue

# server port and IP
#HOST = "172.31.3.76"
HOST = "0.0.0.0"
PORT = 4446

# broker info
#BROKER_IP = "203.113.138.21"
BROKER_IP = "10.55.123.94"
BROKER_PORT = 4444


#THING3
IMEI_T3 = '862785045422907'
#Config for tcdt account
#DATA_TOPIC_T3 = "channels/c99d2313-a9ab-4052-acc3-83a2a4c89883/messages/data"
#EVENTS_TOPIC_T3 = "channels/c99d2313-a9ab-4052-acc3-83a2a4c89883/messages/events"
#USER_NAME_T3 = "72622d67-ce99-48d6-890d-2e705024be46"
#PASSWORD_T3 = "97734c42-a2cb-40b5-be04-984e2106ba5f"

#Config for tcdt1 account (Cuc BDTW)
DATA_TOPIC_T3 = "channels/290120d3-2cf5-4599-905f-8b81c94f2536/messages/data"
EVENTS_TOPIC_T3 = "channels/290120d3-2cf5-4599-905f-8b81c94f2536/messages/events"
USER_NAME_T3 = "bcd7bfbb-dcda-451f-bcc8-c2553dd205a4"
PASSWORD_T3 = "0123456789test1"


#THING4
IMEI_T4 = '862785045412718'
DATA_TOPIC_T4 = "channels/93ad74a3-be70-498b-b64d-1e4b492fd1dc/messages/data"
EVENTS_TOPIC_T4 = "channels/93ad74a3-be70-498b-b64d-1e4b492fd1dc/messages/events"
USER_NAME_T4 = "c39a9fcd-044f-4959-a217-7e7611b9f29b"
PASSWORD_T4 = "3c37bb79-2f0b-43a5-90b5-4e89ffaae721"

#THING5
IMEI_T5 = '862785045414235'
DATA_TOPIC_T5 = "channels/2161be76-2c15-4c18-9239-e37ef159f755/messages/data"
EVENTS_TOPIC_T5 = "channels/2161be76-2c15-4c18-9239-e37ef159f755/messages/events"
USER_NAME_T5 = "fffc6297-5b03-4e06-a150-1f542c4a449d"
PASSWORD_T5 = "42f17f2d-6ce4-434a-b0a4-236c5e12d36b"


# BROKER_IP = "5.196.95.208"
# BROKER_PORT = 1883


# message_queue
msg_queue = queue.Queue()

REPORT_GPS_DATA = b"R0"
REPORT_WIFI_DATA = b"R1"
REPORT_WIFI_GSM_CELL = b"R12"
REPORT_WIFI_LTE_CELL = b"R13"
REPORT_GSM_CELL = b"R2"
REPORT_LTE_CELL = b"R3"
REPORT_HEAT_BEAT = b"RH"
REPORT_DEVICE_BINDING = b"B"


SEPARATOR_LENGTH = 1
HEAD_LENGTH = 2
MODE_LENGTH = 1
IMEI_LENGTH = 15
DATA_TYPE_LENGTH = 3

REPORT_GPS_DATA_LENGTH = 60
REPORT_WIFI_DATA_LENGTH = 67
REPORT_WIFI_GSM_CELL_LENGTH = 89
REPORT_WIFI_LTE_CELL_LENGTH = 94
REPORT_GSM_CELL_LENGTH = 46
REPORT_LTE_CELL_LENGTH = 50
REPORT_HEAT_BEAT_LENGTH = 34
REPORT_DEVICE_BINDING_LENGTH = 22

INFO_GPS_DATA       = ['Sat_No', 'Time_Stamp', 'Latitude', 'Longitude', 'Speed', 'Heading', 'Event_ID', 'Bat_Votage', 'Sequence_No']
INFO_WIFI_DATA      = ['Time_Stamp', 'MAC1', 'RSSI1', 'MAC2', 'RSSI2', 'Event_ID', 'Bat_Voltage', 'Sequence_No']
INFO_WIFI_GSM_CELL  = ['Time_Stamp', 'MAC1', 'RSSI1', 'MAC2', 'RSSI2', 'MNC', 'Cell_ID', 'LAC', 'MCC', 'Event_ID', 'Bat_Voltage', 'Sequence_No']
INFO_WIFI_LTE_CELL  = ['Time_Stamp', 'MAC1', 'RSSI1', 'MAC2', 'RSSI2', 'MNC', 'Cell_ID', 'LAC', 'MCC', 'PCID', 'Event_ID', 'Bat_Voltage', 'Sequence_No']
INFO_GSM_CELL       = ['Time_Stamp', 'MNC', 'Cell_ID', 'LAC', 'MCC', 'Event_ID', 'Bat_Voltage', 'Sequence_No']
INFO_LTE_CELL       = ['Time_Stamp', 'MNC', 'Cell_ID', 'LAC', 'MCC', 'PCID', 'Event_ID', 'Bat_Voltage', 'Sequence_No']
INFO_HEART_BEAT     = ['Sat_No', 'Time_Stamp', 'FixValue1', 'FixValue2', 'FixValue3', 'FixValue4','Event_ID', 'Bat_Voltage','Sequence_No']

MAX_VOLTAGE_LEVEL = 4.20
MIN_VOLTAGE_LEVEL = 3.31

PUBLISH_BAT_MSG_DURATION = 150  #seconds
PUBLISH_GPS_MSG_DURATION = 15   #seconds

