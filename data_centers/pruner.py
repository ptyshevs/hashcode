from helpers import parse

print(parse())
def magic():
    R, S, U, P, M, unavaiable, servers = parse()
    servers = sorted(servers, key=lambda x: x[1], reverse=True)
    print(servers)

    rows = []
    for i in range(R):
        rows.append("a"*S)

    for i in range(U):
        rows[unavaiable[i][0]] = rows[unavaiable[i][0]][:unavaiable[i][1]] + 'u' + rows[unavaiable[i][0]][unavaiable[i][1]+1:]

    result = []
    #    done = 0
    while len(servers) > 0:
        for i in range(R):
            if servers[0][0]*'a' in rows[i]:
                slot = rows[i].find(servers[0][0]*'a')
                rows[i] = rows[i][:slot] + servers[0][0]*'u' + rows[i][slot + servers[0][0]:]
                result.append([[i, slot],servers[0]])
                break
        del servers[0]
    for i in range(R):
        print(rows[i])
    print(result)

magic()