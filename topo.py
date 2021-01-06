from mininet.topo import Topo
from mininet.net import  Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, UserSwitch  
import random
import time

class MultiSwitchTopo(Topo):
    "multiple switch connected to n hostst"
    def build(self):
        addresses1 = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4','10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9','10.0.0.10']
      
       
        gwAddresses = ['10.0.1.1', '10.0.1.2', '10.0.1.3', '10.0.1.4', '10.0.1.5', '10.0.1.6', '10.0.1.7', '10.0.1.8', '10.0.1.9', '10.0.1.10']
        
        switch = self.addSwitch('s13', cls=OVSKernelSwitch)

        switch1 = self.addSwitch('s1', cls=OVSKernelSwitch)
        switch2 = self.addSwitch('s2', cls=OVSKernelSwitch)
        switch3 = self.addSwitch('s3', cls=OVSKernelSwitch)
        switch4 = self.addSwitch('s4', cls=OVSKernelSwitch)
        switch5 = self.addSwitch('s5', cls=OVSKernelSwitch)

       
        switch7 = self.addSwitch('s7', cls=OVSKernelSwitch)
        switch8 = self.addSwitch('s8', cls=OVSKernelSwitch)
        switch9 = self.addSwitch('s9', cls=OVSKernelSwitch)
        switch10 = self.addSwitch('s10', cls=OVSKernelSwitch)
        switch11 = self.addSwitch('s11', cls=OVSKernelSwitch)
        
        for h in range(len(addresses1)):
            host = self.addHost('h%s' % (h+1), ip=addresses1[h])
            self.addLink(host, switch1)

        for h in range(len(addresses2)):
            host = self.addHost('h%s' % (len(addresses1)+h+1), ip=addresses2[h])
            self.addLink(host, switch2)

        for h in range(len(addresses3)):
            host = self.addHost('h%s' % (len(addresses1)*2+h+1), ip=addresses3[h])
            self.addLink(host, switch3)
            
        for h in range(len(addresses4)):
            host = self.addHost('h%s' % (len(addresses1)*3+h+1), ip=addresses4[h])
            self.addLink(host, switch4)
            
        for h in range(len(addresses5)):
            host = self.addHost('h%s' % (len(addresses1)*4+h+1), ip=addresses5[h])
            self.addLink(host, switch5)
            
        self.addLink(switch7, switch1)
        self.addLink(switch8, switch2)
        self.addLink(switch9, switch3)
        self.addLink(switch10, switch4)
        self.addLink(switch11, switch5)
        
        self.addLink(switch, switch7)
        self.addLink(switch, switch8)        
        self.addLink(switch, switch9)
        self.addLink(switch, switch10)
        self.addLink(switch, switch11)


        for g in range(len(gwAddresses)):
            gw = self.addHost('g%s' % (g+1), ip=gwAddresses[g])
            self.addLink(gw, switch)            
            

def topo():
    topo = MultiSwitchTopo()
    net = Mininet(topo)
    net.start()
    print("Dumping host connection")
    popens = {}
        
   
    for h in net.switches:

        if h.name=='s1':
            for n in range(10):
                randDelay = random.randint(1,3)
                h.cmdPrint("tc qdisc add dev s1-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's2':
            for n in range(10):
                randDelay = random.randint(1,3)
                h.cmdPrint("tc qdisc add dev s2-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's3':
            for n in range(10):
                randDelay = random.randint(1,5)
                h.cmdPrint("tc qdisc add dev s3-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's4':
            for n in range(10):
                randDelay = random.randint(3,6)
                h.cmdPrint("tc qdisc add dev s4-eth%d root netem delay %dms"%(n+1, randDelay))

        elif h.name == 's5':
            for n in range(10):
                randDelay = random.randint(2,6)
                h.cmdPrint("tc qdisc add dev s5-eth%d root netem delay %dms"%(n+1, randDelay))
                
        elif h.name == 's7':
            h.cmdPrint("tc qdisc add dev s7-eth1 root netem delay 5ms")   
        elif h.name == 's8':
            h.cmdPrint("tc qdisc add dev s8-eth1 root netem delay 5ms")   
        elif h.name == 's9':
            h.cmdPrint("tc qdisc add dev s9-eth1 root netem delay 5ms")   
        elif h.name == 's10':
            h.cmdPrint("tc qdisc add dev s10-eth1 root netem delay 5ms")   
        elif h.name == 's11':
            h.cmdPrint("tc qdisc add dev s11-eth1 root netem delay 5ms")
            

    for h in net.hosts:
        if h.name =='g1':
            h.cmdPrint("tc qdisc add dev g1-eth0 root netem delay 2ms")
        elif h.name =='g2':
            h.cmdPrint("tc qdisc add dev g2-eth0 root netem delay 3ms")
        elif h.name =='g3':
            h.cmdPrint("tc qdisc add dev g3-eth0 root netem delay 4ms")
        elif h.name =='g4':
            h.cmdPrint("tc qdisc add dev g4-eth0 root netem delay 2ms")            
        elif h.name =='g5':
            h.cmdPrint("tc qdisc add dev g5-eth0 root netem delay 1ms")            
        elif h.name =='g7':
            h.cmdPrint("tc qdisc add dev g7-eth0 root netem delay 4ms")
        elif h.name =='g8':
            h.cmdPrint("tc qdisc add dev g8-eth0 root netem delay 1ms")
        elif h.name =='g10':
            h.cmdPrint("tc qdisc add dev g10-eth0 root netem delay 3ms")

    CLI(net)

if __name__ == "__main__":
    setLogLevel('info')
    topo()