import OpenOPC, sched, time, json, subprocess, os
from config import config
from datetime import datetime

items = {}
max_name_size = 1
max_item_size = 1
for i in config['items']:
    if len(i['item_id']) > max_item_size: max_item_size = len(i['item_id'])
    if len(i['key']) > max_name_size: max_name_size = len(i['key'])
    items[i['item_id']] = {
        'item_id': i['item_id'],
        'key': i['key'],
        'host': i['host']
    }
max_name_size += 1
max_item_size += 1

cfgo = config.get('output')

if cfgo.get('to_zabbix') and cfgo.get('zabbix_server'):
    send_to_zabbix = True
    # port = cfgo.get('zabbix_server_port') if cfgo.get('zabbix_server_port') else 10051
    # zbx = ZabbixSender(cfgo.get('zabbix_server'), port)

s = sched.scheduler(time.time, time.sleep)

def human_time(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    #return "{:>02}:{:>02}:{:>05.2f}".format(h, m, s)
    return "{:>02}:{:>02}:{:>02}".format(h, m, int(s))

def epoch_time(time_str):
    dt = datetime.strptime(time_str)
    return (dt - datetime(1970,1,1)).total_seconds()

def log(strout):
    if cfgo.get('verbose'): 
        if cfgo.get('to_console'):
            print strout
        if cfgo.get('to_file'):
            fname = 'opcmonitor'+datetime.now().strftime('%Y%m%d')+'.log'
            f = open (fname, 'a')
            f.write(str(strout))
            f.close()

def wrapper(sc):
    try:
        query_items()
    except Exception as ex:
        log(ex)
    sc.enter(config['scan_interval'], 1, wrapper, (sc,))

def query_items():
    log('## querying items @%s' % datetime.now())
    opc = OpenOPC.open_client()
    opc.connect(config['server'])
    tags = [item['item_id'] for item in config['items'] if True]
    values = opc.read(tags)
    opc.close()

    for i in range(len(values)): 
        (item_id, val, qual, time) = values[i] 
        
        old = items.get(item_id)
        delay_loops = 0
        if old and old.get('value'):
            if old['value'] == val:
                delay_loops = old['delay'] + config['scan_interval']
        items[item_id].update({
            'value': val, 
            'quality': qual,
            'time': time,
            'delay': delay_loops
        })
    output = json.dumps({'items': items})
    if not cfgo.get('use_json'):
        output = "%-*s %-*s %-15s %-8s %-12s %-15s\n" % (max_name_size,'key',max_item_size,'item_id','value','quality','delay (s)','timestamp')
        for item in items:
            output += "%-*s %-*s %-15s %-8s %-12s %-15s\n" % (max_name_size,items[item]['key'],max_item_size,items[item]['item_id'],items[item]['value'],items[item]['quality'],human_time(items[item]['delay']),items[item]['time'])            
    if cfgo.get('to_file'):
        f = open (config['file_output'], 'w')
        f.write(output)
        f.close()
    if cfgo.get('to_console'):
        print output
    if send_to_zabbix:
        output = 'zabbix >> %s\n' % datetime.now()
        data = ''
        for item in items:
            data += "%s %s %5s\n" % (items[item].get('host'), items[item].get('key'), items[item].get('value')) 
            if cfgo.get('zabbix_quality_suffix'):
                data += "%s %s %5s\n" % (items[item].get('host'), items[item].get('key')+cfgo['zabbix_quality_suffix'], items[item].get('quality')) 
            if cfgo.get('zabbix_timestamp_suffix'):
                data += "%s %s %5s\n" % (items[item].get('host'), items[item].get('key')+cfgo['zabbix_timestamp_suffix'], items[item].get('time')) 
            if cfgo.get('zabbix_delay_suffix'):
                data += "%s %s %5s\n" % (items[item].get('host'), items[item].get('key')+cfgo['zabbix_delay_suffix'], items[item].get('delay')) 
        output += data
        f = open ('opcmonitor_zabbix.tmp', 'w')
        f.write(data)
        f.close()
        proc = subprocess.Popen('zabbix_sender -z %s -p %d -i %s' % (cfgo['zabbix_server'],cfgo['zabbix_port'],'opcmonitor_zabbix.tmp'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output += '\nzabbix <<\n'
        output += proc.stdout.read()
        os.remove('opcmonitor_zabbix.tmp')
        log(output)
    #sc.enter(config['scan_interval'], 1, query_items, (sc,))

s.enter(config['scan_interval'], 1, wrapper, (s,))
s.run()

