from matchstick import MatchStick
from kindling import Kindling

import threading as threading 

kindling_port=(7073)
multicast_group=('244.1.1.1', 8269)




class FireLink:
	"""Be a part in the ring of fire consisting of MatchStick (Multicast
	announce and management tool) and Kindling (the actual proxy)."""

	def __init__(self):

		self.proxy = Kindling(None, kindling_port)
		self.mc = MatchStick(multicast_group, self.proxy.point_to_address)

		self.mc_threat = threading.Thread(target=self.mc)
		self.proxy_threat = threading.Thread(target=proxy)

		self.proxy_threat.start()
		self.mc_threat.start()
		self.mc_threat.join()
		


