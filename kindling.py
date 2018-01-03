from threading import Thread
import socket

class Kindling (Thread):
	"""The python variant of 
	$ socat -u4v UDP4-LISTEN:7073,bind=0.0.0.0,reuseaddr,fork UDP4-DATAGRAM:$nextip:$lport
	albeit single threaded...
	"""
	def __init__(self, target, lsock):
		"""
		@param target (ip::String, port::int)
		"""
		self.insock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_address = ('0.0.0.0', lsock)
		self.insock.bind(self.server_address)

		self.outsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.point_to_address(target)


	def point_to_address(self, target):
		self.target_addr = target
		
	def stop(self):
		self.running = False

	def run(self):
		self.running = True
		while self.running:
				data, address = self.insock.recvfrom(1024)
				if data:
						if not self.target_addr:
								print('no target address given, skipping msg')
								next
						sent = self.outsock.sendto(data, self.target_addr)
						if Fire.is_fire_msg(data):
								Fire.display_fire()


class Fire:
	""" The object that draws the fire if needed """
	def is_fire_msg(data):
		return data and data == "fire"
	
	def display_fire():
		print('fire')
		
