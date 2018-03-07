from faker import Faker
import random

INT_COL 	= 'int'
FLOAT_COL 	= 'float'
SSTR_COL 	= 'sstr'
DSTR_COL 	= 'dstr'
IDX_COL		= 'idx'

TAB_SC 		= 'tabsc'
TAB_DC 		= 'tabdc'

class LaTeXGenerator(object):
	"""Class for generating Random LaTeX for ACM and IEEE formats"""

	def __init__(self, locale='en_US'):
		self.fake = Faker(locale)
		self.path_to_images = 'images/'
		self.NUM_IMAGES = 999
		self.table_starter = """\\begin{%s}
  \\caption{%s}
  \\label{tab:%s}
  \\begin{tabular}{%s}
  \\toprule
  %s\\\\
  \\midrule"""
		self.table_ender = """\\bottomrule
  \\end{tabular}
  \\end{%s}"""
  		self.table_counter = 0

	def generate_paragraph(self, num_sentences=20, variable_len=True):
		return self.fake.paragraph(num_sentences, variable_len)

	def generate_name(self):
		return self.fake.name()

	def generate_address(self):
		return self.fake.address()

	def generate_username(self, name=None):
		if name is None:
			name = self.generate_name()
		return ''.join(name.tolower().split()) + str(random.randint(0, 99))

	def generate_email(self):
		return self.fake.email()

	def generate_title(self, num_words=12, variable_len=True):
		return self.fake.sentence(num_words, variable_len)

	def generate_heading(self, num_words=2, variable_len=True):
		return self.fake.sentence(num_words, variable_len).toupper()

	def generate_caption(self, num_words=15, variable_len=True):
		return self.fake.sentence(num_words, variable_len)

	def generate_image(self, single_column=True):
		if not single_column:
			raise NotImplemented('No wide images available for 2-column format.')
		return path_to_images + str(random.randint(0, self.NUM_IMAGES)) +'.png'

	def make_bold(self, token):
		return '\\textbf{%s}' % token

	def generate_rows(self, num_rows, column_types, enable_make_bold=True):
		if IDX_COL in column_types:
			row_count = 1

		all_rows = ''

		for _ in range(num_rows):
			current_row = list() 
			make_bold = enable_make_bold and (random.uniform(0, 1) > 0.7)
			for i in column_types:
				if i is IDX_COL:
					current_row.append(row_count)
					row_count += 1
				elif i is INT_COL:
					current_row.append(random.randint(0, 1000))
				elif i is FLOAT_COL:
					current_row.append(self.fake.pyfloat(left_digits=random.randint(1, 2), right_digits=2))
				elif i is SSTR_COL:
					current_row.append(self.fake.sentence(nb_words=2, variable_nb_words=True))
				elif i is DSTR_COL:
					current_row.append(self.fake.sentence(nb_words=5, variable_nb_words=True))
			
			if make_bold:
				current_row = [self.make_bold(str(token)) for token in current_row]
			else:
				current_row = [str(token) for token in current_row]

			all_rows = all_rows + ' & '.join(current_row) + ' \\\\ \n'

		return all_rows

	def __generate_table(self, table_type, num_rows, column_types):
		num_columns = len(column_types)
		caption = self.fake.sentence(nb_words=10, variable_nb_words=True)
		label = 'tab' + str(self.table_counter)
		self.table_counter += 1
		column_format = 'c' * num_columns
		headers = list()
		for _ in range(num_columns):
			headers.append(' '.join(self.fake.words(nb=random.randint(1, 2))))
		headers = ' & '.join(headers)
		return self.table_starter % (table_type, caption, label, column_format, headers) + ' \n ' \
														+ self.generate_rows(num_rows, column_types) + '\n'\
														+ self.table_ender % (table_type)
	
	def generate_table_sc(self, num_rows, column_types):
		return self.__generate_table('table', num_rows, column_types)


	def generate_table_dc(self, num_rows, column_types):
		return self.__generate_table('table*', num_rows, column_types)

	def get_single_columns(self):
		return [INT_COL, FLOAT_COL]

	def get_double_columns(self):
		return [INT_COL, FLOAT_COL]

	def generate_table(self, table_type=None):
		if not table_type:
			table_type = random.choice([TAB_SC, TAB_DC])
		num_rows = random.randint(4, 10)
		num_strings = random.randint(0, 1)
		
		if table_type is TAB_SC:
			num_columns = random.randint(2, 5)
			column_types = [random.choice(self.get_single_columns()) for _ in range( num_columns - 1 - num_strings)]
			
			if random.random() >=0.5:
				column_types = [ IDX_COL ] + column_types
			else:
				column_types.append(random.choice(self.get_single_columns()))
			
			column_types = column_types + [ SSTR_COL ] * num_strings
			
			copy = column_types[1:]
			random.shuffle(copy)
			column_types[1:] = copy

			return self.generate_table_sc(num_rows, column_types)

		else:
			num_columns = random.randint(4, 6)
			column_types = [random.choice(self.get_double_columns()) for _ in range( num_columns - 1 - num_strings)]
			if random.random() >=0.5:
				column_types = [ IDX_COL ] + column_types
			else:
				column_types.append(random.choice(self.get_double_columns()))

			column_types = column_types + [ DSTR_COL ] * num_strings

			copy = column_types[1:]
			random.shuffle(copy)
			column_types[1:] = copy
			return self.generate_table_dc(num_rows, column_types)

if __name__ == '__main__':
	myObj = LaTeXGenerator()
	print myObj.generate_table()