#!/usr/bin/env python3
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import os
import sys
import json
import time
import requests

with open('config.json') as json_file:
    conf = json.load(json_file)

STREAMERS = conf['flussonic_servers']
USER = conf['login']
PASSWORD = conf['password']
REMOTE_URL_PATH = '/flussonic/api/sessions'


### Reading from streamers ###
class FlussonicCollector(object):
    def collect(self):
        sessions_stats = []
        c = GaugeMetricFamily('flussonic_stream_sessions', 'Flussonic sessions for stream.', labels=['stream_name', 'stream_type', 'hostname'])
        for flussonic_host in STREAMERS:
            #print(flussonic_host);
            REMOTE_URL = "http://"  + flussonic_host + REMOTE_URL_PATH
            try:
                response = requests.get(REMOTE_URL, timeout=(1, 5), auth=(USER, PASSWORD)).json()
            except requests.RequestException:
                print("Connect to server error: " + flussonic_host)
                continue
            #print(response.json())
            data = response
            ### Filling stats array ###
            num = 0
            for item in data["sessions"]:
                is_added = 0
                ch_name = data["sessions"][num]["name"]
                ch_type = data["sessions"][num]["type"]

                for o_num in range (0, len(sessions_stats)):
                    if sessions_stats[o_num][0] == ch_name and sessions_stats[o_num][1] == ch_type and sessions_stats[o_num][2] == flussonic_host:
                        sessions_stats[o_num][3] += 1
                        #print(sessions_stats[o_num][0] + " " + sessions_stats[o_num][1])
                        is_added = 1

                if is_added == 0:
                    sessions_stats.append([ch_name, ch_type, flussonic_host, 1])
                num += 1

        ### Writing to file ###
        s_num = 0
        for s_num in range(0 ,len(sessions_stats)):
            c.add_metric([sessions_stats[s_num][0], sessions_stats[s_num][1], sessions_stats[s_num][2]], sessions_stats[s_num][3])
        yield c
    ### end for ###


if __name__ == "__main__":
    try:
        REGISTRY.register(FlussonicCollector())
        start_http_server(9228)
        while True: 
            time.sleep(1)
            #print("DateTime " + time.strftime("%c"))
    except KeyboardInterrupt:
        print(" Interrupted")
        exit(0)

