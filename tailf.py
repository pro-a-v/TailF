import time
from datetime import datetime
import threading
from zabbix_trap_sender import ZabbixTrapSender
import copy
from queue import Queue


class Counter:
    data = dict()
    current_time = datetime.now()

    def set(self,code):
        dif = datetime.now() - self.current_time
        if int(dif.total_seconds()) < 60:
            if not code in self.data:
                self.data[code] = 1
            else:
                self.data[code] += 1
        else:
            q.put(self.data.copy())
            self.clear_all()

    def clear_all(self):
        self.current_time = datetime.now()
        self.data.clear()



def Sender():
    while True:
        item = q.get()
        trap = ZabbixTrapSender(zabbix_host='Zabbix_server_ip', zabbix_port= 10051, zabbix_item_hostname='Hostname_in_zabbix')
        for key, val in item.items():
            print(key, '-' , val)
            trap.sendData( 'HTTP_status_'+str(key), str(val))
        q.task_done()


def tailf(filename):
    f = open(filename, 'r')
    f.seek(0,2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line



cnt = Counter()
q = Queue()

if __name__ == '__main__':
    filename = '/var/log/nginx/ccom.hyber.im-access.log'
    t = threading.Thread(target=Sender)
    t.daemon = True
    t.start()
    for i in tailf(filename):
        cnt.set(i.split( )[8])