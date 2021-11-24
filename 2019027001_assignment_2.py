from random import randint

ITER_COUNT = 10000
BOARD_SIZE = 5
BOMB_SCORE = -100
BONUS_SCORE = 1
GOAL_SCORE = 100
GAMMA = 0.9
INF = 1e9
VALID_MOVE = [ -BOARD_SIZE, -1, 1, BOARD_SIZE ]

board = [ 0 for i in range(BOARD_SIZE * BOARD_SIZE) ]
qweight = [ [ 0. for i in range(BOARD_SIZE * BOARD_SIZE) ] 
                 for i in range(BOARD_SIZE * BOARD_SIZE) ]

def getIndex(r, c):
    return r * BOARD_SIZE + c

def valid(before, now, next):
    if next < 0 or next >= BOARD_SIZE * BOARD_SIZE:
        return False
    if before == next:
        return False
    if now + 1 == next and now % BOARD_SIZE == BOARD_SIZE - 1:
        return False
    if now - 1 == next and now % BOARD_SIZE == 0:
        return False
    return True

def getValidMoves(before, now):
    nextlist = []
    for i in VALID_MOVE:
        if valid(before, now, now - i):
            nextlist.append(now - i)
    return nextlist

def evaluate(now, next):
    val = -INF
    nextlist = getValidMoves(now, next)
    for i in nextlist:
        val = max(val, qweight[next][i])
    return board[next] + GAMMA * val

def main():
    fin = open('input.txt','r')
    lines = fin.readlines()
    linecnt = 0
    start = -1
    for line in lines:
        for i in range(BOARD_SIZE):
            if line[i] == 'S':
                start = getIndex(linecnt, i)
            elif line[i] == 'B':
                board[getIndex(linecnt, i)] = BOMB_SCORE
            elif line[i] == 'T':
                board[getIndex(linecnt, i)] = BONUS_SCORE
            elif line[i] == 'G':
                board[getIndex(linecnt, i)] = GOAL_SCORE
        linecnt += 1
    if start < 0:
        print('No start point')
        return
    for i in range(ITER_COUNT):
        now = start
        before = start
        while board[now] != GOAL_SCORE:
            nextlist = getValidMoves(before, now)
            next = nextlist[randint(0, len(nextlist) - 1)]
            qweight[now][next] = evaluate(now, next)
            before = now
            now = next
    fout=open('output.txt','w')
    startval = -INF
    before = start
    now = start
    fout.write(str(now))
    while board[now] != GOAL_SCORE:
        nextlist = getValidMoves(before, now)
        curval = -INF
        next = -1
        for i in nextlist:
            if qweight[now][i] > curval:
                if now == start:
                    startval = max(startval, qweight[now][i])
                curval = max(curval, qweight[now][i])
                next = i
        if next == -1:
            print('No valid moves')
            return
        fout.write(' ' + str(next))
        before = now
        now = next
    fout.write('\n')
    fout.write(str(startval))

    fin.close()
    fout.close()

main()