from tcp_mqtt_gateway import constant
import struct


def decode_report_header(rcv_buf):
    decode_length = 0
    # decode report header
    rcv_buffer = rcv_buf
    if len(rcv_buffer) >= constant.HEAD_LENGTH:
        head_header = rcv_buffer[0:constant.HEAD_LENGTH]
        rcv_buffer = rcv_buffer[(constant.HEAD_LENGTH + 1):]
        decode_length = decode_length + constant.HEAD_LENGTH + 1

    if len(rcv_buffer) >= constant.MODE_LENGTH:
        mode_header = rcv_buffer[0:constant.MODE_LENGTH]
        rcv_buffer = rcv_buffer[(constant.MODE_LENGTH + 1):]
        decode_length = decode_length + constant.MODE_LENGTH + 1

    if len(rcv_buffer) >= constant.IMEI_LENGTH:
        imei_header = rcv_buffer[:constant.IMEI_LENGTH]
        rcv_buffer = rcv_buffer[(constant.IMEI_LENGTH + 1):]
        decode_length = decode_length + constant.IMEI_LENGTH + 1

    if len(rcv_buffer) >= constant.DATA_TYPE_LENGTH:
        data_type_header = rcv_buffer[:constant.DATA_TYPE_LENGTH]
        if data_type_header[2:3] == b";":
            rcv_buffer = rcv_buffer[constant.DATA_TYPE_LENGTH:]
            data_type_header = data_type_header[0:2]
            decode_length = decode_length + constant.DATA_TYPE_LENGTH
        else:
            rcv_buffer = rcv_buffer[constant.DATA_TYPE_LENGTH + 1:]
            decode_length = decode_length + constant.DATA_TYPE_LENGTH + 1

    return head_header, mode_header, imei_header, data_type_header, rcv_buffer, decode_length
