import fileinput

def extract_available_pairs(record_buf):
    for i in range(len(record_buf)):
        records_i = record_buf[i]
        name_i = records_i[1]
        type_i = records_i[2]
        begin_line_i = int(records_i[3])
        end_line_i = int(records_i[4])
        split_name_i = records_i[5]
        for j in range(i+1, len(record_buf)):
            records_j = record_buf[j]
            name_j = records_j[1]
            type_j = records_j[2]
            begin_line_j = int(records_j[3])
            end_line_j = int(records_j[4])
            split_name_j = records_j[5]
            if (end_line_i < begin_line_j) or (begin_line_i > end_line_j):
                continue
            print(records_i[0], name_i, name_j,
                  (str(begin_line_i) + '--' + str(end_line_i) + ',' + str(begin_line_j) + '--' + str(end_line_j)),
                  split_name_i, split_name_j,
                  sep='\t')


# header
print("path", "name1", "name2", "range", "words1", "word2", sep='\t')

current_path = None
record_buf = []
is_header = True
for line in fileinput.input(files='-'):
    if is_header:
        is_header = False
        continue
    line = line.strip()
    records = line.split('\t')
    path = records[0]
    if current_path is not None and current_path != path:
        extract_available_pairs(record_buf)
        record_buf = []

    current_path = path
    record_buf.append(records)

if len(record_buf) > 0:
    extract_available_pairs(record_buf)
