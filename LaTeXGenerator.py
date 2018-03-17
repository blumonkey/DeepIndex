from __future__ import print_function
from __future__ import division
from faker import Faker
import random
import math
from jinja2 import Environment, FileSystemLoader
import tempfile
import os
import json
import argparse

INT_COL = 'int'
FLOAT_COL = 'float'
SSTR_COL = 'sstr'
DSTR_COL = 'dstr'
IDX_COL = 'idx'

TAB_SC = 'tabsc'
TAB_DC = 'tabdc'

IMG_SC = 'imgsc'
IMG_DC = 'imgdc'

BibTex_Entries = ["Abril07",  "Cohen07",  "JCohen96",  "Kosiur01",  "Harel79",  "Editor00",  "Editor00a",  "Spector90",  "Douglass98",  "Knuth97",  "Knuth98",  "GM05",  "Smith10",  "VanGundy07",  "VanGundy08",  "VanGundy09",  "Andler79",  "Harel78",  "anisi03",  "Clarkson85",  "Thornburg01",  "Ablamowicz07",  "Poker06",  "Obama08",  "JoeScientist001",  "Novak03",  "Lee05",  "Rous08",  "384253",  "Werneck:2000:FMC:351827.384253",  "1555162",  "Conti:2009:DDS:1555009.1555162",  "Li:2008:PUC:1358628.1358946",  "Hollis:1999:VBD:519964",  "Goossens:1999:LWC:553897",  "897367",  "Buss:1987:VTB:897367",  "Czerwinski:2008:1358628",  "Clarkson:1985:ACP:911891",  "1984:1040142",  "2004:ITE:1009386.1010128",  "Mullender:1993:DS(:302430",  "Petrie:1986:NAD:899644",  "Petrie:1986:NAD:12345",  "book-minimal",  "KA:2001",  "KAGM:2001",  "Kong:2002:IEC:887006.887010",  "Kong:2003:IEC:887006.887011",  "Kong:2004:IEC:123456.887010",  "Kong:2005:IEC:887006.887010",  "Kong:2006:IEC:887006.887010",  "SaeediMEJ10",  "SaeediJETC10",  "Kirschmer:2010:AEI:1958016.1958018",  "Hoare:1972:CIN:1243380.1243382",  "Lee:1978:TQA:800025.1198348",  "Dijkstra:1979:GSC:1241515.1241518",  "Wenzel:1992:TVA:146022.146089",  "Mumford:1987:MES:54905.54911",  "McCracken:1990:SSC:575315",  "MR781537",  "MR781536",  "Adya-01",  "Akyildiz-01",  "Akyildiz-02",  "Bahl-02",  "CROSSBOW",  "Culler-01",  "Harvard-01",  "Natarajan-01",  "Tzamaloukas-01",  "Zhou-06",  "ko94",  "gerndt:89",  "6:1:1",  "7:1:137",  "7:2:183",  "knuth:texbook",  "6:3:380",  "lamport:latex",  "7:3:359",  "test",  "reid:scribe",  "Zhou:2010:MMS:1721695.1721705",  "TUGInstmem",  "CTANacmart",  "bowman:reasoning",  "braams:babel",  "clark:pct",  "herlihy:methodology",  "salas:calculus",  "Fear05",  "Amsthm15"]


def get_single_columns():
    return [INT_COL, FLOAT_COL]


class LaTeXGenerator(object):
    """Class for generating Random LaTeX for ACM and IEEE formats"""

    def __init__(self, locale='en_US'):
        self.fake = Faker(locale)
        self.path_to_images = '../../images/'
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

        self.env = Environment(
            loader = FileSystemLoader('templates')
        )

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
            return caption, self.figure_dc % (img_url, caption)
        return caption, self.figure_sc % (img_url, caption)

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
        return caption, self.table_starter % (table_type, caption, label, column_format, headers) + ' \n ' \
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
        return "\\section{%s}" % title.upper(), title.upper()

    def subsection_tag(self, title):
        return "\\subsection{%s}" % title, title

    # TODO: Add citations, footnotes and table/figure references.
    def format_paragraph(self, paragraph):
        return paragraph

    def random_select(self, paths):
        bin_size = 1 / paths
        prob = random.random()
        return math.floor(prob / bin_size)

    def make_body(self, metadata):
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

                if 'sections' not in metadata.keys():
                    metadata['sections'] = list()
                latex, title = self.section_tag(self.generate_section())
                metadata['sections'].append(title)

                document.append(latex)
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
                        if 'tables' not in metadata.keys():
                            metadata['tables'] = list()
                        caption, latex = self.generate_table()
                        metadata['tables'].append(caption)

                        document.append(latex)
                        table_count += 1
                elif random_choice == 2:
                    if figure_count == MAX_FIGURE_COUNT:
                        continue
                    else:
                        if 'figures' not in metadata.keys():
                            metadata['figures'] = list()
                        caption, latex = self.generate_figure()
                        metadata['figures'].append(caption)

                        document.append(latex)
                        figure_count += 1
                else:
                    if subsection_count == MAX_SUBSECTION_COUNT:
                        if paragraph_count == MAX_PARAGRAPH_COUNT:
                            stack.pop()
                        continue
                    else:
                        stack.append(SUBSEC)
                        latex, title = self.subsection_tag(self.generate_section())

                        metadata['sections'].append(title)

                        document.append(latex)
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
                        caption, latex = self.generate_table()
                        if 'tables' not in metadata.keys():
                            metadata['tables'] = list()

                        metadata['tables'].append(caption)

                        document.append(latex)
                        table_count += 1
                elif random_choice == 2:
                    if figure_count == MAX_FIGURE_COUNT:
                        continue
                    else:
                        caption, latex = self.generate_figure()
                        if 'figures' not in metadata.keys():
                            metadata['figures'] = list()

                        metadata['figures'].append(caption)

                        document.append(latex)
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
                        latex, title = self.subsection_tag(self.generate_section())
                        metadata['sections'].append(title)

                        document.append(latex)
                        document.append(self.format_paragraph(self.generate_paragraph()))
                        subsection_count += 1
                        paragraph_count = 1
                else:
                    stack.pop()
                    stack.pop()

        document = '\n'.join(document)

        directory = metadata['format']
        with tempfile.NamedTemporaryFile(dir='./templates/'+directory, delete=False, suffix='.tex') as tmpfile:
            doc_name = os.path.basename(tmpfile.name)
            tmpfile.write(document)

        metadata['body'] = doc_name[:-4]
        return doc_name

    def generate_acm_info(self):
        isbn = self.fake.isbn10()
        place = self.fake.city()
        yearacm = self.fake.year()
        date = self.fake.month_name() + ' ' + yearacm
        place_full = place + ', ' + self.fake.state() + ' USA'
        yearcr = self.fake.year()

        return "\\acmDOI{10.475/123_4}\n" + \
                "\\acmISBN{%s}\n" % isbn + \
                "\\acmConference[%s'97]{ACM %s conference}{%s}{%s}\n" %(place, place, date, place_full) + \
                "\\acmYear{%s}\n" % yearacm + \
                "\\copyrightyear{%s}\n" % yearcr + \
                "\\acmPrice{15.00}\n" + \
                "\\acmSubmissionID{123-A12-B3}\n"

    def generate_title_block(self, metadata):
        title = self.generate_title()
        subtitle = self.generate_title(num_words=2)
        titlenote = self.fake.sentence(nb_words=10, variable_nb_words=True)
        hasSubtitle = ( random.random() >= 0.5 )

        metadata['title'] = title
        if hasSubtitle:
            metadata['subtitle'] = subtitle
            return "\\title{%s}\n" % title + \
                "\\titlenote{%s}\n" % titlenote + \
                "\\subtitle{%s}\n" % subtitle

        return "\\title{%s}\n" % title + \
               "\\titlenote{%s}\n" % titlenote

    def generate_authors_block(self, metadata):
        main_authors = random.randint(1, 3)
        sub_authors = random.randint(0, 3)
        professors = random.randint(0, 2)

        metadata['authors'] = list()

        _authors = list()

        for _ in range(main_authors):
            author_name = self.fake.name()
            has_author_note = ( random.random() >= 0.5 )
            if has_author_note:
                author_note = "\\authornote{%s}\n" % self.fake.sentence(nb_words=6, variable_nb_words=True)
            else:
                author_note='\n'
            institute = random.choice(['University of ', 'Institute of ']) + self.fake.city()
            street_address = self.fake.address().split('\n')[0]
            city = self.fake.city()
            state = self.fake.state()
            postcode = self.fake.zipcode_plus4()
            email = self.fake.email()

            _authors.append(
                "\\author{%s}\n" % author_name +
                author_note +
                "\\affiliation{\n" +
                "      \institution{%s}\n" % institute +
                "      \streetaddress{%s}\n" % street_address +
                "      \city{%s}\n" % city +
                "      \state{%s}\n" % state +
                "      \postcode{%s}\n" % postcode +
                "    }\n" + \
                "\email{%s}\n\n" % email
            )

            curr_author = {
                'name': author_name,
                'institute': institute,
                'city': city,
                'state': state,
                'email': email
            }

            metadata['authors'].append(curr_author)

        for _ in range(sub_authors):
            author_name = self.fake.name()
            institute = random.choice(['University of ', 'Institute of ']) + self.fake.city()
            street_address = self.fake.address().split('\n')[0]
            email = self.fake.email()

            _authors.append(
                "\\author{%s}\n" % author_name +
                "\\affiliation{\n" +
                "      \institution{%s}\n" % institute +
                "      \streetaddress{%s}\n" % street_address +
                "    }\n" + \
                "\email{%s}\n\n" % email
            )

            curr_author = {
                'name': author_name,
                'institute': institute,
                'email': email
            }

            metadata['authors'].append(curr_author)

        for _ in range(professors):
            author_name = self.fake.name()
            institute = random.choice(['University of ', 'Institute of ']) + self.fake.city()
            email = self.fake.email()

            _authors.append(
                "\\author{%s}\n" % author_name +
                "\\affiliation{\n" +
                "      \institution{%s}\n" % institute +
                "    }\n" + \
                "\email{%s}\n\n" % email
            )

            curr_author = {
                'name': author_name,
                'institute': institute,
                'email': email
            }

            metadata['authors'].append(curr_author)

        return '\n'.join(_authors)

    def generate_short_authors_command(self, metadata):
        names = metadata['authors'][0]['name'].split()
        lastname = names[1]
        return '\\renewcommand{\shortauthors}{%s et al.}' % lastname

    def generate_abstract(self):
        return self.generate_paragraph(num_sentences=15)

    def generate_keywords(self):
        num_keywords = random.randint(3, 7)
        keywords = list()
        for _ in range(num_keywords):
            keywords.append(self.fake.word())

        return ', '.join(keywords)

    def generate_no_cites(self):
        num_cites = random.randint(10, 30)
        cites = random.sample(BibTex_Entries, num_cites)
        cite_tex = ['\\nocite{%s}' % key for key in cites]
        return '\n'.join(cite_tex)


    def generate_acm_authorsdraft(self):
        metadata = dict()
        metadata['format'] = 'acm-authorsdraft'
        template = self.env.get_template('acm-authorsdraft/main.tmp.tex')

        acm_info = self.generate_acm_info()
        title = self.generate_title_block(metadata)
        authors = self.generate_authors_block(metadata)
        short_authors = self.generate_short_authors_command(metadata)
        abstract = self.generate_abstract()
        keywords = self.generate_keywords()
        body = self.make_body(metadata)
        no_cites = self.generate_no_cites()

        filled_tex = template.render(ACM_INFO=acm_info, TITLE=title, AUTHORS=authors, SHORT_AUTHORS_COMMAND=short_authors, ABSTRACT=abstract, KEY_WORDS=keywords, BODY=body, NO_CITES=no_cites)
        print(filled_tex)

        fname = "./templates/acm-authorsdraft/main-%s.tex" % metadata['body']
        with open(fname, "w") as tex_file:
            tex_file.write(filled_tex)

        file_name = './templates/acm-authorsdraft/meta-%s.json' % metadata['body']
        with open(file_name, 'w') as fp:
            json.dump(metadata, fp, sort_keys=True, indent=4, separators=(',', ': '))

        return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Latex files by format')
    parser.add_argument('format', help='Format of the Journal/Conference')
    parser.add_argument('num', type=int, help='Number of files to generate')

    args = parser.parse_args()
    print(args)
    if args.format != 'acm-authorsdraft':
        print('Not implemented')
    numDocs = args.num

    myObj = LaTeXGenerator()
    for _ in range(numDocs):
        print('Generating...'+str(_))
        metadata = myObj.generate_acm_authorsdraft()
        # print(metadata)

