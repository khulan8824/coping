
import datetime
import os
import sys
from subprocess import check_output, PIPE, Popen
import subprocess
import shlex

class Node:
    address = "" # address of the gateway
    isRoot = False
    neighbors = {}
    
    def __init__(self, address, isParent, neighbors):
        self.address = address
        self.isParent = isParent
        for n in neighbors:
            temp = self.initialiazeNeighbor(address)
            neighbors[n] = temp
    
    
    ''' Try to assign the neighbors appropriate rtt values by pinging'''
    def initializeNeighbor(self, address):
        cmd='ping -w 5 -c 3 -q '+address
        command = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
        stdout, stderr = command.communicate()
        stdout = str(stdout)
        if '/' not in stdout:
            return 0
        else:
            return float(stdout.split('/')[-3])        