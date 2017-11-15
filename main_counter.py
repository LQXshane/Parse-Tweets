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

# from  2016-08-04 to  2016-10-23
# Total 26,246,374 tweets

if __name__ == '__main__':
    jsdir = sys.argv[1]
    utc = pytz.utc
    MAXDATE = datetime(2010,01,01,tzinfo=utc)
    MINDATE = datetime(2017,12,30,tzinfo=utc)
    COUNT = 0
    INVALIDS = 0
    files = [ f for f in os.listdir(jsdir) if os.path.isfile(os.path.join(jsdir,f))]
    j = 0; print "%d of json files in total"%(len(files))
    for f in files:
        j += 1
        if j % 10000 == 0: print j
        if f.endswith(".json"):
            with open(os.path.join(jsdir,f)) as js:
                data = json.load(js)
            js.close()
            COUNT += len(data)
            for i in range(len(data)):
                try:
                    dt = parser.parse(data[i]['created_at'])
                except:
                    # print "No valid datetime on record"
                    INVALIDS += 1
                    continue
                if 'created_at' in data[i]:
                    if dt > MAXDATE:
                        MAXDATE = dt
                    if dt < MINDATE:
                        MINDATE = dt

    print "From ",MINDATE.date(), "to ", MAXDATE.date()
    print "Total %d tweets"%(COUNT)
    print "%d tweets does not have datetime"%(INVALIDS)
