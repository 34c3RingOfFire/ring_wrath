from sys import platform
import socket
import struct
if (platform.startswith("freebsd")!= True):
    from netifaces import interfaces, ifaddresses, AF_INET
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
        ip = subprocess.call(['./getip.sh'])
        print(ip)
        return ip
      # print '%s: %s' % (ifaceName, ', '.join(addresses))


def choose_external_ip():
	return choice(external_ip_list())



class Multicaster:
   def __init__(self, ip, port):
       addr = ('', port)
       self.mc_group = (ip, port)
       self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       self.sock.bind(addr)

       group = socket.inet_aton(ip)
       mreq =  struct.pack('4sL', group, socket.INADDR_ANY)
       self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
       self.me_list = external_ip_list()
       self.my_ip = choose_external_ip()
       self.ip_list = [ self.my_ip ]

   def update_ip_list(self, newlist):
       self.ip_list = newlist

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
        return self.send_out_msg(Multicaster.marshall(self.ip_list))

   def announce_yourself(self):
        return self.send_out_msg("ANNOUNCE\n" + self.my_ip)

   def marshall(ip_list):
        str = ""
        for ip in ip_list:
            str += ip + "\n"
        return str

   def parse_ip_list(data):
        return data.decode().splitlines() 

   def run(self):
      self.run = True
      self.announce_yourself()
      try: 
         while self.run:
            data, address = self.sock.recvfrom(1024)
            if address in self.me_list: 
                   continue
            incoming_ip_list = Multicaster.parse_ip_list(data)
            if not self.my_ip in incoming_ip_list: 
                    incoming_ip_list.append(self.my_ip)
                    self.update_ip_list(incoming_ip_list)
                    emit_my_ip_list();
      finally:
          self.sock.close()
      

   def stop(self):
       self.run = False
