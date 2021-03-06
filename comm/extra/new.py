#!/usr/bin/env python
# -*- coding:utf-8 -*-
import bluetooth
import threading

name = "BluetoothChat"
uuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]

bluetooth.advertise_service(server_sock, name, uuid)

print "Waiting for connection on RFCOMM channel %d" % port


class echoThread(threading.Thread):
    def __init__ (self, sock, client_info):
        threading.Thread.__init__(self)
        self.sock = sock
        self.client_info = client_info

    def run(self):
        try:
            while True:
                data = self.sock.recv(1024)
                if len(data) == 0: break
                print self.client_info, ": received [%s]" % data
                self.sock.send(data)
                print self.client_info, ": sent [%s]" % data
        except IOError:
            pass
        self.sock.close()
        print self.client_info, ": disconnected"

while True:
    client_sock, client_info = server_sock.accept()
    print client_info, ": connection accepted"
    echo = echoThread(client_sock, client_info)
    echo.setDaemon(True)
    echo.start()

server_sock.close()
print "all done"
