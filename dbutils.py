# Utility class
# Author : @anweshpatel
# Created : 03.16.2019
# Project : Unified Sensor Network

class dbutils(object):
	def __init__(self, metadata):
		self.metadata = metadata
	
	@staticmethod
	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
