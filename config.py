class Conf:
	def __init__(self):
		self.conf = dict()
		self.conf['datadir'] = '/var/lib/prefextract/'
		self.conf['hostname'] = 'localhost'
		self.conf['port'] = 8967
		self.conf['hypernymDepth'] = 2
		self.conf['useDepthWeightedRating'] = 1
		self.conf['hypernymDepthPowerQ'] = 1.0
		self.conf['depthWeightingDepthPowerQ'] = 1.0
		self.conf['averageFactorAddition'] = 0.0

config = Conf()
