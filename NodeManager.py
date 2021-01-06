import random
import datetime
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex
import threading
import os
import sys
from math import *
import operator
import statistics 
from statistics import stdev 
import numpy as np
from sklearn.linear_model import LinearRegression


from twisted.python import log
from twisted.internet import reactor, protocol
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

import MessageServerProtocol as server
import MessageClientProtocol as client
import Node as n


class NodeManager:
    
    gatewayTable = {}
    selected_gateway = ""
    node = None
    gateways = []
    period = 120
    sendCount = 0
    receiveCount = 0
    cnt = 0
    isProxy = False
    
    def __init__(self, node, period, gateways):
        self.node = node
        self.period = period
        self.gateways = gateways
        
    
    def process(self, datas, sender):
        rtt = self.node.initializeNeighbor(sender)
        print("RTT",rtt)
        m1 = []
        m2 = []
        print(datas)
        for data in datas:
            address, latency  = data.decode('utf-8').split(',')
            address = address.encode('utf-8')
            self.gatewayTable[address] = float(latency)
            m1.append(float(latency))
            m2.append(self.pingGateway(address))
        
        print("Gateways", self.gatewayTable)
        self.selected_gateway = min(self.gatewayTable.iteritems(), key=operator.itemgetter(1))[0] 
        print("Selected", self.selected_gateway)
        self.sendNeighbors(datas)
        sim = float(self.cosine_similarity(m1,m2))
        print("Similarity", sim)
    
    def senseGateways(self):
        result = ""
        for gw in self.gateways:
            lat = self.pingGateway(gw)
            if lat >0:
                if result != "":
                    result +="#"
                result += gw+','+str(lat)
        self.sendNeighbors(result)
    
    def sendNeighbors(self, result):
        for n in self.node.neighbors:
            print("Sending to:", n)
            self.sendCount += 1
            if n == self.node.address:
                continue
            f = protocol.ClientFactory()
            f.protocol = client.MessageClientProtocol        
            f.protocol.addr = n
            f.protocol.text = result
            reactor.connectTCP(n, 5555, f)
            if not reactor.running:
                reactor.run()
                
    def mainLoop(self):            
        if self.cnt <20:
            reactor.callLater(self.period, self.mainLoop)
            if self.node.isParent:
                self.senseGateways()
                
            with open('messages_'+self.node.address,'a') as f:
                f.write("{0},{1},{2}\n".format(str(self.cnt) ,str(self.sendCount), str(self.receiveCount)))                
            self.sendCount = 0
            self.receiveCount = 0
            print("============ Round",self.cnt,"================")
            self.cnt +=1            
        else:
            print("END")
            sys.exit(0)
        
        
    def pingGateway(self,address):
        status = True
        cmd = ""
        if self.isProxy:
            cmd='''curl -x '''+self.selected_gateway+''':3128 -U david.pinilla:"|Jn 5DJ\\7inbNniK|m@^ja&>C" -m 180 -w %{time_total},%{http_code} http://ovh.net/files/1Mb.dat -o /dev/null -s'''
        else:
            cmd='''curl http://'''+self.selected_gateway+''':8080/1Mb.dat -m 180 -w %{time_total},%{http_code} -o /dev/null -s'''
            
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        lat, code = stdout.decode("utf-8").split(',')        
        #Checking if gateway is accessible
        if int(code) != 200:
            return ""
        else:
            return float(lat)
        
    def cosine_similarity(self, x,y):
        numerator = sum(a*b for a,b in zip(x,y))
        denominator = self.square_rooted(x)*self.square_rooted(y)
        if denominator >0:
            return round(numerator/float(denominator),3)
        else:
            return 0
        
    def download(self):
        if self.cnt <400:
            reactor.callLater(60, self.download)
            self.downloadContent()
        
    def downloadContent(self):
        ##########Downloading with power of 2 choices################
        status = True
        cmd = ""
        if self.isProxy:
            cmd='''curl -x '''+self.selected_gateway+''':3128 -U david.pinilla:"|Jn 5DJ\\7inbNniK|m@^ja&>C" -m 180 -w %{time_total},%{http_code} http://ovh.net/files/10Mb.dat -o /dev/null -s'''
        else:
            cmd='''curl http://'''+self.selected_gateway+''':8080/10Mb.dat -m 180 -w %{time_total},%{http_code} -o /dev/null -s'''
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        lat, code = stdout.decode("utf-8").split(',')
        if int(code) != 200:
            return
        else:
            with open('download_'+self.myAddress,'a') as f:
                f.write("{0},{1}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(lat.encode('ascii', 'ignore'))))
        
