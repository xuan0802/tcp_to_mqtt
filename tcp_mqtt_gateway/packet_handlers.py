import struct
import math
from tcp_mqtt_gateway import constant
from tcp_mqtt_gateway.packet_decode import *


class GpsDataMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'R0'
    Sat_No = 0
    Time_Stamp = ''
    Latitude = 0.0
    Longitude = 0.0
    Speed = 0.0
    Heading = 0.0
    Event_ID = 0
    Battery_Voltage = 0.0
    Battery_Percent = 0
    Sequence_Number = 0


class WifiDataMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'R1'
    Time_Stamp = ''
    MAC1 = ''
    RSSI1 = 0.0
    MAC2 = ''
    RSSI2 = 0.0
    Event_ID = 0
    Battery_Voltage = 0.0
    Battery_Percent = 0
    Sequence_Number = 0


class WifiGsmCellMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'R12'
    Time_Stamp = ''
    MAC1 = ''
    RSSI1 = 0.0
    MAC2 = ''
    RSSI2 = 0.0
    MNC = 0
    Cell_ID = 0
    LAC = 0
    MCC = 0
    Event_ID = 0
    Battery_Voltage = 0.0
    Battery_Percent = 0
    Sequence_Number = 0


class WifiLteCellMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'R13'
    Time_Stamp = ''
    MAC1 = ''
    RSSI1 = 0.0
    MAC2 = ''
    RSSI2 = 0.0
    MNC = 0
    Cell_ID = 0
    LAC = 0
    MCC = 0
    PCID = 0
    Event_ID = 0
    Battery_Voltage = 0.0
    Battery_Percent = 0
    Sequence_Number = 0


class GsmCellMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'R2'
    Time_Stamp = ''
    MNC = 0
    Cell_ID = 0
    LAC = 0
    MCC = 0
    Event_ID = 0
    Battery_Voltage = 0.0
    Battery_Percent = 0
    Sequence_Number = 0


class LtcCellMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'R3'
    Time_Stamp = ''
    MNC = 0
    Cell_ID = 0
    LAC = 0
    MCC = 0
    PCID = 0
    Event_ID = 0
    Battery_Voltage = 0.0
    Battery_Percent = 0
    Sequence_Number = 0


class HeartBeatMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'RH'
    Sat_No = 0
    Time_Stamp = ''
    Fix_Value1 = ''
    Fix_Value2 = ''
    Fix_Value3 = ''
    Fix_Value4 = ''
    Event_ID = 0
    Battery_Voltage = 0.0
    Battery_Percent = 0
    Sequence_Number = 0


class DeviceBindingMsg:
    Mode = ''
    IMEI = ''
    Data_Type = 'B'

def cal_battery_percentage(bat_voltage):
    if (bat_voltage >= constant.MAX_VOLTAGE_LEVEL):
        return 100
    elif (bat_voltage < constant.MIN_VOLTAGE_LEVEL):
        return 1
    else:
        bat_percentage = -236.8832472154429*pow(bat_voltage,3) + 2645.043986447070*pow(bat_voltage,2) - 9685.274190037062*bat_voltage + 11669.61656992294
        bat_percentage = math.floor(bat_percentage)
        return int(bat_percentage)


def process_packet(rcv_buf):
    packet_decoder = {
        constant.REPORT_GPS_DATA: handle_gps_report,
        constant.REPORT_GSM_CELL: handle_gsm_cell_report,
        constant.REPORT_HEAT_BEAT: handle_heart_beat_report,
        constant.REPORT_LTE_CELL: handle_lte_cell_report,
        constant.REPORT_WIFI_DATA: handle_wifi_data_report,
        constant.REPORT_WIFI_GSM_CELL: handle_wifi_gsm_cell_report,
        constant.REPORT_WIFI_LTE_CELL: handle_wifi_lte_cell_report,
        constant.REPORT_DEVICE_BINDING: handle_data_binding_report,
    }

    # decode report data header
    head_header, mode_header, imei_header, data_type_header, rcv_buffer, report_decode_len = decode_report_header(rcv_buf)

    # decode each type of packet
    print(rcv_buffer)
    decode_length, decode_msg, decode_flg = packet_decoder[data_type_header](rcv_buffer)

    decode_msg.Mode = mode_header.decode()
    decode_msg.IMEI = imei_header.decode()

    if decode_flg == 1:
        constant.msg_queue.put(decode_msg)

    return decode_length + report_decode_len, decode_msg, decode_flg


def handle_gps_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    # Initialize decode message struct
    decode_msg = GpsDataMsg()

    #Check length of out_data to make sure enough fields of this messages
    if len(out_data) == len(constant.INFO_GPS_DATA):
        decode_flg = 1
        #Sat No.
        decode_msg.Sat_No = int(out_data[0])
        #Time_stamp
        utc_ts = out_data[1]
        yy = utc_ts[0:2]
        mm = utc_ts[2:4]
        dd = utc_ts[4:6]
        hh = utc_ts[6:8]
        tmp_hh = int(hh) + 7 #convert utc time to VN time
        hh = str(tmp_hh)
        mmin = utc_ts[8:10]
        ss = utc_ts[10:12]

        decode_msg.Time_Stamp = hh+':'+mmin+':'+ss+'+'+dd+'-'+mm+'-' + yy
        #Latitude
        decode_msg.Latitude = float(out_data[2])
        #Longitude
        decode_msg.Longitude = float(out_data[3])
        #Speed
        decode_msg.Speed = float(out_data[4])
        #Heading
        decode_msg.Heading = float(out_data[5])
        #Event_ID
        decode_msg.Event_ID = int(out_data[6])
        #Battery_Voltage
        decode_msg.Battery_Voltage = float(out_data[7])/1000.0
        #Battery_Percent
        #decode_msg.Battery_Percent = int(decode_msg.Battery_Voltage*100.0/constant.MAX_VOLTAGE_LEVEL)
        decode_msg.Battery_Percent = cal_battery_percentage(decode_msg.Battery_Voltage)
        #Sequence Number
        decode_msg.Sequence_Number = int(out_data[8])
    else:
        decode_flg = 0
    return len(rcv_buff), decode_msg, decode_flg

def handle_wifi_data_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    #Initialize decode message struct
    decode_msg = WifiDataMsg()

    #Check length of out_data to make sure enough fields of this messages
    if len(out_data) == len(constant.INFO_WIFI_DATA):
        decode_flg = 1
        #Time_stamp
        utc_ts = out_data[0]
        yy = utc_ts[0:2]
        mm = utc_ts[2:4]
        dd = utc_ts[4:6]
        hh = utc_ts[6:8]
        tmp_hh = int(hh) + 7 #convert utc time to VN time
        hh = str(tmp_hh)
        mmin = utc_ts[8:10]
        ss = utc_ts[10:12]
        decode_msg.Time_Stamp = hh+':'+mmin+':'+ss+'+'+dd+'-'+mm+'-' + yy
        #MAC1
        decode_msg.MAC1 = out_data[1]
        #RSSI1
        decode_msg.RSSI1 = float(out_data[2])
        #MAC2
        decode_msg.MAC2 = out_data[3]
        #RSSI2
        decode_msg.RSSI2 = float(out_data[4])
        #Event_ID
        decode_msg.Event_ID = int(out_data[5])
        #Battery Voltage
        decode_msg.Battery_Voltage = float(out_data[6])/1000.0
        # Battery_Percent
        #decode_msg.Battery_Percent = int(decode_msg.Battery_Voltage * 100.0 / constant.MAX_VOLTAGE_LEVEL)
        decode_msg.Battery_Percent = cal_battery_percentage(decode_msg.Battery_Voltage)
        #Sequence Number
        decode_msg.Sequence_Number = int(out_data[7])
    else:
        decode_flg = 0

    return len(rcv_buff), decode_msg, decode_flg


def handle_wifi_gsm_cell_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    # Initialize decode message struct
    decode_msg = WifiGsmCellMsg()

    # Check length of out_data to make sure enough fields of this messages
    if len(out_data) == len(constant.INFO_WIFI_GSM_CELL):
        decode_flg = 1
        # Time_stamp
        utc_ts = out_data[0]
        yy = utc_ts[0:2]
        mm = utc_ts[2:4]
        dd = utc_ts[4:6]
        hh = utc_ts[6:8]
        tmp_hh = int(hh) + 7  # convert utc time to VN time
        hh = str(tmp_hh)
        mmin = utc_ts[8:10]
        ss = utc_ts[10:12]
        decode_msg.Time_Stamp = hh + ':' + mmin + ':' + ss + '+' + dd + '-' + mm + '-' + yy
        # MAC1
        decode_msg.MAC1 = out_data[1]
        # RSSI1
        decode_msg.RSSI1 = float(out_data[2])
        # MAC2
        decode_msg.MAC2 = out_data[3]
        # RSSI2
        decode_msg.RSSI2 = float(out_data[4])
        #MNC
        decode_msg.MNC = int(out_data[5])
        #Cell_ID
        decode_msg.Cell_ID = int(out_data[6])
        #LAC
        decode_msg.LAC = int(out_data[7])
        #MCC
        decode_msg.MCC = int(out_data[8])
        #Event_ID
        decode_msg.Event_ID = int(out_data[9])
        #Battery_Voltage
        decode_msg.Battery_Voltage = float(out_data[10])/1000.0
        # Battery_Percent
        #decode_msg.Battery_Percent = int(decode_msg.Battery_Voltage * 100.0 / constant.MAX_VOLTAGE_LEVEL)
        decode_msg.Battery_Percent = cal_battery_percentage(decode_msg.Battery_Voltage)
        #Sequence_Number
        decode_msg.Sequence_Number = int(out_data[11])
    else:
        decode_flg = 0

    return len(rcv_buff), decode_msg, decode_flg

def handle_wifi_lte_cell_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    # Initialize decode message struct
    decode_msg = WifiLteCellMsg()

    # Check length of out_data to make sure enough fields of this messages
    if len(out_data) == len(constant.INFO_WIFI_LTE_CELL):
        decode_flg = 1
        # Time_stamp
        utc_ts = out_data[0]
        yy = utc_ts[0:2]
        mm = utc_ts[2:4]
        dd = utc_ts[4:6]
        hh = utc_ts[6:8]
        tmp_hh = int(hh) + 7  # convert utc time to VN time
        hh = str(tmp_hh)
        mmin = utc_ts[8:10]
        ss = utc_ts[10:12]
        decode_msg.Time_Stamp = hh + ':' + mmin + ':' + ss + '+' + dd + '-' + mm + '-' + yy
        # MAC1
        decode_msg.MAC1 = out_data[1]
        # RSSI1
        decode_msg.RSSI1 = float(out_data[2])
        # MAC2
        decode_msg.MAC2 = out_data[3]
        # RSSI2
        decode_msg.RSSI2 = float(out_data[4])
        #MNC
        decode_msg.MNC = int(out_data[5])
        #Cell_ID
        decode_msg.Cell_ID = int(out_data[6])
        #LAC
        decode_msg.LAC = int(out_data[7])
        #MCC
        decode_msg.MCC = int(out_data[8])
        #PCID
        decode_msg.PCID = int(out_data[9])
        #Event_ID
        decode_msg.Event_ID = int(out_data[10])
        #Battery_Voltage
        decode_msg.Battery_Voltage = float(out_data[11])/1000.0
        # Battery_Percent
        #decode_msg.Battery_Percent = int(decode_msg.Battery_Voltage * 100.0 / constant.MAX_VOLTAGE_LEVEL)
        decode_msg.Battery_Percent = cal_battery_percentage(decode_msg.Battery_Voltage)
        #Sequence_Number
        decode_msg.Sequence_Number = int(out_data[12])
    else:
        decode_flg = 0

    return len(rcv_buff), decode_msg, decode_flg

def handle_gsm_cell_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    # Initialize decode message struct
    decode_msg = GsmCellMsg()

    # Check length of out_data to make sure enough fields of this messages
    if len(out_data) == len(constant.INFO_GSM_CELL):
        decode_flg = 1
        # Time_stamp
        utc_ts = out_data[0]
        yy = utc_ts[0:2]
        mm = utc_ts[2:4]
        dd = utc_ts[4:6]
        hh = utc_ts[6:8]
        tmp_hh = int(hh) + 7  # convert utc time to VN time
        hh = str(tmp_hh)
        mmin = utc_ts[8:10]
        ss = utc_ts[10:12]
        decode_msg.Time_Stamp = hh + ':' + mmin + ':' + ss + '+' + dd + '-' + mm + '-' + yy
        # MNC
        decode_msg.MNC = int(out_data[1])
        # Cell_ID
        decode_msg.Cell_ID = int(out_data[2])
        # LAC
        decode_msg.LAC = int(out_data[3])
        # MCC
        decode_msg.MCC = int(out_data[4])
        # Event_ID
        decode_msg.Event_ID = int(out_data[5])
        # Battery_Voltage
        decode_msg.Battery_Voltage = float(out_data[6]) / 1000.0
        # Battery_Percent
        #decode_msg.Battery_Percent = int(decode_msg.Battery_Voltage * 100.0 / constant.MAX_VOLTAGE_LEVEL)
        decode_msg.Battery_Percent = cal_battery_percentage(decode_msg.Battery_Voltage)
        # Sequence_Number
        decode_msg.Sequence_Number = int(out_data[7])
    else:
        decode_flg = 0

    return len(rcv_buff), decode_msg, decode_flg


def handle_lte_cell_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    # Initialize decode message struct
    decode_msg = LtcCellMsg()

    # Check length of out_data to make sure enough fields of this messages
    if len(out_data) == len(constant.INFO_LTE_CELL):
        decode_flg = 1
        # Time_stamp
        utc_ts = out_data[0]
        yy = utc_ts[0:2]
        mm = utc_ts[2:4]
        dd = utc_ts[4:6]
        hh = utc_ts[6:8]
        tmp_hh = int(hh) + 7  # convert utc time to VN time
        hh = str(tmp_hh)
        mmin = utc_ts[8:10]
        ss = utc_ts[10:12]
        decode_msg.Time_Stamp = hh + ':' + mmin + ':' + ss + '+' + dd + '-' + mm + '-' + yy
        # MNC
        decode_msg.MNC = int(out_data[1])
        # Cell_ID
        decode_msg.Cell_ID = int(out_data[2])
        # LAC
        decode_msg.LAC = int(out_data[3])
        # MCC
        decode_msg.MCC = int(out_data[4])
        # PCID
        decode_msg.PCID = int(out_data[5])
        # Event_ID
        decode_msg.Event_ID = int(out_data[6])
        # Battery_Voltage
        decode_msg.Battery_Voltage = float(out_data[7]) / 1000.0
        # Battery_Percent
        #decode_msg.Battery_Percent = int(decode_msg.Battery_Voltage * 100.0 / constant.MAX_VOLTAGE_LEVEL)
        decode_msg.Battery_Percent = cal_battery_percentage(decode_msg.Battery_Voltage)
        # Sequence_Number
        decode_msg.Sequence_Number = int(out_data[8])
    else:
        decode_flg = 0

    return len(rcv_buff), decode_msg, decode_flg


def handle_heart_beat_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    # Initialize decode message struct
    decode_msg = HeartBeatMsg()

    # Check length of out_data to make sure enough fields of this messages
    if len(out_data) == len(constant.INFO_HEART_BEAT):
        decode_flg = 1
        #Sat No
        decode_msg.Sat_No = int(out_data[0])
        # Time_stamp
        utc_ts = out_data[1]
        yy = utc_ts[0:2]
        mm = utc_ts[2:4]
        dd = utc_ts[4:6]
        hh = utc_ts[6:8]
        tmp_hh = int(hh) + 7  # convert utc time to VN time
        hh = str(tmp_hh)
        mmin = utc_ts[8:10]
        ss = utc_ts[10:12]
        decode_msg.Time_Stamp = hh + ':' + mmin + ':' + ss + '+' + dd + '-' + mm + '-' + yy

        #FixValue1
        decode_msg.Fix_Value1 = out_data[2]
        #FixValue2
        decode_msg.Fix_Value2 = out_data[3]
        #FixValue3
        decode_msg.Fix_Value3 = out_data[4]
        #FixValue4
        decode_msg.Fix_Value4 = out_data[5]
        # Event_ID
        decode_msg.Event_ID = int(out_data[6])
        # Battery_Voltage
        decode_msg.Battery_Voltage = float(out_data[7]) / 1000.0
        # Battery_Percent
        #decode_msg.Battery_Percent = int(decode_msg.Battery_Voltage * 100.0 / constant.MAX_VOLTAGE_LEVEL)
        decode_msg.Battery_Percent = cal_battery_percentage(decode_msg.Battery_Voltage)
        # Sequence_Number
        decode_msg.Sequence_Number = int(out_data[8])
    else:
        decode_flg = 0

    return len(rcv_buff), decode_msg, decode_flg


def handle_data_binding_report(rcv_buff):
    data_buff = rcv_buff
    data_str = data_buff.decode()
    out_data = []
    tmp_str = ''
    for i in data_str:
        if (i != ',') and (i != '+'):
            tmp_str = tmp_str + i
        else:  # delimiter
            out_data.append(tmp_str)
            tmp_str = ''
    # append last tmp_str to out
    out_data.append(tmp_str)

    # Initialize decode message struct
    decode_msg = DeviceBindingMsg()
    decode_flg = 0   #Not process Device_Binding message

    return len(rcv_buff), decode_msg, decode_flg