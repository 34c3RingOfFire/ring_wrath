from sys import platform
import socket
import struct
if (platform.startswith("freebsd")!= True):
    from netifaces import interfaces, ifaddresses, AF_INET
else:
    import os
from random import choice

# derived from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib


def flatten(l):
   return [ i for sublist in l for i in sublist ]

def external_ip_list():
    if (platform.startswith("freebsd") != True):
         addresses = [i['addr'] for ifaceName in interfaces() 
	                 for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
         return list(filter( lambda ip:  not ip.startswith('127.'), addresses) )
    else:
        ip = os.system('sh ./getip.sh')
        print(ip)
        return list([str(ip)])
      # print '%s: %s' % (ifaceName, ', '.join(addresses))


def choose_external_ip():
	return choice(external_ip_list())



class MatchStick:
   def __init__(self, mc_group, assign_target):
       listen_addr = ('', mc_group[1])
       self.mc_group = mc_group
       self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       self.sock.bind(listen_addr)

       self.target_assignment = assign_target

       group = socket.inet_aton(self.mc_group[0])
       mreq =  struct.pack('4sL', group, socket.INADDR_ANY)
       if (platform.startswith('freebsd') != True):
           self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
       self.me_list = external_ip_list()
       self.my_ip = choose_external_ip()
       self.ip_list = [ self.my_ip ]
       print('Multicaster initialised')
       print('I am ' + self.my_ip )
       

   def update_ip_list(self, newlist):
       print('Update to:\n' + str(newlist))
       self.ip_list = newlist
       self.assign_target(my_peer)

   def my_peer(self):
       try:
          pos = 1+self.ip_list.index(self.my_ip)
       except:
          print("ERROR: could not find myself in ip list")
          sys.exit(1)
       if pos >= len(self.ip_list):
           return self.ip_list[0]
       else:
           return self.ip_list[pos]
	       


   def send_out_msg(self, msg):
       out_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       out_sock.settimeout(0.2)
       ttl = struct.pack('b', 2)
       out_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
       try:
           sent = out_sock.sendto(msg.encode(), self.mc_group)
       finally:
           out_sock.close()
       return sent
       

   def emit_my_ip_list(self):
        result = self.send_out_msg(Multicaster.marshall(self.ip_list))
        print('emitted ip list: ' + str(result))
        return result

   def announce_yourself(self):
        result = self.send_out_msg("ANNOUNCE\n" + self.my_ip)
        print('announced myself: ' + str(result))
        return result

   def marshall(ip_list):
        str = ""
        for ip in ip_list:
            str += ip + "\n"
        return str

   def parse_ip_list(data):
        return data.decode().splitlines() 

   def run(self):
      print('Multicaster run!')
      self.run = True
      self.announce_yourself()
      try: 
         while self.run:
            data, address = self.sock.recvfrom(1024)
            print('Multicaster received multicast from ' + str(address))
            if address in self.me_list: 
                   print('Multicaster has been talking to himself.')
                   continue
            incoming_ip_list = Multicaster.parse_ip_list(data)
            print('Incoming list:\n' + str(incoming_ip_list))
            if not self.my_ip in incoming_ip_list: 
                    print('Multicaster: "They do not know me! Append me!"')
                    incoming_ip_list.append(self.my_ip)
                    self.update_ip_list(incoming_ip_list)
                    self.emit_my_ip_list();
      finally:
          self.sock.close()
      

   def stop(self):
       self.run = False
