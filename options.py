from db import dbcsv
import pandas
import os

# Class to hold options for bingo card
class options(object):
	def __init__(self, csvfile):
		self.csvpath   = csvfile
		self.dbcsv     = dbcsv(csvfile)
		self.dataframe = None
		self.check_if_exists()

	def check_if_exists(self):
		if not os.path.exists(self.csvpath):
			self.add_entry("tank","dps","support","entry")

	def add_entry(self, is_tank, is_dps, is_support, entry):
		self.dbcsv.write([is_tank, is_dps, is_support, entry])

	def get_dataframe(self):
		return pandas.read_csv(self.csvpath)
	
	def print_all(self):
		df = self.get_dataframe()
		return df.to_string()
