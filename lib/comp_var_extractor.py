import fileinput
import sys
from spiral import ronin
import re
import enchant

###############
# specify the addtional dictionary file as the first command-line argument
addtional_dict_file = sys.argv[1]
eng_dict = enchant.DictWithPWL("en_US", addtional_dict_file)

###############
# definitions of common regular expressions
digit_pattern = re.compile(r'\d+')

##############################################
# main
is_header = True
for line in fileinput.input(files='-'):
    line = line.strip()
    if is_header:
        print(line, 'words', sep='\t')
        is_header = False
        continue
    items = line.split()
    name = items[1]
    if not name.isascii():
        continue

    tokens = ronin.split(name)
    if len(tokens) == 1:
        continue

    valid_cnt = 0
    for tk in tokens:
        if digit_pattern.match(tk):
            continue
        if eng_dict.check(tk) and len(tk) >= 2:
            valid_cnt += 1

    if valid_cnt < 2:
        continue
        
    words = ','.join(tokens)
    print(line, words, sep='\t')
