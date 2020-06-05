import heapq
import copy

#read the input files
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

#define the node object to be used later
#it takes the game board and the constraints as input
#use the generateDomains function to turn the board into a scratch domains matrix just using the rule that no duplicate number would be in each row and each line
#use inequality as the heuristics for forward checking and further narrow the domains
#the most constrained variable's position and the number of variables it constraints are calculated by the mostConstrainVariable function
#the domain size of the most constrained variable is calculated by its length
#the domain size of the most constrained variable is also used to form a priority queue, which would be used later to decide the best way to assign a value to a variable
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

#checks if all the variables has values assigned to them
def checkFilled(board):
    for i in range(5):
        for j in range(5):
            if board[i][j]==0:
                return False
    else:
        return True

#generate the scratch domains for the variables in the board
#using just the simple rule of no duplicate value in each row and each line
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

#the main algorithm in this solution
#use the inequalities to further constrain the domains
#bigger than means that the smaller variable can only have the values that are less than the bigger variable's max possible value
#checks if there is any variable ended up with no value available to them in each step, return False and end if there is an empty domain
def forwardChecking(domains,leftRightConstraints,upDownConstraints):
    for n in range(5):
        for i in range(5):
            for j in range(5):
                if not domains[i][j]:
                    return False

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
                    return False
                    
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
    return True

#gets the most constrained variable by checking whether the position is still 0 in the board and whether a variable has the smallest domain
#gets the most constrained variable's constrainingNum(how many variable it constraints) by checking how many variables in its same row and column have not been assigned value
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

#create a priority queue with the initial board and the constraints
#assign a value to the most constrained variable and push the new nodes created by this operation into the priority queue if the new node is valid(satisfies the constraints)
#pick the node with the most constrained variable, assign a value to it and do the same thing again
#if two nodes both have the most constrained variable, break the tie by checking how many other variables they each constraints
#do all the things above again and again until every place in the block has been filled
#the all-filled board would be the solution
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


data=read("Input3.txt")
# for elem in generateDomains(data[0]):
#     print(elem)
# for elem in data[1]:
#     print(elem)
# for elem in data[2]:
#     print(elem)
anode=node(data[0],data[1],data[2])
# for elem in anode.domains:
#     print(elem)


print(backTrack(anode))