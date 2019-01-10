from __future__ import division
from math import log

import Tkinter as tk



### Classes Created For the ID3 Algo

class Node():
    '''
    This class is representation of a decision tree's branching points.

    '''
    def __init__(self):
        self.name = ""  # Holds the feature to be breaking the dataset upon
        self.children = []  # Holds the one layer deeper in the node
        self.branches = []  # Holds the atrributes unique values in a feature
        self.path = ""  # Records in string how we are able to reach that node. // we will record this from parent rows to child rows
        self.isLeaf = False  # indicates if the decision has been made. Indicate if the tree is over as layer-wise

        self.layer = 1
        self.orderInLayer = 0

### Classes Created For Graph ###

class GraphScreen():
    def __init__(self):
        self.screenHeight = 0
        self.screenWidth = 0
        self.graphLayer = []
        self.layerNumber = 0
        self.layerIndexCounter = []

class GraphLayer():
    def __init__(self):
        self.layerDegree = 0
        self.xCoord = 0
        self.yCoord = 0
        self.width = 0
        self.height = 0
        self.gridNumber = 0
        self.GraphGridNode = []

class GraphGridNode():
    def __init__(self):
        self.xCoord = 0
        self.yCoord = 0
        self.width = 0
        self.height = 0
        self.GraphFeatureNode = []
        self.GraphBranchList = []
        self.isLeaf = False

class GraphFeatureNode():
    def __init__(self):
        self.xCoord = 0
        self.yCoord = 0
        self.width = 0
        self.height = 0
        self.name = ""
        self.isLeaf = False

class GraphBranchList():
    def __init__(self):
        self.xCoord = 0
        self.yCoord = 0
        self.width = 0
        self.height = 0
        self.branchNumber = 0
        self.branchNames = []




output = None # output features name
OUTPUTATTRIBUTES = None # output columns attributes
# // this global since these are main objectives we will use it a lot in order to be efficient we made it global

### Globals Needed for Graph ###
maxLayer = 0

layerIndexCounters2 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

layerHeight = 150

gridWidth = 100

featureNodeWidth = 80



def Main():
    '''
    Main function for this work.
    To cahange the data sat change the number at end of ('./dataSets/dataset1.txt') in 7 row below
    :return:
    '''
    global output
    global OUTPUTATTRIBUTES

    ###### !!!!!!!!!! TO CHANGE THE EXAMPLE CHANGE THE NUMBER AT THE END OF DATABASE !!!!!!!!!!!! ########
    dataSetTable = getDataSetTable('./dataSets/dataset3.txt') # reading the data

    # get data decision criterias
    output = dataSetTable[0][len(dataSetTable[0])-1] #
    OUTPUTATTRIBUTES = getAttributes(output, dataSetTable)

    # split the examples of the data with the features
    labels = dataSetTable[0]  # Feautures' names
    data = dataSetTable[1:][:]  # examples , occurunces, data

    ### begining of the algo. ###
    #starts the recursive function until it forms a Decision Tree
    root = constructDecisionTree(data, labels)

    # Displays the output for each path way. For example if the decision tree has 5 leaf it will display how it got there for each path
    displayTreePathWay(root)




    screen = GraphScreen()

    collectNecceseryDataForTheGraph(root, screen)
    screen.layerNumber = maxLayer
    screen.layerIndexCounter = layerIndexCounters2

    screen.screenHeight = maxLayer * layerHeight
    screen.screenWidth = max(layerIndexCounters2) * gridWidth

    screen = constructBaseSCreen(screen)
    displayTree(screen, root)

    #collectNecceseryDataForTheGraph2(root, screen)

    #displayTree2(root, screen)
### ID3 Algo ###

def constructDecisionTree(data,labels):
    '''

    :param data: this is the example set
    :param labels: this is the features names
    :return node: at the end returns a decision tree with nodes at different layers
    '''


    classList = [ex[-1] for ex in data]

    ### Control Phase starts

    # Control: if the column at hand has one attribute //or// entropy == 0 ?
    if classList.count(classList[0]) == len(classList):
        #returns any element of the class since they are the same
        return classList[0]

    # Control: Are we only left with a single example //or // entropy == 0 ?
    if len(data) == 1:
        return data[0][len(data[0])-1]
        ## Disclamer: We could have called entropy function but that would be inefficient since we can control with these two if statements

    # Control: Are we left with a single column
    if len(data[0]) == 1:
        # if we are left with just one column we can not extract any more information then we will return with the majority of the decision
        return majority(classList)

    ### Control Phase ends

    bestF = getBestFeature(data) # records the best feature we should use to divide out Data upon !-int (index)
    bestFLabel = labels[bestF]  # record the name of the feature in !-String

    node = Node() # Creates another node in the tree
    node.name = bestFLabel # labels the new class

    del(labels[bestF])



    featValues = [ex[bestF] for ex in data]

    # sets the attribute in the way to one layer deeper in the tree
    uniqueVals = list(set(featValues))
    node.branches = uniqueVals

    for value in uniqueVals:
        subLabels = labels[:]
        newNode = constructDecisionTree(split(data, bestF, value),subLabels)
        if type(newNode) != str:
            node.children.append(newNode)
        else:
            n = Node()
            n.name = newNode
            n.isLeaf=True
            node.children.append(n)

    # when the code comes this point it constructed a complete tree in a class family
    return node


### MATH FUNCTIONS ###

def gain(parentEnt, entropyList, rowCount):
    '''
    Calculates the information gain of the given for each attribute

    :param parentEnt: the entropy of the higher layer
    :param entropyList: the entropies of the classes if we were to divide them
    :param rowCount:
    :return:
    '''
    weightedAverage = 0
    for i in range(len(entropyList[0])):
        weightedAverage += entropyList[1][i] / rowCount * entropyList[0][i]



    #print "gain:",float(format(parentEnt - weightedAverage, '.3f'))
    return float(format(parentEnt - weightedAverage, '.3f'))

def entropy(table):
    '''
    Calculates the entropy level by using the formula


    :param table:
    :return:
    '''
    array = [0 for i in range(len(OUTPUTATTRIBUTES))]


    for i in range(len(table)):
        current = table[i][len(table[0])-1]
        index = OUTPUTATTRIBUTES.index(current)
        array[index]+=1

    total = 0
    for i in array:
        i = i/sum(array)
        if i != 0:
            total += i * log(i,2)
    total *= -1
    total = float(format(total, '.3f'))

    return total, len(table)


### UTILITIES ###

def majority(classList):
    '''
    finds the majority decision in a single left feature table

    :param classList:
    :return:
    '''
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def getAttributes(feature, dataSetTable):
    '''
    returns the unique values in a feature column

    :param feature:
    :param dataSetTable:
    :return:
    '''
    attributes = []
    column = dataSetTable[0].index(feature)
    for i in range(1, len(dataSetTable)):
        if attributes.__contains__(dataSetTable[i][column]) is not True:
            attributes.append(dataSetTable[i][column])
    return attributes

def getDataSetTable(path):
    '''

    :param path:
    :return:
    '''
    table = []
    with open(path, 'r') as file:
        for line in file:
            tmp = []
            for word in line.split(","):
                tmp.append(word.strip())
            table.append(tmp)
    return table

def split(data, axis, val):
    '''
    splits the data into smaller chunks to prepare for recursive call

    new data will be selected of the rows of the attrbute that we are concerned but with out the feature

    :param data: example set
    :param axis: the column/feature to be deleted
    :param val:   the rows/attribute to be selected
    :return: # newdata
    '''

    newData = []
    for feat in data:
        if feat[axis] == val:
            reducedFeat = feat[:axis]
            reducedFeat.extend(feat[axis + 1:])
            newData.append(reducedFeat)
    return newData

def getBestFeature(data):
    '''
    finds the best feature we should divide our tree upon

    :param data:
    :return:
    '''
    features = len(data[0]) - 1

    informationGains = [0 for i in range(len(data[0]) - 1)]

    for i in range(features):
        parentEntropy, totalRow = entropy(data)

        attributes = getAttributes(data[0][i], data)
        childEntropies = [[0 for k in range(len(attributes))] for l in range(2)]
        counter = 0
        for j in attributes:  # for each attribute
            filteredTable = split(data, i, j)
            #print j
            #for k in filteredTable:
                #print k
            childEntropies[0][counter], childEntropies[1][counter] = entropy(filteredTable)
            counter += 1

        informationGains[i] = gain(parentEntropy, childEntropies, totalRow)
    return informationGains.index(max(informationGains))


#### Displaying the Desicion Tree
def displayTree(scr, root):
    root2 = tk.Tk()
    canvas = tk.Canvas(root2, width=scr.screenWidth, height=scr.screenHeight, borderwidth=0, highlightthickness=0, bg="white")
    canvas.grid()

    tk.Canvas.create_circle = _create_circle
    tk.Canvas.create_circle_arc = _create_circle_arc

    #create_rectangle(bbox, **options)


    #canvas.create_rectangle(scr.graphLayer[0].GraphGridNode[0].GraphFeatureNode[0].xCoord, scr.graphLayer[0].GraphGridNode[0].GraphFeatureNode[0].yCoord, scr.graphLayer[0].GraphGridNode[0].GraphFeatureNode[0].xCoord + scr.graphLayer[0].GraphGridNode[0].GraphFeatureNode[0].width, scr.graphLayer[0].GraphGridNode[0].GraphFeatureNode[0].yCoord + scr.graphLayer[0].GraphGridNode[0].GraphFeatureNode[0].height)
    '''
    for i in range(maxLayer):
        for j in range(layerIndexCounters2[i+1]):
            if i == 1:
                scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].name += root.name
            else:    
                scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].name += root.children[]
    '''
    for i in range(maxLayer):
        for j in range(layerIndexCounters2[i+1]):
            canvas.create_rectangle(scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].xCoord,
                                    scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].yCoord,
                                    scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].xCoord +
                                    scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].width,
                                    scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].yCoord +
                                    scr.graphLayer[i].GraphGridNode[j].GraphFeatureNode[0].height)


    root2.wm_title("Decisison Tree")
    root2.mainloop()

def constructBaseSCreen(screen):
    global midScreen

    for i in range(screen.layerNumber):
        newLayer = GraphLayer()
        newLayer.xCoord = 0
        newLayer.yCoord = i * 150
        newLayer.width = screen.screenWidth
        newLayer.height = 150
        newLayer.gridNumber = layerIndexCounters2[i + 1]

        midScreen = newLayer.width / 2  # middle of the screen

        for j in range(newLayer.gridNumber):
            newGrid = GraphGridNode()
            newGrid.height = layerHeight - 4  # 2 pixel margin from above and below
            newGrid.width = gridWidth
            newGrid.yCoord = newLayer.yCoord + 2  # start from 2
            # newGrid.xCoord = midScreen - (layerIndexCounters2[i+1]*(newGrid.width)/2 + (newGrid.width) /2) + (j * (gridWidth + 2))
            newGrid.xCoord = midScreen - (layerIndexCounters2[i + 1] * (newGrid.width) / 2) + (j * gridWidth)
            # newGrid.xCoord = newLayer.xCoord +  ( (i+1) * 2 ) + (i * gridWidth)  # 2 px as margin + number of grid away

            ### Fill Inside Grid ###
            new_F_Node = GraphFeatureNode()

            new_F_Node.xCoord = newGrid.xCoord + 2
            new_F_Node.yCoord = newGrid.yCoord + 2
            new_F_Node.height = (newGrid.height - 4) / 3  # 2 pixel margin from above and below
            new_F_Node.width = newGrid.width - 4

            newGrid.GraphFeatureNode.append(new_F_Node)

            new_B_List = GraphBranchList()

            new_B_List.xCoord = newGrid.xCoord + 2
            new_B_List.yCoord = new_F_Node.yCoord + new_F_Node.height + 2
            new_B_List.height = (newGrid.height - 4) / 3 * 2
            new_B_List.width = new_F_Node.width - 4

            newGrid.GraphBranchList.append(new_B_List)

            ### Filling Grid Ends ###

            newLayer.GraphGridNode.append(newGrid)

        screen.graphLayer.append(newLayer)
    return screen


def collectNecceseryDataForTheGraph2(node=None, scr=GraphScreen):
    global maxLayer
    global layerIndexCounters2

    # scr.layerNumber = 0 # to define the layerNumber

    if node.isLeaf == True:
        # if this is leaf node first writh how it got there with recorded string on node.path & then write the decision
        # print node.path, "OUTPUT =", node.name
        pass

    else:
        # if this not leaf write down to the nome how it got there and call this for every child

        for i in range(len(node.children)):
            # to each child node write the path how it got there
            # node.children[i].path += str(node.path + node.name.upper() + "=" + node.branches[i] + "->")

            # enters layer information


            node.children[i].orderInLayer = layerIndexCounters2[node.layer + 1]
            tmp = node.children[i].name
            print tmp
            #scr.graphLayer[i].GraphGridNode[node.children[i].orderInLayer-1].GraphFeatureNode[0].name += str(tmp)

            collectNecceseryDataForTheGraph2(node.children[i], scr)



def collectNecceseryDataForTheGraph(node=None, scr=GraphScreen):
    global maxLayer
    global layerIndexCounters2

    # scr.layerNumber = 0 # to define the layerNumber

    if node.isLeaf == True:
        # if this is leaf node first writh how it got there with recorded string on node.path & then write the decision
        # print node.path, "OUTPUT =", node.name
        if node.layer >= maxLayer:
            # record the max layer to create layer for the screen
            maxLayer = node.layer

    else:
        # if this not leaf write down to the nome how it got there and call this for every child

        for i in range(len(node.children)):
            # to each child node write the path how it got there
            # node.children[i].path += str(node.path + node.name.upper() + "=" + node.branches[i] + "->")

            # enters layer information
            node.children[i].layer = node.layer + 1
            layerIndexCounters2[node.children[i].layer] += 1

            node.children[i].orderInLayer = layerIndexCounters2[node.children[i].layer]


            collectNecceseryDataForTheGraph(node.children[i], scr)


def displayTreePathWay(node=None):
    '''
    This function outputs
    for each path way. For example if the decision tree has 5 leaf it will display how it got there for each path

    :param node  // the class of the decision tree on the highset level
    '''
    if node.isLeaf == True:
        # if this is leaf node first writh how it got there with recorded string on node.path & then write the decision
        print node.path, "OUTPUT =", node.name
    else:
        # if this not leaf write down to the nome how it got there and call this for every child
        for i in range(len(node.children)):
            # to each child node write the path how it got there
            node.children[i].path += str(node.path + node.name.upper() + "=" + node.branches[i] + "->")
            # !!! new
            # enters layer information
            node.children[i].layer = node.layer + 1

            displayTreePathWay(node.children[i])

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)

def create_rectangle(x1,y1,x2,y2, **kwargs):
    canvas.create_rectangle(x1,y1,x2,y2, **kwargs)

def create_text(x, y, str):
    txt = canvas.create_text(x, y, font=("Purisa", 12), text=str)
    canvas.itemconfig(txt, text=str)

if __name__ == '__main__':
    Main()
