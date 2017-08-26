import sys, time, json, os.path, datetime

from water_pump import Pump
from multiprocessing import Process

pin = int(sys.argv[1])


def get_data(name):
    content = 'null'
    if os.path.isfile('data/'+name):
        with open('data/' + name, 'r') as f:
            content = f.read()
            f.close()
    return json.loads(content)


def set_data(name, data):
    with open('data/' + name, 'w+') as f:
        f.write(json.dumps(data))
        f.close()


def work(pin):
    print("started subprocess")
    pump = Pump(pin=pin)
    while True:
        log = get_data('irrigated_log')
        need = get_data('need')
        unfinished = get_data('unfinished')
        if unfinished is not None:
            already_watered = unfinished['duration']
            need = need - already_watered
            print("Unfinished irrigation detected, {} seconds remaining".format(need))
        elif log is not None and len(log)>0:
            now = time.time()
            already_watered = 0
            for record in log:
                timestamp = record["timestamp"]
                if now - timestamp > 3600 * 24 * 3:
                    continue
                already_watered += record["duration"]
            if already_watered < need / 2:
                need = need - already_watered
                print("Time to water again, for {} seconds".format(need))
            else:
                continue
        else:
            log = []
        
        if need > 0:
            if unfinished is None:
                unfinished = {"timestamp": time.time(), "duration": 0}
            pump.on()
            start = time.time()
            starting_duration = unfinished['duration']
            while time.time() - start < need:
                time.sleep(1)
                unfinished['duration'] = starting_duration + time.time() - start
                set_data('unfinished', unfinished)
            log.append({"timestamp": unfinished["timestamp"], "duration": unfinished["duration"]})
            set_data('irrigated_log', log)
            set_data('unfinished', None)
            pump.off()
        time.sleep(300)

w = None
while True:
    if w is None or not w.is_alive():
        w = Process(target=work, args=(pin,))
        w.start()
    time.sleep(1)
