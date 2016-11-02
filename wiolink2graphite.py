#!/usr/bin/python
import time
import socket
import sys
#import os
#import re

import codecs
import requests
requests.packages.urllib3.disable_warnings()
import base64
#import struct
import json
#import hashlib

timestamp = int(time.time())

# Get the connection variables from the external file
from parameters import username, password, STDOUT, DOLOG, BASE_URL, ACCESS_TOKEN, CARBON_SERVER, CARBON_PORT

LOGFILE     = str(timestamp)+'.log'
LOGFILE     = '_log.log'

class Logger():
    def __init__(self, logfile, stdout):
        self.logfile  = LOGFILE
        self.stdout = STDOUT

    def writer(self, msg):
        if LOGFILE and LOGFILE != '' and DOLOG == True:
            with codecs.open(self.logfile, 'a', encoding = 'utf-8') as f:
                try:
                  f.write(msg.strip()+'\r\n')  # \r\n for notepad
                except:
                  f.write(str(msg))
        if self.stdout == 'True' or STDOUT == True:
            try:
                #print msg
                pass
            except:
                print msg.encode('ascii', 'ignore') + ' # < non-ASCII chars detected! >'

def fetcher(url):
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(username + ':' + password),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.get(url, headers=headers, verify=False)
    msg = 'Status code: %s' % str(r.status_code)
    logger.writer(msg)
    msg = str(r.text)
    logger.writer(msg)
    if '"celsius_degree": 0.0' in msg:
        r.status_code = '404'
    if '"fahrenheit_degree": 32.0' in msg:
        r.status_code = '404'
    if str(r.status_code) == '200':
        return r.text
    else:
        return 'failed'

def get_fromsource(sensor):
    url = base_url+sensor+'?access_token='+ACCESS_TOKEN
    msg =  '\r\nFetching devices from %s ' % url
    logger.writer(msg)
    data = fetcher(url)
    return data

def get_sensordata(value):
  logger.writer('**** WIO ')
  # Reach out to WIO_Link Server and get all sensor information in a dictionary
  raw = get_fromsource(value)
  value = value.split('/')[1]
  if raw == 'failed':
      #print value,' no info'
      pass
  else:
      data = json.loads(raw)
      #print data

      #print value
      if value == 'temperature':
          value = 'celsius_degree'
      if value == 'temperature_f':
          value = 'fahrenheit_degree'
      #print value,': ',data[value]
      dataset[value] = data[value]

def createMsg():
  message = []

  for value in dataset:
    if len(value) == 0:
        field = 'none'
    else:
        field = value
    messageReturn = [ 'wio.%s %s %d' % (field, dataset.get(value), timestamp), ]
    message += messageReturn

  return message

def sendMsg(message):
  sock = socket.socket()
  sock.connect((CARBON_SERVER, CARBON_PORT))
  sock.sendall(message)
  sock.close()

if __name__ == "__main__":
  base_url = BASE_URL
  logger = Logger(LOGFILE, STDOUT)

  global dataset
  dataset = {}

  get_sensordata('GroveAirqualityA0/quality')
  get_sensordata('GroveDigitalLightI2C0/lux')
  get_sensordata('GroveTempHumD0/humidity')
  get_sensordata('GroveTempHumD0/temperature')
  get_sensordata('GroveTempHumD0/temperature_f')

  #createMsg()
  sendMessage = createMsg()
  message = '\n'.join(sendMessage) + '\n'
  sendMsg(message)
  #print message
  sys.exit(0)
