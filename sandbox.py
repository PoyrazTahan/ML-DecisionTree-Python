from __future__ import division
from math import log
import Tkinter as tk

class Node():
    def __init__(self):
        self.name = ""
        self.children = []
        self.branches = []
        self.path = ""
        self.isLeaf = False

output = None
OUTPUTATTRIBUTES = None
W=1000
H = 700

root = tk.Tk()
canvas = tk.Canvas(root, width=W, height=H, borderwidth=0, highlightthickness=0, bg="white")
canvas.grid()

startX = W/2
startY = 100
layerTickness = 200
layerCounter = 0
layerArray = []

def create_circle( x, y, r, **kwargs):
    canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def create_text(x,y,str):
    txt = canvas.create_text(x, y, font=("Purisa", 12), text= str)
    canvas.itemconfig(txt, text=str)

def create_rectangle(x1,y1,x2,y2, **kwargs):
    canvas.create_rectangle(x1,y1,x2,y2, **kwargs)

def displayTreeGraph(node=None):
    global startX
    global startY
    global layerCounter

    if node.isLeaf == True:
        create_circle()
        print node.path,"OUTPUT =", node.name
        layerCounter+=(-1)
    else:
        for i in range (len(node.children)):
            node.children[i].path += str(node.path+node.name.upper()+"="+ node.branches[i]+"->")
            displayTreeGraph(node.children[i])




def Main():
    global output
    global OUTPUTATTRIBUTES

    dataSetTable = getDataSetTable('./dataSets/dataset1.txt')

    output = dataSetTable[0][len(dataSetTable[0])-1]
    OUTPUTATTRIBUTES = getAttributes(output,dataSetTable)

    labels = dataSetTable[0]
    data = dataSetTable[1:][:]

    root = ID3(data, labels)
    displayTree(root)

def displayTree(node=None):
    if node.isLeaf == True:
        print node.path,"OUTPUT =", node.name
    else:
        for i in range (len(node.children)):
            node.children[i].path += str(node.path+node.name.upper()+"="+ node.branches[i]+"->")
            displayTree(node.children[i])

def ID3(data,labels):
    classList = [ex[-1] for ex in data]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(data) == 1:
        return data[0][len(data[0])-1]

    if len(data[0]) == 1:
        return majority(classList)

    bestF = getBestFeature(data)
    bestFLabel = labels[bestF]

    node = Node()
    node.name = bestFLabel
    del(labels[bestF])
    featValues = [ex[bestF] for ex in data]
    uniqueVals = list(set(featValues))
    node.branches = uniqueVals
    for value in uniqueVals:
        subLabels = labels[:]
        newNode = ID3(split(data, bestF, value),subLabels)
        if type(newNode) != str:
            node.children.append(newNode)
        else:
            n = Node()
            n.name = newNode
            n.isLeaf=True
            node.children.append(n)

    return node

def getBestFeature(data):
    features = len(data[0]) - 1

    informationGains = [0 for i in range(len(data[0]) - 1)]

    for i in range(features):
        parentEntropy, totalRow = entropy(data)

        attributes = getAttributes(data[0][i], data)
        childEntropies = [[0 for k in range(len(attributes))] for l in range(2)]
        counter = 0
        for j in attributes:  # for each attribute
            filteredTable = split(data, i, j)
            childEntropies[0][counter], childEntropies[1][counter] = entropy(filteredTable)
            counter += 1

        informationGains[i] = gain(parentEntropy, childEntropies, totalRow)
    return informationGains.index(max(informationGains))

def split(data, axis, val):
    newData = []
    for feat in data:
        if feat[axis] == val:
            reducedFeat = feat[:axis]
            reducedFeat.extend(feat[axis+1:])
            newData.append(reducedFeat)
    return newData

def majority(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def gain(parentEnt, entropyList, rowCount):
    weightedAverage = 0
    for i in range(len(entropyList[0])):
        weightedAverage += entropyList[1][i] / rowCount * entropyList[0][i]
    return parentEnt - weightedAverage

def entropy(table):
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
    return total, len(table)

def getAttributes(feature, dataSetTable):
    attributes = []
    column = dataSetTable[0].index(feature)
    for i in range(1, len(dataSetTable)):
        if attributes.__contains__(dataSetTable[i][column]) is not True:
            attributes.append(dataSetTable[i][column])
    return attributes

def getDataSetTable(path):
    table = []
    with open(path, 'r') as file:
        for line in file:
            tmp = []
            for word in line.split(","):
                tmp.append(word.strip())
            table.append(tmp)
    return table


if __name__ == '__main__':
    Main()