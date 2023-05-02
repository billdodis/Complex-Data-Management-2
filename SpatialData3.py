def line_intersection(p1, p2, p3, p4):
    [x1, y1] = p1
    [x2, y2] = p2
    [x3, y3] = p3
    [x4, y4] = p4
    # calculate the denominator
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    # if the denominator is 0, the lines are parallel
    if denom == 0:
        return False
    # calculate the numerator for the first line
    numer1 = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    # calculate the numerator for the second line
    numer2 = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)
    # calculate the parameters t and u
    t = numer1 / denom
    u = numer2 / denom
    # if 0 <= t <= 1 and 0 <= u <= 1, the lines intersect
    if 0 <= t <= 1 and 0 <= u <= 1:
        return True
    # otherwise, the lines do not intersect
    return False


resultsList = []

with open('grid.dir', 'r') as f:
    arr = []
    line = f.readline().rstrip()
    xy = line.split(' ')
    minX = float(xy[0])
    maxX = float(xy[1])
    minY = float(xy[2])
    maxY = float(xy[3])
    counter = 0
    resultY = []
    sumOfConnections = 0
    while line:
        counter += 1
        line = f.readline().rstrip()
        if line != '':
            lineSplitted = line.split(' ')
            sumOfConnections += int(lineSplitted[2])
            if counter == 11:
                resultsList.append(resultY)
                resultY = []
                resultY.append(int(lineSplitted[2]))
                counter = 1
            else:
                resultY.append(int(lineSplitted[2]))
        else:
            resultsList.append(resultY)

records = [None] * sumOfConnections

gridArray = []
gridIntersectsWith = []
for x in range(10):
    xList = []
    gridIntersectsHelper = []
    for y in range(10):
        # ola ta y tha mpainun se mia lista kai auth h lista tha mpainei
        # sthn telikh gia na einai efikto to paw sto [0][0] ths genikhs listas
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

        gridIntersectsHelper.append([])
    gridArray.append(xList)
    gridIntersectsWith.append(gridIntersectsHelper)

with open('grid.grd', 'r') as f:
    line = True
    while line:
        found = False
        line = f.readline().rstrip()
        if line != '':
            recordList = []
            minMaxList = []
            linestringsList = []
            lineSplitted = line.split(', ')
            recordList.append(int(lineSplitted[0]))
            minMaxList.append([float(lineSplitted[1]), float(lineSplitted[2])])
            minMaxList.append([float(lineSplitted[3]), float(lineSplitted[4])])
            recordList.append(minMaxList)
            for i in range(5, len(lineSplitted), 2):
                linestring = [float(lineSplitted[i]), float(lineSplitted[i + 1])]
                linestringsList.append(linestring)
            recordList.append(linestringsList)
            records[recordList[0] - 1] = recordList
            for x in range(len(gridIntersectsWith)):
                for y in range(len(gridIntersectsWith[x])):
                    if resultsList[x][y] > 0:
                        resultsList[x][y] -= 1
                        gridIntersectsWith[x][y].append(recordList[0])
                        found = True
                        break
                if found:
                    break

records = [x for x in records if x is not None]

queriesFile = open("./queries.txt", "r")
lines = queriesFile.readlines()
queries = []
for line in lines:
    query = []
    line = line.strip()
    splittedLine = line.split(",")
    splittedLine = splittedLine[1].split(" ")
    for i in splittedLine:
        query.append(float(i))
    queries.append(query)

# !!! BE CAREFUL, QUERY's FORMAT IS Xmin, Xmax, Ymin, Ymax !!!

queriesCellsXY = [[] for i in range(len(queries))]

for i in range(len(queries)):
    for x in range(len(gridArray)):
        for y in range(len(gridArray[x])):
            # intersections check!
            if (gridArray[x][y][0] <= queries[i][0] <= gridArray[x][y][2] and  # 1st - case
                gridArray[x][y][1] <= queries[i][2] <= gridArray[x][y][3]) or \
                    (gridArray[x][y][2] >= queries[i][1] >= gridArray[x][y][0] and  # 2nd - case
                     gridArray[x][y][3] >= queries[i][3] >= gridArray[x][y][1]) or \
                    (gridArray[x][y][0] <= queries[i][0] <= gridArray[x][y][2] and  # 3rd - case
                     gridArray[x][y][1] <= queries[i][3] <= gridArray[x][y][3]) or \
                    (gridArray[x][y][2] >= queries[i][1] >= gridArray[x][y][0] and  # 4th - case
                     gridArray[x][y][3] >= queries[i][2] >= gridArray[x][y][1]) or \
                    (queries[i][0] <= gridArray[x][y][0] and queries[i][2] <= gridArray[x][y][1] and  # 5th - case
                     queries[i][1] >= gridArray[x][y][2] and queries[i][3] >= gridArray[x][y][3]) or \
                    (queries[i][0] <= gridArray[x][y][0] and queries[i][1] >= gridArray[x][y][2] and  # 6th - case
                     (gridArray[x][y][1] <= queries[i][2] <= gridArray[x][y][3]
                      or gridArray[x][y][1] <= queries[i][3] <= gridArray[x][y][3])) or \
                    (queries[i][2] <= gridArray[x][y][1] and queries[i][3] >= gridArray[x][y][3] and  # 7th - case
                     (gridArray[x][y][0] <= queries[i][0] <= gridArray[x][y][2]
                      or gridArray[x][y][0] <= queries[i][1] <= gridArray[x][y][2])):
                queriesCellsXY[i].append([x, y])

allResultsMBRs = []

for i in range(len(queries)):
    uniqueResults = []
    results = 0
    resultsMBRs = []
    coordinatesCounter = 0
    for coordinates in queriesCellsXY[i]:
        for mbr in gridIntersectsWith[coordinates[0]][coordinates[1]]:
            if (queries[i][0] <= records[mbr - 1][1][0][0] <= queries[i][1] and  # 1st - case
                queries[i][2] <= records[mbr - 1][1][0][1] <= queries[i][3]) or \
                    (queries[i][1] >= records[mbr - 1][1][1][0] >= queries[i][0] and  # 2nd - case
                     queries[i][3] >= records[mbr - 1][1][1][1] >= queries[i][2]) or \
                    (queries[i][0] <= records[mbr - 1][1][0][0] <= queries[i][1] and  # 3rd - case
                     queries[i][2] <= records[mbr - 1][1][1][1] <= queries[i][3]) or \
                    (queries[i][1] >= records[mbr - 1][1][1][0] >= queries[i][0] and  # 4th - case
                     queries[i][3] >= records[mbr - 1][1][0][1] >= queries[i][2]) or \
                    (records[mbr - 1][1][0][0] <= queries[i][0] and records[mbr - 1][1][0][1] <= queries[i][
                        2] and  # 5th - case
                     records[mbr - 1][1][1][0] >= queries[i][1] and records[mbr - 1][1][1][1] >= queries[i][3]) or \
                    (records[mbr - 1][1][0][0] <= queries[i][0] and records[mbr - 1][1][1][0] >= queries[i][
                        1] and  # 6th - case
                     (queries[i][2] <= records[mbr - 1][1][0][1] <= queries[i][3]
                      or queries[i][2] <= records[mbr - 1][1][0][1] <= queries[i][3]

                      or queries[i][2] <= records[mbr - 1][1][0][1] <= queries[i][3]
                      or queries[i][2] <= records[mbr - 1][1][1][1] <= queries[i][3]
                      or queries[i][2] <= records[mbr - 1][1][1][1] <= queries[i][3]
                      or queries[i][2] <= records[mbr - 1][1][1][1] <= queries[i][3])) or \
                    (records[mbr - 1][1][0][0] <= queries[i][0] and records[mbr - 1][1][0][1] <= queries[i][
                        2] and  # 7th - case ----
                     records[mbr - 1][1][1][0] >= queries[i][1] and records[mbr - 1][1][1][1] >= queries[i][3]) or \
                    (records[mbr - 1][1][0][1] <= queries[i][2] and records[mbr - 1][1][1][1] >= queries[i][
                        3] and  # 8th - case ----
                     (queries[i][0] <= records[mbr - 1][1][0][0] <= queries[i][1]
                      or queries[i][0] <= records[mbr - 1][1][0][0] <= queries[i][1]
                      or queries[i][0] <= records[mbr - 1][1][0][0] <= queries[i][1]
                      or queries[i][0] <= records[mbr - 1][1][1][0] <= queries[i][1]
                      or queries[i][0] <= records[mbr - 1][1][1][0] <= queries[i][1]
                      or queries[i][0] <= records[mbr - 1][1][1][0] <= queries[i][1])):
                if mbr not in uniqueResults:
                    uniqueResults.append(mbr)
                    results += 1
                    resultsMBRs.append(mbr)
        if len(gridIntersectsWith[coordinates[0]][coordinates[1]]) == 0:
            del (queriesCellsXY[i][coordinatesCounter])
        coordinatesCounter += 1
    allResultsMBRs.append(resultsMBRs)


for i in range(len(queries)):
    uniqueResults2 = []
    queryResults = []
    # line 1 coordinate1= [queries[i][0], queries[i][2]]
    # line 1 coordinate2= [queries[i][0], queries[i][3]]
    # line 2 coordinate1= [queries[i][0], queries[i][3]]
    # line 2 coordinate2= [queries[i][1], queries[i][3]]
    # line 3 coordinate1= [queries[i][1], queries[i][3]]
    # line 3 coordinate2= [queries[i][1], queries[i][2]]
    # line 4 coordinate1= [queries[i][1], queries[i][2]]
    # line 4 coordinate2= [queries[i][0], queries[i][2]]
    # queries[i][0] = Xmin OF THE WINDOW
    # queries[i][1] = Xmax OF THE WINDOW
    # queries[i][2] = Ymin OF THE WINDOW
    # queries[i][3] = Ymax OF THE WINDOW
    # LINE 1 = [xMin,yMin] -> [xMin, yMax]
    # LINE 2 = [xMin,yMax] -> [xMax, yMax]
    # LINE 3 = [xMax,yMax] -> [xMax, yMin]
    # LINE 4 = [xMax,yMin] -> [xMin, yMin]
    gridFirstLineCoordinate1 = [queries[i][0], queries[i][2]]
    gridFirstLineCoordinate2 = [queries[i][0], queries[i][3]]
    gridSecondLineCoordinate1 = [queries[i][0], queries[i][3]]
    gridSecondLineCoordinate2 = [queries[i][1], queries[i][3]]
    gridThirdLineCoordinate1 = [queries[i][1], queries[i][3]]
    gridThirdLineCoordinate2 = [queries[i][1], queries[i][2]]
    gridFourthLineCoordinate1 = [queries[i][1], queries[i][2]]
    gridFourthLineCoordinate2 = [queries[i][0], queries[i][2]]
    for coordinates in queriesCellsXY[i]:
        for mbr in allResultsMBRs[i]:

            # FIRST CHECK IF Xmin, Xmax tou mbr ENTOS TOU XMIN XMAX TOU WINDOW
            # THE SAME FOR Y SIDE.
            #  THEN LETS CHECK EVERY LINESTRING OF THE SELECTED MBRs.
            # records[mbr - 1][1][0][0] = Xmin
            # records[mbr - 1][1][1][0] = Xmax
            # records[mbr - 1][1][0][1] = Ymin
            # records[mbr - 1][1][1][1] = Ymax
            # AN EMPERIEXETAI O X H O Y AKSONAS STO WINDOW. AUTOMATA EINAI ENTOS
            if (records[mbr - 1][1][0][0] >= queries[i][0] and records[mbr - 1][1][1][0] <= queries[i][1]) or \
                    (records[mbr - 1][1][0][1] >= queries[i][2] and records[mbr - 1][1][1][1] <= queries[i][3]):
                if mbr not in uniqueResults2:
                    uniqueResults2.append(mbr)
                    queryResults.append(mbr)
            else:
                # below are the coordinates.
                # records[mbr - 1][2][coordinatesIndex][0] = X1
                # records[mbr - 1][2][coordinatesIndex][1] = Y1
                # records[mbr - 1][2][coordinatesIndex + 1][0] = X2
                # records[mbr - 1][2][coordinatesIndex + 1][1] = Y2

                # WE WILL CHECK THE LINE INTERSECTION FUNCTION WITH ALL THE 4 LINES OF THE GRID
                for coordinatesIndex in range(len(records[mbr - 1][2])):
                    if coordinatesIndex != len(records[mbr - 1][2]) - 1:
                        LineCoordinate1 = [records[mbr - 1][2][coordinatesIndex][0],
                                           records[mbr - 1][2][coordinatesIndex][1]]
                        LineCoordinate2 = [records[mbr - 1][2][coordinatesIndex + 1][0],
                                           records[mbr - 1][2][coordinatesIndex + 1][1]]
                        if line_intersection(LineCoordinate1, LineCoordinate2, gridFirstLineCoordinate1,
                                             gridFirstLineCoordinate2) \
                                or line_intersection(LineCoordinate1, LineCoordinate2, gridSecondLineCoordinate1,
                                                     gridSecondLineCoordinate2) \
                                or line_intersection(LineCoordinate1, LineCoordinate2, gridThirdLineCoordinate1,
                                                     gridThirdLineCoordinate2) \
                                or line_intersection(LineCoordinate1, LineCoordinate2, gridFourthLineCoordinate1,
                                                     gridFourthLineCoordinate2):
                            if mbr not in uniqueResults2:
                                uniqueResults2.append(mbr)
                                queryResults.append(mbr)
                                break

    print('Query No.' + str(i + 1) + ' results:')
    print(*queryResults, end='\n')
    print('Cells Searched: ' + str(len(queriesCellsXY[i])))
    print('Results Found: ' + str(len(queryResults)))
    print('----------')
