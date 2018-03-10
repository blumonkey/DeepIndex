from __future__ import print_function
from __future__ import division
from faker import Faker
import random
import math

INT_COL = 'int'
FLOAT_COL = 'float'
SSTR_COL = 'sstr'
DSTR_COL = 'dstr'
IDX_COL = 'idx'

TAB_SC = 'tabsc'
TAB_DC = 'tabdc'

IMG_SC = 'imgsc'
IMG_DC = 'imgdc'


def get_single_columns():
    return [INT_COL, FLOAT_COL]


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

        self.figure_sc = """\\begin{figure}
\\includegraphics[height=2in, width=3in]{%s}
\\caption{%s}
\\end{figure}"""

        self.figure_dc = """\\begin{figure*}
\\includegraphics[height=2in, width=3in]{%s}
\\caption{%s}
\\end{figure*}"""

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

    def generate_section(self, num_words=2, variable_len=True):
        return self.fake.sentence(num_words, variable_len)

    def generate_caption(self, num_words=15, variable_len=True):
        return self.fake.sentence(num_words, variable_len)

    def get_image_path(self):
        return self.path_to_images + str(random.randint(0, self.NUM_IMAGES)) + '.png'

    def __generate_image(self, image_type):
        caption = self.fake.sentence(nb_words=10, variable_nb_words=True)
        img_url = self.get_image_path()
        if image_type is IMG_DC:
            return self.figure_dc % (img_url, caption)
        return self.figure_sc % (img_url, caption)

    def generate_figure(self, image_type=None):
        if not image_type:
            image_type = random.choice([IMG_SC, IMG_DC])
        return self.__generate_image(image_type)

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
               + self.generate_rows(num_rows, column_types) + '\n' \
               + self.table_ender % (table_type)

    def generate_table_sc(self, num_rows, column_types):
        return self.__generate_table('table', num_rows, column_types)

    def generate_table_dc(self, num_rows, column_types):
        return self.__generate_table('table*', num_rows, column_types)

    def get_columns(self):
        return [INT_COL, FLOAT_COL]

    def generate_table(self, table_type=None):
        if not table_type:
            table_type = random.choice([TAB_SC, TAB_DC])
        num_rows = random.randint(4, 10)
        num_strings = random.randint(0, 1)

        if table_type is TAB_SC:
            num_columns = random.randint(2, 5)
            column_types = [random.choice(get_single_columns()) for _ in range(num_columns - 1 - num_strings)]

            if random.random() >= 0.5:
                column_types = [IDX_COL] + column_types
            else:
                column_types.append(random.choice(get_single_columns()))

            column_types = column_types + [SSTR_COL] * num_strings

            copy = column_types[1:]
            random.shuffle(copy)
            column_types[1:] = copy

            return self.generate_table_sc(num_rows, column_types)

        else:
            num_columns = random.randint(4, 6)
            column_types = [random.choice(self.get_columns()) for _ in range(num_columns - 1 - num_strings)]
            if random.random() >= 0.5:
                column_types = [IDX_COL] + column_types
            else:
                column_types.append(random.choice(self.get_columns()))

            column_types = column_types + [DSTR_COL] * num_strings

            copy = column_types[1:]
            random.shuffle(copy)
            column_types[1:] = copy
            return self.generate_table_dc(num_rows, column_types)

    def section_tag(self, title):
        return "\\section{%s}" % title.upper()

    def subsection_tag(self, title):
        return "\\subsection{%s}" % title

    # TODO: Add citations, footnotes and table/figure references.
    def format_paragraph(self, paragraph):
        return paragraph

    def random_select(self, paths):
        bin_size = 1 / paths
        prob = random.random()
        return math.floor(prob / bin_size)

    def make_body(self):
        stack = []
        document = []

        SEC = 'sec'
        SUBSEC = 'subsec'

        section_count = 0
        subsection_count = 0

        paragraph_count = 0
        table_count = 0
        figure_count = 0

        MAX_SECTION_COUNT = 5
        MAX_SUBSECTION_COUNT = 4
        MAX_PARAGRAPH_COUNT = 3
        MAX_TABLE_COUNT = 3
        MAX_FIGURE_COUNT = 5

        while True:
            if not stack:
                if section_count == MAX_SECTION_COUNT:
                    break
                stack.append(SEC)
                document.append(self.section_tag(self.generate_section()))
                document.append(self.format_paragraph(self.generate_paragraph()))
                section_count += 1
                subsection_count = 0
                paragraph_count = 1
            elif stack[-1] is SEC:
                random_choice = self.random_select(4)
                if random_choice == 0:
                    if paragraph_count == MAX_PARAGRAPH_COUNT:
                        if subsection_count == MAX_SUBSECTION_COUNT:
                            stack.pop()
                        continue
                    else:
                        document.append(self.format_paragraph(self.generate_paragraph()))
                        paragraph_count += 1
                elif random_choice == 1:
                    if table_count == MAX_TABLE_COUNT:
                        continue
                    else:
                        document.append(self.generate_table())
                        table_count += 1
                elif random_choice == 2:
                    if figure_count == MAX_FIGURE_COUNT:
                        continue
                    else:
                        document.append(self.generate_figure())
                        figure_count += 1
                else:
                    if subsection_count == MAX_SUBSECTION_COUNT:
                        if paragraph_count == MAX_PARAGRAPH_COUNT:
                            stack.pop()
                        continue
                    else:
                        stack.append(SUBSEC)
                        document.append(self.subsection_tag(self.generate_section()))
                        document.append(self.format_paragraph(self.generate_paragraph()))
                        subsection_count += 1
                        paragraph_count = 1
            elif stack[-1] is SUBSEC:
                random_choice = self.random_select(5)
                if random_choice == 0:
                    if paragraph_count == MAX_PARAGRAPH_COUNT:
                        if subsection_count == MAX_SUBSECTION_COUNT:
                            stack.pop()
                            stack.pop()
                        continue
                    else:
                        document.append(self.format_paragraph(self.generate_paragraph()))
                        paragraph_count += 1
                elif random_choice == 1:
                    if table_count == MAX_TABLE_COUNT:
                        continue
                    else:
                        document.append(self.generate_table())
                        table_count += 1
                elif random_choice == 2:
                    if figure_count == MAX_FIGURE_COUNT:
                        continue
                    else:
                        document.append(self.generate_figure())
                        figure_count += 1
                elif random_choice == 3:
                    if subsection_count == MAX_SUBSECTION_COUNT:
                        if paragraph_count == MAX_PARAGRAPH_COUNT:
                            stack.pop()
                            stack.pop()
                        continue
                    else:
                        stack.pop()
                        stack.append(SUBSEC)
                        document.append(self.subsection_tag(self.generate_section()))
                        document.append(self.format_paragraph(self.generate_paragraph()))
                        subsection_count += 1
                        paragraph_count = 1
                else:
                    stack.pop()
                    stack.pop()

        return document


if __name__ == '__main__':
    myObj = LaTeXGenerator()
    a =  myObj.make_body()
    print('\n'.join(a))
