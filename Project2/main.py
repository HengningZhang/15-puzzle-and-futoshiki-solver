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
    garbage=f.readline()
    for i in range(5):
        leftRight.append(f.readline().split(" "))
    garbage=f.readline()
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
        self.mcdv=mostConstrainedVariable(self.board,self.domains)
        self.lenMCDV=len(self.domains[self.mcdv[0]][self.mcdv[1]])
        self.mcgv=mostConstrainingVariable(self.board)
        self.lenMCGV=len(self.domains[self.mcgv[0]][self.mcgv[1]])
    def __lt__(self,other):
        if self.lenMCDV==other.lenMCDV:
            return self.lenMCGV<other.lenMCGV
        return self.lenMCDV<other.lenMCDV
    def __gt__(self,other):
        return other<self
    def __eq__(self,other):
        return self.lenMCDV==other.lenMCDV and self.lenMCGV==other.lenMCGV

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
        for j in range(4):
            if leftRightConstraints[i][j][0]==">":
                for k in range(max(domains[i][j]),6):
                    if k in domains[i][j+1]:
                        domains[i][j+1].remove(k)
            elif leftRightConstraints[i][j][0]=="<":
                for k in range(max(domains[i][j+1]),6):
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
    mcgv=(0,0)
    for i in range(5):
        for j in range(5):
            if len(domains[i][j])<minCount and board[i][j]==0:
                minCount=len(domains[i][j])
                mcdv=(i,j)
                counter=board[i].count(0)-1
                for k in range(5):
                    if board[k][j]==0:
                        counter+=1
                counter-=1
                if counter>maxCount:
                    mcgv=(i,j)
    return mcdv,mcgv
# def mostConstrainingVariable(board):
#     maxCount=0
#     output=(0,0)
#     for i in range(5):
#         for j in range(5):
#             if board[i][j]==0:
#                 counter=board[i].count(0)
#                 for k in range(5):
#                     if board[k][j]==0:
#                         counter+=1
#                 if counter>maxCount:
#                     output=(i,j)
#     return output

def backTrack(node):
    if node.status==True:
        return node.board
    unassigned=node.mc

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

print(anode.mcdv)
print(anode.mcgv)
print(anode.board)
