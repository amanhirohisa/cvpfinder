import fileinput

def Levenshtein_distance(str1, str2):
    upper_row = []
    lower_row = []
    for j in range(len(str2)+1):
        upper_row.append(j)
        lower_row.append(0)

    for i in range(len(str1)):
        lower_row[0] = upper_row[0] + 1
        for j in range(1, len(str2)+1):
            dist = upper_row[j-1]
            if str1[i] != str2[j-1]:
                dist = dist + 1
            if dist > upper_row[j] + 1:
                dist = upper_row[j] + 1
            if dist > lower_row[j-1] + 1:
                dist = lower_row[j-1] + 1

            lower_row[j] = dist

        for j in range(len(lower_row)):
            upper_row[j] = lower_row[j]

    return lower_row[-1]

# header
print("path", "name1", "name2", "range", "string_similarity", sep='\t')

is_header = True
for line in fileinput.input(files='-'):
    if is_header:
        is_header = False
        continue
    line = line.strip()
    records = line.split('\t')
    path = records[0]
    name1 = records[1]
    name2 = records[2]
    scope = records[3]
    ld = Levenshtein_distance(name1, name2)
    max_len = len(name1)
    if max_len < len(name2):
        max_len = len(name2)
    nd = ld/max_len
    sim = 1 - nd

    print(path, name1, name2, scope, sim, sep='\t')
