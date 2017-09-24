# -*- coding: utf-8 -*-
__author__ = "qiuxuanlin"


# Sampled time period is 7/18/2016 - 11/7/2016.
import json
from dateutil import parser
from datetime import datetime
import csv
import os
import pytz

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

def main(destdir, file_in, output):
    cusers = {}
    with open(file_in, 'r') as uniqueUsers:
        reader = csv.reader(uniqueUsers)
        for line in reader:
            if len(line) == 2 and line[0]:
                cusers[line[1]] = 0
    uniqueUsers.close()

    print "Total # of twitter users: ", len(cusers)

    utc = pytz.utc
    start, end =  datetime(2016,07,18,tzinfo=utc), datetime(2016,11,07,tzinfo=utc)


    file_out = os.path.join(destdir,output)
    with open(file_out, 'w') as twts:
        # read all json files in dir
        writer = csv.writer(twts, delimiter=',')
        files = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f))]
        for f in files:
            if f.endswith(".json"):
                with open(f) as js:
                    data = json.load(js)
                js.close()
                for i in range(len(data)):
                    # within valid time frame
                    dt = parser.parse(data[i]['created_at'])
                    line = []
                    if 'created_at' in data[i] and start <= dt <= end:
                        # from uniqueUsers users
                        username = data[i]['user']['screen_name']
                        if username in cusers:
                            if cusers[username] >= 4: continue
                            cusers[username] += 1
                            # print twts.tell()
                            line.extend([data[i]["id"], dt, username, cusers[username], data[i]["text"]])
                            writer.writerow(line) # write to file
    twts.close()

if __name__ == '__main__':
    destdir = sys.argv[1]
    file_in = os.path.join(destdir, sys.argv[2])
    output = "user_tweets" + sys.argv[3] + ".csv"

    main(destdir, file_in, output)
