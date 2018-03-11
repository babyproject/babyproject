import numpy as mp

inputData=[]
lis=[]
box=[10, 20]
step=3
for point in inputData[box[0]:len(inputData)-box[0]]:
    for x in range(point[0]-box[0], point[0]-box[0]):
        if inputData[x][1] not in range(point[1]-box[1], point[1]-box[1])
        lis.append(inputData[x])

for x in range(box[0], len(inputData)-box[0], step):
    for px in range(x-box[0], x+box[0], 1):
        if inputData[px][1] not in range(inputData[x][1]-box[1], inputData[x][1]+box[1]):
            lis.append(inputData[x])
