import csv
import os
import re


pattern = re.compile(r'(main\-.*)\-(\d+).jpg')

with open('annotations.csv', 'rb') as fread:
	csv_reader = csv.reader(fread, delimiter=',', quotechar='"')
	isHeader = True
	with open('new_annotations.csv', 'wb') as fwrite:
		csv_writer = csv.writer(fwrite, delimiter=',', quotechar='"')
		for row in csv_reader:
			print row[0]
			if isHeader:
				csv_writer.writerow(row)
				isHeader = False
			if os.path.isfile('files/'+row[0]):
				csv_writer.writerow(row)
			else:
				fname = row[0]
				if pattern.match(fname):
					match = int(pattern.match(fname).group(2))
					print match
					new_fname = pattern.match(fname).group(1) + '-' + ('%02d' % match) + '.jpg'
					print new_fname
					if os.path.isfile('files/'+new_fname):
						csv_writer.writerow([new_fname] + row[1:])
					else:
						print 'Fail case'
				
