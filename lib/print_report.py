import sys

args = sys.argv

string_th = float(args[1])
semantic_th = float(args[2])

string_results = args[3]
semantic_results = args[4]

report_file = args[5]

data = []
is_header = True
with open(string_results) as f:
    for line in f:
        if is_header:
            is_header = False
            continue
        line = line.strip()
        path, name1, name2, scope, sim = line.split('\t')
        record = { 'path': path,
                   'name1': name1 + ' @(' + scope.split(',')[0] + ')',
                   'name2': name2 + ' @(' + scope.split(',')[1] + ')',
                   'confusing': 0,
                   'string_sim': float(sim)
                 }
        if float(sim) > string_th:
            record['confusing'] = 1
        data.append(record)

is_header = True
idx = 0
with open(semantic_results) as f:
    for line in f:
        if is_header:
            is_header = False
            continue
        line = line.strip()
        path, name1, name2, scope, sim = line.split('\t')
        record = data[idx]
        record['semantic_sim'] = float(sim)
        if float(sim) > semantic_th:
            record['confusing'] = record['confusing'] + 1
        idx = idx + 1

data.sort(key=lambda x: x['confusing'], reverse=True)

count = 0
for i in range(len(data)):
    if data[i]['confusing'] > 0:
        count = count + 1

if count == 0:
    print('No confusing variable pair found')
else:
    print(str(count) + ' confusing variable pair', end='')
    if ( count > 1 ):
        print('s', end='')
    print(' found !')
    print('see ' + report_file + ' for the details.')
with open(report_file, 'w') as f:
    # header
    print("path", "confusing", "name1", "name2", "string_similarity", "semantic_similarity", sep=',', file=f)
    for i in range(len(data)):
        confusing_mark = ''
        for j in range(data[i]['confusing']):
            confusing_mark = confusing_mark + '*'
        print(data[i]['path'], confusing_mark, data[i]['name1'], data[i]['name2'], data[i]['string_sim'], data[i]['semantic_sim'], sep=',', file=f)
