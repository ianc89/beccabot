import csv

# Class to manage csv usage
class dbcsv(object):
	def __init__(self, path):
		self.path = path

	def rebuild(self):
		csvfile = open(self.path, 'w', newline='')
		csvfile.close()

	def write(self, row):
		csvfile = open(self.path, 'a', newline='')
		writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(row)
		csvfile.close()