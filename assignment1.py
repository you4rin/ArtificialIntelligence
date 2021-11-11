from random import randint
from queue import Queue
from sys import setrecursionlimit

def bfs(q,idx,n,row,ldiag,rdiag,qlist):
    for i in range(n):
        if ((1<<i)&row)!=0:
            continue
        if ((1<<(i+(n-idx-1)))&ldiag)!=0:
            continue
        if ((1<<(i+idx))&rdiag)!=0:
            continue
        qlist.append(i+1)
        q.put([idx+1,n,row|(1<<i),ldiag|(1<<(i+(n-idx-1))),rdiag|(1<<(i+idx)),qlist[:]])
        qlist.pop()

def hfunc(state):
    ret=0
    for i in range(len(state)):
        for j in range(i+1,len(state)):
            if state[i]==state[j]:ret+=1
            elif abs(i-j)==abs(state[i]-state[j]):ret+=1
    return ret

def hc(n,curstate,val):
    while True:
        if val==0:
            return curstate
        board=[[0 for _ in range(n)] for _ in range(n)]
        y=x=None
        nextval=val
        for i in range(n):
            for j in range(n):
                tmpstate=curstate[:]
                if(curstate[i]==j+1):
                    board[i][j]=val
                    continue
                tmpstate[i]=j+1
                board[i][j]=hfunc(tmpstate)
        for i in range(n):
            for j in range(n):
                if board[i][j]<nextval:
                    y,x=i,j
                    nextval=board[i][j]
        if y==None:
            return None
        curstate[y]=x+1
        val=nextval

def csp(cnt,n,forbidden,legalcnt,state):
    if(cnt==n):
        return state
    nextval=n+1
    nextidx=None
    for i in range(n):
        if state[i]!=0:
            continue
        if nextval>legalcnt[i]:
            nextval=legalcnt[i]
            nextidx=i
    if nextval==0:
        return None
    for i in range(n):
        if forbidden[nextidx]&(1<<i):
            continue
        nextforbidden=forbidden[:]
        nextlegalcnt=legalcnt[:]
        nextstate=state[:]
        nextstate[nextidx]=i+1
        for j in range(n):
            if nextstate[j]!=0:
                continue
            if (nextforbidden[j]&(1<<i))==0:
                nextforbidden[j]|=(1<<i)
                nextlegalcnt[j]-=1
            if i+abs(nextidx-j)<n and (nextforbidden[j]&(1<<(i+abs(nextidx-j))))==0:
                nextforbidden[j]|=1<<(i+abs(nextidx-j))
                nextlegalcnt[j]-=1
            if i-abs(nextidx-j)>=0 and (nextforbidden[j]&(1<<(i-abs(nextidx-j))))==0:
                nextforbidden[j]|=1<<(i-abs(nextidx-j))
                nextlegalcnt[j]-=1
        ret=csp(cnt+1,n,nextforbidden,nextlegalcnt,nextstate)
        if ret!=None:
            return ret
    return None

def main():
    setrecursionlimit(10**6)
    fin=open('input.txt','r')
    lines=fin.readlines()
    for line in lines:
        if len(line.split())<2:
            break
        n,algo=line.split()
        n=int(n)
        ret=None
        if algo=='bfs':
            q=Queue()
            q.put([0,n,0,0,0,[]])
            while(not q.empty()):
                front=q.get()
                if front[0]==n:
                    ret=front[5][:]
                    break
                bfs(q,*front)
        if algo=='hc':
            for i in range(30+4*n):
                initstate=[randint(1,n) for _ in range(n)]
                initval=hfunc(initstate)
                ret=hc(n,initstate,initval)
                if ret!=None:
                    break
        if algo=='csp':
            forbidden=[0 for i in range(n)]
            legalcnt=[n for i in range(n)]
            state=[0 for i in range(n)]
            ret=csp(0,n,forbidden,legalcnt,state)
        fout=open(str(n)+'_'+algo+'_'+'output.txt','w')
        if(ret==None):
            fout.write('no solution\n')
        else:
            for i in ret:
                fout.write(str(i)+' ')
            fout.write('\n')
        fout.close()
    fin.close()

main()