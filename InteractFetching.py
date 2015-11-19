#!/usr/bin/python27
# -*- coding: utf-8 -*-
import urllib2 , urllib
import json
from numpy import array, argsort
import csv
import datetime
from collections import OrderedDict
import json
import os

# request params
data = """{{
        "username" : "{username}",
        "password" : "{password}",
        "client" : "Apiary"
        }}""".format(username=os.environ["S_USERNAME"], password=os.environ["S_PASSWORD"])

headers = { "Content-Type" : "application/json" }
url = 'https://app-staging.mycontacts.io/api/v2/login'

request = urllib2.Request(url,data,headers=headers)
response = urllib2.urlopen(request).read()

# get authentification token
authToken = json.loads(response)['token']['authToken']

## Fetch data ##

# request params
urlInteractions = 'https://app-staging.mycontacts.io/api/v2/contacts/stats/interactions'        # kss_0vF2aYWpuPKLmd2BHj8LP7
headersInteractions = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'authToken': authToken
}

requestInteract = urllib2.Request( url = urlInteractions, headers=headersInteractions )
responseInteract = urllib2.urlopen(requestInteract).read()


# get interactions & dates
interactions = [i['count'] for i in json.loads(responseInteract)["stats"]["interactions_in_time"]]
dates = [k['key'] for k in json.loads(responseInteract)["stats"]["interactions_in_time"]]

# formate dates
dates = [datetime.datetime.strptime(d, '%d/%m/%Y %H:%M:%S').date() for d in dates]

# get min and max dates
minDate = dates[0]
maxDate = dates[-1]
period = maxDate - minDate
# minimum interval : day
datesList = [minDate + datetime.timedelta(days=x) for x in range(0, period.days)]

# create date dict with this interval
dateArray = []
# assing known dates to their interactions values
for d in datesList:
        if d in dates:
                dateArray.append({"date" : d.strftime('%m/%d/%Y'), "interactions" : interactions[dates.index(d)]})
        else:
                dateArray.append({"date" : d.strftime('%m/%d/%Y'), "interactions" : 0 })

print json.dumps(dateArray)