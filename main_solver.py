# -*- coding: utf-8 -*-
__author__ = "qiuxuanlin"


# Sampled time period is 7/18/2016 - 11/7/2016.
import json
from dateutil import parser
from datetime import datetime
import csv
import os
import pytz
import collections

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

def main(destdir, file_in, output, jsdir):
    cusers = collections.defaultdict(list)
    with open(file_in, 'r') as uniqueUsers:
        reader = csv.reader(uniqueUsers)
        for line in reader:
            if len(line) == 2 and line[0]:
                cusers[line[1]] = []
    uniqueUsers.close()

    print "Total # of twitter users: ", len(cusers)

    utc = pytz.utc
    start, end =  datetime(2016,07,18,tzinfo=utc), datetime(2016,11,07,tzinfo=utc)


    file_out = os.path.join(destdir,output)
    print datetime.now()
    with open(file_out, 'w') as twts:
        # read all json files in dir
        writer = csv.writer(twts, delimiter=',')
        files = [ f for f in os.listdir(jsdir) if os.path.isfile(os.path.join(jsdir,f))]
        j = 0; print "%d of json files in total, "%(len(files))
        for f in files:
            j += 1
            if j % 10000 == 0: print j
            if f.endswith(".json"):
                with open(os.path.join(jsdir,f)) as js:
                    data = json.load(js)
                js.close()
                for i in range(len(data)):
                    # within valid time frame
                    try:
                        dt = parser.parse(data[i]['created_at'])
                    except: continue
                    if 'created_at' in data[i] and start <= dt <= end:
                        # from uniqueUsers users
                        username = data[i]['user']['screen_name']
                        if username in cusers:
                            if len(cusers[username]) >= 3:
                                k = 3
                                while k > 0:
                                    line = cusers[username].pop()
                                    writer.writerow(line) # write to file
                                    k -= 1
                                del cusers[username]
                                continue
                            if cusers[username] and dt == cusers[username][-1][1]:
                                pass
                            else:
                                cusers[username].append([data[i]["id"], dt, username,data[i]["text"]])
                            if twts.tell() >= 100000000: print twts.tell(), i
        # print cusers

    twts.close()
    print datetime.now()

if __name__ == '__main__':
    destdir = sys.argv[1]
    file_in = os.path.join(destdir, sys.argv[2])
    output = "user_tweets" + sys.argv[3] + ".csv"
    jsdir = sys.argv[4]

    main(destdir, file_in, output, jsdir)
