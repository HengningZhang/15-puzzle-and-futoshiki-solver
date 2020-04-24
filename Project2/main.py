import heapq
import copy

def read(filename):
    f=open(filename,"r")
    start=[]
    leftRight=[]
    upDown=[]
    for i in range(5):
        start.append(f.readline().split(" "))
        for j in range(5):
            start[i][j]=int(start[i][j])
    f.readline()
    for i in range(5):
        leftRight.append(f.readline().split(" "))
    f.readline()
    for i in range(4):
        upDown.append(f.readline().split(" "))
    return start,leftRight,upDown


class node:
    def __init__(self,board,leftRightConstraints,upDownConstraints):
        self.board=board
        self.status=checkFilled(board)
        self.lrc=leftRightConstraints
        self.udc=upDownConstraints
        self.domains=generateDomains(board)
        self.valid=forwardChecking(self.domains,self.lrc,self.udc)
        self.mcdv,self.constrainingNum=mostConstrainVariable(self.board,self.domains)
        self.lenMCDV=len(self.domains[self.mcdv[0]][self.mcdv[1]])
    def __lt__(self,other):
        if self.lenMCDV==other.lenMCDV:
            return self.constrainingNum>other.constrainingNum
        return self.lenMCDV<other.lenMCDV
    def __gt__(self,other):
        return other<self
    def __eq__(self,other):
        return self.lenMCDV==other.lenMCDV and self.constrainingNum==other.constrainingNum

def checkFilled(board):
    for i in range(5):
        for j in range(5):
            if board[i][j]==0:
                return False
    else:
        return True
def generateDomains(board):
    domains=[[] for i in range(5)]
    for i in range(5):
        for j in range(5):
            if board[i][j]==0:
                domain=[1,2,3,4,5]
                for k in range(5):
                    if board[i][k] in domain:
                        domain.remove(board[i][k])
                    if board[k][j] in domain:
                        domain.remove(board[k][j])
                domains[i].append(domain)
            else:
                domains[i].append([board[i][j]])
    return domains

def forwardChecking(domains,leftRightConstraints,upDownConstraints):
    valid=True
    for n in range(5):
        for i in range(5):
            for j in range(4):
                if leftRightConstraints[i][j][0]==">":
                    for k in range(max(domains[i][j]),6):
                        if k in domains[i][j+1]:
                            domains[i][j+1].remove(k)
                elif leftRightConstraints[i][j][0]=="<":
                    for k in range(max(domains[i][j+1]),6):
                        if k in domains[i][j]:
                            domains[i][j].remove(k)
        for i in range(4):
            for j in range(5):
                if upDownConstraints[i][j][0]=="v":
                    for k in range(max(domains[i][j]),6):
                        if k in domains[i+1][j]:
                            domains[i+1][j].remove(k)
                elif upDownConstraints[i][j][0]=="^":
                    for k in range(max(domains[i+1][j]),6):
                        if k in domains[i][j]:
                            domains[i][j].remove(k)
    for i in range(5):
        for j in range(5):
            if not domains[i][j]:
                valid=False
    return valid 
def mostConstrainVariable(board,domains):
    minCount=5
    maxCount=0
    mcdv=(0,0)
    constrainingNum=0
    for i in range(5):
        for j in range(5):
            if board[i][j]==0 and len(domains[i][j])<=minCount:
                counter=board[i].count(0)-1
                for k in range(5):
                    if board[k][j]==0:
                        counter+=1
                counter-=1
                if len(domains[i][j])<minCount:
                    minCount=len(domains[i][j])
                    mcdv=(i,j)
                    constrainingNum=counter
                    maxCount=counter
                elif len(domains[i][j])==minCount:
                    if counter>maxCount:
                        mcdv=(i,j)
                        constrainingNum=counter
                        maxCount=counter
    return mcdv,constrainingNum


def backTrack(anode):
    frontier=[]
    frontier.append(anode)
    heapq.heapify(frontier)
    while frontier:
        current=heapq.heappop(frontier)
        if current.status==True:
            return current.board
        index=current.mcdv
        domain=current.domains[index[0]][index[1]]
        for i in range(len(domain)):
            newBoard=copy.deepcopy(current.board)
            newBoard[index[0]][index[1]]=domain[i]
            newNode=node(newBoard,current.lrc,current.udc)
            if newNode.valid==True:
                heapq.heappush(frontier,newNode)
    return False


data=read("input1.txt")
for elem in generateDomains(data[0]):
    print(elem)
for elem in data[1]:
    print(elem)
for elem in data[2]:
    print(elem)
anode=node(data[0],data[1],data[2])
for elem in anode.domains:
    print(elem)


print(backTrack(anode))