# Bingo card class that will read information from a csv file
from db import dbcsv
import pandas
# Turn off warning for setting value
pandas.options.mode.chained_assignment = None 
# Options
from options import options

class card(object):
	def __init__(self, name):
		self.name    = name
		self.csvpath = "card_"+name+".csv"
		self.db      = dbcsv(self.csvpath)

	def initialise_card(self):
		# Delete existing file
		self.db.rebuild()
		# Add header to file
		self.db.write(["complete","entry"])

	def add_entry(self, entry):
		# Just simple adding
		self.db.write([False, entry])

	def get_entries(self):
		df = pandas.read_csv(self.csvpath)
		entries = []
		for i in df.index:
			entries.append((i, df['complete'][i], df['entry'][i]))
		return entries

	def complete_entry(self, box):
		df = pandas.read_csv(self.csvpath)
		df['complete'][box] = True
		df.to_csv(self.csvpath)

	def generate_random_card(self, inc_tank, inc_dps, inc_support):
		# Function to generate a random card
		self.initialise_card()
		# Get the options
		opts    = options("all_options.csv")
		df_opt  = opts.get_dataframe()
		df_opt  = df_opt.drop(df_opt[(df_opt.tank != inc_tank) & (df_opt.dps != inc_dps) & (df_opt.support != inc_support)].index)
		print ("Available :",len(df_opt),"options")
		# Get 25
		results = df_opt.sample(25)
		for i in results.index:
			self.add_entry(df_opt.loc[i]['entry'])

	def print_card(self):
		entries = self.get_entries()
		# Card layout
		card_str = ""
		for e in entries:
			if e[0]%5 == 0:
				card_str += "\n----------------\n|"
			if e[1] == True:
				card_str += "XX".ljust(2)+"|"
			else:
				card_str += str(e[0]).ljust(2)+"|"
		card_str += "\n----------------\n"
		print (card_str)
		return card_str

	def print_tasks(self):
		entries = self.get_entries()
		# Info layout
		info_str = ""
		for e in entries:
			info_str += str(e[0]).ljust(3)+": "+e[2]+"\n"
		print (info_str)
		return info_str







