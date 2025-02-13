from helpers import parse

def magic(path='input/example.in'):
    R, S, U, P, M, unavaiable, servers = parse(path)
    for i in range(len(servers)):
        servers[i].append(i)
    servers = sorted(servers, key=lambda x: x[0], reverse=True)
#     print(servers)

    rows = []

    for i in range(R):
        rows.append("a"*S)

    for i in range(U):
        rows[unavaiable[i][0]] = rows[unavaiable[i][0]][:unavaiable[i][1]] + 'u' + rows[unavaiable[i][0]][unavaiable[i][1]+1:]

    result = []
    while len(servers) > 0:
        i = -1
        for k in range(R):
            if servers[0][0]*'a' in rows[k] and (i == -1 or rows[k].count('a') >= rows[i].count('a')):
                i = k
        if i != -1:
            slot = rows[i].find(servers[0][0]*'a')
            rows[i] = rows[i][:slot] + servers[0][0]*'u' + rows[i][slot + servers[0][0]:]
            result.append([[i, slot],servers[0]])
        del servers[0]
#     for i in range(R):
#         print(rows[i])
    return result

magic()