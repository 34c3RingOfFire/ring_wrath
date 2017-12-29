from netifaces import interfaces, ifaddresses, AF_INET
from random import choice

# derived from https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib


def flatten(l):
   return [ i for sublist in l for i in sublist ]

def external_ip_list():
         addresses = [i['addr'] for ifaceName in interfaces() 
	                 for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
         return list(filter( lambda ip:  not ip.startswith('127.'), addresses) )
   
      # print '%s: %s' % (ifaceName, ', '.join(addresses))


def choose_external_ip():
	return choice(external_ip_list())
