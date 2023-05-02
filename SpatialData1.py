import csv

records = []

with open("./tiger_roads.csv", 'r') as file:
    csvreader = csv.reader(file)
    counter = 0
    AllX = []
    AllY = []
    for row in csvreader:
        if counter > 0:
            recordArray = []
            MBRarray = []
            Xarray = []
            Yarray = []
            linestringArray = []
            for i in row:
                oneLine = i.split(" ")
                Xarray.append(float(oneLine[0]))
                Yarray.append(float(oneLine[1]))
                linestringArray.append([float(oneLine[0]), float(oneLine[1])])
            AllX.append(min(Xarray))
            AllX.append(max(Xarray))
            AllY.append(min(Yarray))
            AllY.append(max(Yarray))
            MBRarray.append([min(Xarray), min(Yarray)])
            MBRarray.append([max(Xarray), max(Yarray)])
            recordArray.append(counter)
            recordArray.append(MBRarray)
            recordArray.append(linestringArray)
            records.append(recordArray)
        counter += 1

gridArray = []
minX = min(AllX)
minY = min(AllY)
maxX = max(AllX)
maxY = max(AllY)
resultsList = []
gridIntersectsWith = []

for x in range(10):
    xList = []
    resultX = []
    gridIntersectsHelper = []

    for y in range(10):
        # ola ta y tha mpainun se mia lista kai auth h lista tha mpainei
        # sthn telikh gia na einai efikto to: paw sto [0][0] ths genikhs listas
        XandYArray = []
        previousX = minX + x * (maxX - minX) / 10
        previousY = minY + y * (maxY - minY) / 10
        nextX = minX + (x + 1) * (maxX - minX) / 10
        nextY = minY + (y + 1) * (maxY - minY) / 10

        if x == 0 and y == 0:
            XandYArray.append(minX)
            XandYArray.append(minY)
            XandYArray.append(nextX)
            XandYArray.append(nextY)
            xList.append(XandYArray)

        elif x == 9 and y == 9:
            XandYArray.append(previousX)
            XandYArray.append(previousY)
            XandYArray.append(maxX)
            XandYArray.append(maxY)
            xList.append(XandYArray)

        else:
            XandYArray.append(previousX)
            XandYArray.append(previousY)
            XandYArray.append(nextX)
            XandYArray.append(nextY)
            xList.append(XandYArray)

        resultX.append(0)
        gridIntersectsHelper.append([])
    resultsList.append(resultX)
    gridArray.append(xList)
    gridIntersectsWith.append(gridIntersectsHelper)

fpGrd = open('grid.grd', 'w')
fpDir = open('grid.dir', 'w')

for i in records:
    for x in range(len(gridArray)):
        for y in range(len(gridArray[x])):
            # HERE WE CHECK IF ANY EDGE OF THE MBR ARE INSIDE OF THE SELECTED GRID
            # 1 TIME FOR EVERY EDGE
            # AFTER WE CHECK THE OTHER SITUATIONS WHERE A MBR OF A LINESTRING IS INVOLVED IN A GRID
            # WHICH ARE
            # ONE: THE ΜΒΡ IS BIGGER THAN THE GRID AND IS NOT CATCHED BY THE FIRST 4 STATEMENTS
            #       WE CHECK IF THE GRID'S EDGES ARE ALL SMALLER THAN THE ITEMS MBR
            # SECOND: A LINESTRING IS INSIDE OF THE GRID BUT NONE OF ITS EDGES ARE INSIDE THIS GRID
            #       WE CHECK
            #
            # intersections check!
            if (gridArray[x][y][0] <= i[1][0][0] <= gridArray[x][y][2] and  # 1st - case
                gridArray[x][y][1] <= i[1][0][1] <= gridArray[x][y][3]) or \
                    (gridArray[x][y][2] >= i[1][1][0] >= gridArray[x][y][0] and  # 2nd - case
                     gridArray[x][y][3] >= i[1][1][1] >= gridArray[x][y][1]) or \
                    (gridArray[x][y][0] <= i[1][0][0] <= gridArray[x][y][2] and  # 3rd - case
                     gridArray[x][y][1] <= i[1][1][1] <= gridArray[x][y][3]) or \
                    (gridArray[x][y][2] >= i[1][1][0] >= gridArray[x][y][0] and  # 4th - case
                     gridArray[x][y][3] >= i[1][0][1] >= gridArray[x][y][1]) or \
                    (i[1][0][0] <= gridArray[x][y][0] and i[1][0][1] <= gridArray[x][y][1] and  # 5th - case
                     i[1][1][0] >= gridArray[x][y][2] and i[1][1][1] >= gridArray[x][y][3]) or \
                    (i[1][0][0] <= gridArray[x][y][0] and i[1][1][0] >= gridArray[x][y][2] and  # 6th - case
                     (gridArray[x][y][1] <= i[1][0][1] <= gridArray[x][y][3]
                      or gridArray[x][y][1] <= i[1][1][1] <= gridArray[x][y][3])) or \
                    (i[1][0][1] <= gridArray[x][y][1] and i[1][1][1] >= gridArray[x][y][3] and  # 7th - case
                     (gridArray[x][y][0] <= i[1][0][0] <= gridArray[x][y][2]
                      or gridArray[x][y][0] <= i[1][1][0] <= gridArray[x][y][2])):
                resultsList[x][y] += 1
                gridIntersectsWith[x][y].append(i[0])

for x in range(len(gridIntersectsWith)):
    for y in range(len(gridIntersectsWith[x])):
        if gridIntersectsWith[x][y]:
            for i in gridIntersectsWith[x][y]:
                if x == len(gridIntersectsWith) - 1 and y == len(gridIntersectsWith[x]) - 1 and i == gridIntersectsWith[x][y][-1]:
                    fpGrd.write(str(records[i - 1]).replace('[', '').replace(']', ''))
                else:
                    fpGrd.write(str(records[i - 1]).replace('[', '').replace(']', '') + "\n")
print('Grid file created successfully!')

fpDir.write(str(minX) + " ")
fpDir.write(str(maxX) + " ")
fpDir.write(str(minY) + " ")
fpDir.write(str(maxY) + "\n")

for x in range(len(resultsList)):
    for y in range(len(resultsList[x])):
        if x == len(resultsList) - 1 and y == len(resultsList[x]) - 1:
            fpDir.write(str(x) + " " + str(y) + " " + str(resultsList[x][y]))
        else:
            fpDir.write(str(x) + " " + str(y) + " " + str(resultsList[x][y]) + "\n")
print('Dir file created successfully!')
