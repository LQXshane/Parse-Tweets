# -*- coding: utf-8 -*-
__author__ = "qiuxuanlin"


# Sampled time period is 7/18/2016 - 11/7/2016.
# " Here are just over 55.44 million election ids. It is tweets that mention: Trump, Hillary and Clinton. "

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

def main(jsdir, file_out, cout, tout):
    def helper(exist, users, data, i, K, candidate):
        username = data[i]['user']['screen_name']
        dt = parser.parse(data[i]['created_at'])
        if username not in exist:
            users[username].append([data[i]["id"], dt, username,data[i]["text"]])
        else:
            return
        if len(users[username]) >= K:
            exist.add(username)
            k = K
            while k > 0:
                line = [candidate]
                line.extend(users[username].pop())
                writer.writerow(line) # output
                k -= 1
            del users[username]
        return

    clinton_users = collections.defaultdict(list) # username: list of user_tweets
    trump_users = collections.defaultdict(list)
    utc = pytz.utc
    START, END =  datetime(2016,07,18,tzinfo=utc), datetime(2016,11,07,tzinfo=utc)
    MAXDATE = datetime(2010,01,01,tzinfo=utc)
    MINDATE = datetime(2017,12,30,tzinfo=utc)
    clinton_exist = set() # set of users who already exist in the final result
    trump_exist = set()

    # print datetime.now()

    with open(file_out, 'w') as TWEETS:
        writer = csv.writer(TWEETS, delimiter=',')
        writer.writerow(["Candidate", "ID", "Time", "Username(who tweeted at least 3 times)","Tweet"])
        files = [ f for f in os.listdir(jsdir) if os.path.isfile(os.path.join(jsdir,f))]

        CCOUNT = TCOUNT = NULL = 0 # number of tweets mentioning clinton and trump respectively
        j = 0
        # print "%d of json files in total, "%(len(files))
        TOTAL = 0
        for f in files:
            j += 1
            # if j % 10000 == 0: print j
            if f.endswith(".json"):
                with open(os.path.join(jsdir,f)) as js:
                    data = json.load(js)
                js.close()
            TOTAL += len(data)
            for i in range(len(data)):
                # within valid time frame
                try:
                    dt = parser.parse(data[i]['created_at'])
                    if dt > MAXDATE:
                        MAXDATE = dt
                    if dt < MINDATE:
                        MINDATE = dt
                except: continue
                if 'created_at' in data[i] and START <= dt <= END:
                    username = data[i]['user']['screen_name']
                    tweet = data[i]["text"].lower()
                    if "trump" in tweet:
                        TCOUNT += 1
                        helper(trump_exist, trump_users, data, i,  1, "Trump")
                    elif "hillary" in tweet or "clinton" in tweet:
                        CCOUNT += 1
                        helper(clinton_exist, clinton_users, data, i, 1, "Clinton")
                    else:
                        NULL += 1
    TWEETS.close()
    # unique clinton and trump users
    with open(cout, 'w') as out:
        writer = csv.writer(out)
        writer.writerows([x] for x in clinton_exist)


    with open(tout, 'w') as out:
        writer = csv.writer(out)
        writer.writerows([x] for x in trump_exist)
        writer.writerow(["Json files, ", len(files)])
        writer.writerow(["Tweets, ", TOTAL])
        writer.writerow(["Trump, ", TCOUNT])
        writer.writerow(["Clinton, ", CCOUNT])
        writer.writerow(["Neither, ", NULL])
        writer.writerow([MAXDATE])
        writer.writerow([MINDATE])


    # print datetime.now()
    # print "%d mentioning Trump in total"%(TCOUNT)
    # print "%d mentioning Clinton in total"%(CCOUNT)
    # print "%d mentioning neither candidates"%(NULL)


if __name__ == '__main__':
    destdir = sys.argv[1]
    jsdir = sys.argv[2]
    file_out = os.path.join(destdir,"valid_tweets.csv")
    clinton = os.path.join(destdir,"clinton_users.csv")
    trump = os.path.join(destdir,"trump_users.csv")
    main(jsdir, file_out, clinton, trump)
