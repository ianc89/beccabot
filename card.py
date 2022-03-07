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

	def complete_entry(self, box, complete):
		try:
			box = int(box)
		except Exception as e:
			print (e)
			return (False,[])
		try:
			df = pandas.read_csv(self.csvpath)
		except Exception as e:
			print (e)
			return (False,[])

		# Check status before updating
		completed_prior = self.check()
		# Update dataframe
		if compelete:
			df['complete'][box] = True
		else:
			df['complete'][box] = False
		df.to_csv(self.csvpath, index=False)
		# Check status after updating
		completed_after = self.check()
		# Identify any new completions
		completed_new = list(set(completed_after) - set(completed_prior))
		# Note if BINGO
		if len(completed_after) == 10:
			completed_new.append("-!-BINGO-!-")
		return (True,completed_new)

	def generate_random_card(self, inc_tank, inc_dps, inc_support):
		# Function to generate a random card
		self.initialise_card()
		# Get the options
		opts    = options("all_options.csv")
		df_opt  = opts.get_dataframe()
		# Messy selection to ensure we only consider options which are true in argument and true in table
		# Then drop those options which are all False
		df_opt  = df_opt.drop(df_opt[False == ((df_opt.tank & inc_tank) | (df_opt.dps & inc_dps) | (df_opt.support & inc_support))].index)
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

	def check(self):
		# Possible rows/cols
		possible = {"Row 1":[0,1,2,3,4],
					"Row 2":[5,6,7,8,9],
					"Row 3":[10,11,12,13,14],
					"Row 4":[15,16,17,18,19],
					"Row 5":[20,21,22,23,24],
					"Col 1":[0,5,10,15,20],
					"Col 2":[1,6,11,16,21],
					"Col 3":[2,7,12,17,22],
					"Col 4":[3,8,13,18,23],
					"Col 5":[4,9,14,19,24],
					"Dia 1":[0,6,12,18,24],
					"Dia 2":[4,8,12,16,20],
					}
		# What is completed
		completed = []
		# Read results
		df = pandas.read_csv(self.csvpath)
		# Loop though allowed completions
		for p in possible:
			complete = True
			for box in possible[p]:
				if df['complete'][box] == True:
					complete &= True
				else:
					complete &= False
			# Record the key if we are all true
			if complete:
				completed.append(p)
		return completed
					







