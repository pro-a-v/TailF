#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket
import struct
import json


class ZabbixTrapSender:
    def __init__(self):
        self.Host = 'Zabbix_server_ip'
        self.Port = 10051
        self.Hostname = 'Hostname_in_zabbix'
        self.HEADER = '''ZBXD\1%s%s'''

    def __init__(self, zabbix_host='Zabbix_server_ip', zabbix_port= 10051, zabbix_item_hostname='Hostname_in_zabbix'):
        self.Host = zabbix_host
        self.Port = zabbix_port
        self.Hostname = zabbix_item_hostname
        self.HEADER = 'ZBXD\1'

    def sendData(self, key, value):
        DATA = '''{ "request":"sender data", "data":[{"host":"''' + self.Hostname + '''","key":"''' + key + '''","value":"''' + str(
            value) + '''"}]} '''
        # print(DATA)
        data_length = len(DATA)
        data_header = struct.pack('i', data_length) + b'\0\0\0\0'
        # print(type(data_header),data_header)
        data_to_send = self.HEADER.encode() + data_header + DATA.encode()
        # print(type(data_to_send),data_to_send)
        # here really should come some exception handling
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.Host, self.Port))
        sock.send(data_to_send)
        # read its response, the first five bytes are the header again
        response_header = sock.recv(5)
        # print(type(response_header),response_header)
        if not response_header == b'ZBXD\1':
            raise ValueError('Got invalid response')
        # read the data header to get the length of the response
        response_data_header = sock.recv(8)
        response_data_header = response_data_header[:4]  # we are only interested in the first four bytes
        # print(type(response_data_header),response_data_header)
        response_len = struct.unpack('i', response_data_header)[0]
        # read the whole rest of the response now that we know the length
        response_raw = sock.recv(response_len)
        # print(type(response_raw),response_raw)
        sock.close()
        response = json.loads(response_raw.decode())
        return DATA + " -----   " + str(response)





