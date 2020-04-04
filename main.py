import heapq
import copy

#define the node object to be used in the tree search algorithm
class Node:
    def __init__(self,grid,costToGoal,pathCost,action,prev):
        #the grid(the puzzle state)
        self.grid=grid
        #costToGoal(h(n)),
        self.ctg=costToGoal
        #pathCost(g(n))
        self.pc=pathCost
        #evaluationValue(f(n))
        self.eval=self.ctg+self.pc
        #this finds the position of the blank space
        self.spacePosition=findSpace(grid)
        #this record the action taken in this step
        self.action=action
        #this is used to trace back all the actions
        self.prev=prev
    #define custom comparison for node objects
    #These are used to compare the f(n)s of different nodes and form the priority queue
    def __lt__(self,other):
        return self.eval<other.eval
    def __gt__(self,other):
        return other.eval<self.eval
    def __eq__(self,other):
        return self.eval==other.eval
    

#this function finds the blank space in the grid
def findSpace(grid):
    for i in range(4):
        for j in range(4):
            if grid[i][j]==0:
                return (i,j)
#this function finds the manhattan distance between two nodes
def manhattanDistance(cur,goal):
    output=0
    for i in range(len(cur)):
        for j in range(len(cur[0])):
            target=cur[i][j]
            if target==0:
                continue
            found=0
            for k in range(len(goal)):
                for l in range(len(goal[0])):
                    if target==goal[k][l]:
                        output+=abs(i-k)
                        output+=abs(j-l)
                        found=1
                        break
                if found==1:
                    break
    return output


#reads the content of the files provided
#each line in the file must end in number, aka must delete the spaces after the numbers for each row
def read(filename):
    f=open(filename,"r")
    start=[]
    end=[]
    for i in range(4):
        start.append(f.readline().split(" "))
        for j in range(4):
            start[i][j]=int(start[i][j])
    garbage=f.readline()
    for i in range(4):
        end.append(f.readline().split(" "))
        for j in range(4):
            end[i][j]=int(end[i][j])
    return start,end

#main body of the aStarSearch
#takes two parameters, the start state and end state of the search
def aStarSearch(start,end):
    #create a list to store the explored states
    explored=[]
    #create an empty list, put in the initial state as a node
    startNode=Node(start,manhattanDistance(start,end),0,"",None)
    frontier=[]
    frontier.append(startNode)
    #use heapify to make the frontier a priority queue
    heapq.heapify(frontier)
    #use a variable to keep track of the number of nodes generated
    nodecount=1
    while frontier:
        #read the first node in the priority queue(frontier)
        cur=heapq.heappop(frontier)
        #if it is the goal node, return it and the nodecount
        if cur.grid==end:
            return cur,nodecount
        #if it is explored, ignore it and go to the next node
        #if not, adds it to the explored list and proceed
        if cur.grid in explored:
            continue
        else:
            explored.append(cur.grid)
        #read the posision of the blank space of the current state
        curI,curJ=cur.spacePosition
        #if there is place for the blank space to move up, move it up and store the result node into the priority queue
        if curI>0:
            up=copy.deepcopy(cur.grid)
            up[curI][curJ],up[curI-1][curJ]=up[curI-1][curJ],up[curI][curJ]
            heapq.heappush(frontier,Node(up,manhattanDistance(up,end),cur.pc+1,"U",cur))
            nodecount+=1
        #if there is place for the blank space to move down, move it down and store the result node into the priority queue
        if curI<3:
            down=copy.deepcopy(cur.grid)
            down[curI][curJ],down[curI+1][curJ]=down[curI+1][curJ],down[curI][curJ]
            heapq.heappush(frontier,Node(down,manhattanDistance(down,end),cur.pc+1,"D",cur))
            nodecount+=1
        #if there is place for the blank space to move left, move it left and store the result node into the priority queue
        if curJ>0:
            left=copy.deepcopy(cur.grid)
            left[curI][curJ],left[curI][curJ-1]=left[curI][curJ-1],left[curI][curJ]
            heapq.heappush(frontier,Node(left,manhattanDistance(left,end),cur.pc+1,"L",cur))
            nodecount+=1
        #if there is place for the blank space to move right, move it right and store the result node into the priority queue
        if curJ<3:
            right=copy.deepcopy(cur.grid)
            right[curI][curJ],right[curI][curJ+1]=right[curI][curJ+1],right[curI][curJ]
            heapq.heappush(frontier,Node(right,manhattanDistance(right,end),cur.pc+1,"R",cur))
            nodecount+=1

#this runs the code above and print the needed stats
#to run the code on different input files just change the names of the file
def main():
    start,end=read("Input4.txt")
    goalNode,nodeCount=aStarSearch(start,end)
    print(nodeCount)
    helper=goalNode
    outAction=""
    outFValue=""
    print(goalNode.pc)
    while helper is not None:
        outAction=helper.action+" "+outAction
        outFValue=str(helper.eval)+" "+outFValue
        print(helper.grid)
        helper=helper.prev
    print(outAction)
    print(outFValue)

main()