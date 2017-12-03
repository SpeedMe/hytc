# encoding: utf-8
import os
import logging
import re
import time
import linecache

logging.basicConfig(format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%D %H:%M:%S', filename='/root/tc.log', level=logging.INFO)

server_limit_bandwidth = 20.00
user_bandwidth = '6.5'
device = 'eth1'

temp_file_path = '/root/hytc_temp.txt'
temp_count = 1
command = '/usr/local/iftop/sbin/iftop -i ' + device + ' -N -n -B -P -s 2 -L 2 -o 2s -t > ' + temp_file_path
tc_command = 'tcset --change --device ' + device + ' --direction outgoing --rate ' + user_bandwidth + 'M --network '
clean_tc_command = 'tcdel --device ' + device + ' --all'
reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')


def verify_param(user_ip, user_traffic, total_traffic):
    if 'MB' not in total_traffic:
        return False
    if 'MB' in total_traffic and float(total_traffic.strip('MB')) < server_limit_bandwidth / 8:
        return False
    if 'KB' not in user_traffic and 'MB' not in user_traffic:
        return False
    if 'KB' in user_traffic and float(user_traffic.strip('KB')) < 900:
        return False
    return True


def analyze_traffic(user_ip, user_traffic, total_traffic):
    if verify_param(user_ip, user_traffic, total_traffic):
        final_tc_command = tc_command + user_ip
        logging.info(final_tc_command)
        os.system(final_tc_command)


def get_param(file_path, num):
    linecache.checkcache(file_path)
    user_traffic_line = linecache.getline(file_path, 2 * num - 1 + 3)
    user_ip_line = linecache.getline(file_path, 2 * num - 1 + 4)
    total_tc_line = linecache.getline(file_path, 9)
    user_traffics = user_traffic_line.split('=>')[1]
    user_traffics_arr = ','.join(filter(lambda x: x, user_traffics.split(' '))).split(',')
    user_max_traffic = user_traffics_arr[0]
    user_ip = reip.findall(user_ip_line)[0]
    total_traffic = ','.join(filter(lambda x: x, total_tc_line.split(':')[1].split(' '))).split(',')[0]
    return (user_traffic_line, user_ip, user_max_traffic, total_traffic)


def run_analyze(num):
    user_traffic_line, user_ip, user_max_traffic, total_traffic = get_param(temp_file_path, num)
    logging.info('num:%d, ip:%s, mx:%s, total:%s', num, user_ip, user_max_traffic, total_traffic)
    if ':1123' not in user_traffic_line:
        analyze_traffic(user_ip, user_max_traffic, total_traffic)


if __name__ == "__main__":
    while True:
        logging.info('cycle [%d] times', temp_count)
        if temp_count == 1000:
            logging.info('clean tc..')
            temp_count = 1
            os.system(clean_tc_command)
        os.system(command)
        run_analyze(1)
        run_analyze(2)
        temp_count += 1
        time.sleep(5)
