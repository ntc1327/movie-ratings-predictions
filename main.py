import math

# calculates the similarities between two users
def cosineSimilarity(index1, index2):
    dotProduct = 0
    total1 = total2 = 0

    # iterates through all movies for each user, gets the dot product and total for the magnitude for each user
    for i in range(1683):
        dotProduct += userList[index1].moviesList[i] * userList[index2].moviesList[i]
        if userList[index1].moviesList[i] is not 0 and userList[index2].moviesList[i] is not 0:
            total1 += userList[index1].moviesList[i] * userList[index1].moviesList[i]
            total2 += userList[index2].moviesList[i] * userList[index2].moviesList[i]

    # calculates magnitudes
    magnitude1 = math.sqrt(total1)
    magnitude2 = math.sqrt(total2)

    print(magnitude1)
    print(magnitude2)

    # if there was nothing calculated, returns lowest value for similarity
    if magnitude1 == 0.0 or magnitude2 == 0.0:
        cosSim = 0
    else:
        cosSim = dotProduct / (magnitude1 * magnitude2)

    return cosSim


# gets a list of movie ratings for the user and dataset passed in
def userRatings(userIndex, userArray):
    movieList = [0] * 1683

    for row in userArray:
        if row[0] == userIndex:
            for i in range(1683):
                if row[1] == i:
                    movieList[i] = row[2]

    return movieList


# for a given user, calculates the 5 nearest neighbors
def nearestNeighbors(userIndex):
    bestNeighbors = [0, 0, 0, 0, 0]
    bestSim1 = bestSim2 = bestSim3 = bestSim4 = bestSim5 = 0

    # iterates through all users, gets the similarity for each, then stores them as a nearest neighbor if they qualify
    for i in range(501):
        if i is not userIndex and i is not 0:
            cosSim = cosineSimilarity(userIndex, i)

            if cosSim > bestSim1:
                bestSim1 = cosSim
                bestNeighbors[0] = i
            elif cosSim > bestSim2:
                bestSim2 = cosSim
                bestNeighbors[1] = i
            elif cosSim > bestSim3:
                bestSim3 = cosSim
                bestNeighbors[2] = i
            elif cosSim > bestSim4:
                bestSim4 = cosSim
                bestNeighbors[3] = i
            elif cosSim > bestSim5:
                bestSim5 = cosSim
                bestNeighbors[4] = i

    return bestNeighbors


# given a user, the movie to predict the rating for, and the number of neighbors to use, predicts the movie's rating
def predictRating(userIndex, testMovie, numNeighbors):
    nearNeighbors = nearestNeighbors(userIndex) # gets the neighbors
    usableNeighbors = [0, 0, 0, 0, 0]
    count = 0
    simXRating = totalSim = 0

    # ensures that the neighbors being used have ratings for the movie being compared
    for i in range(5):
        if userList[nearNeighbors[i]].moviesList[testMovie] is not 0:
            usableNeighbors[i] = nearNeighbors[i]

    # for the number of neighbors to use, calculates similarity then uses that in conjunction with the user's rating to predict a rating
    for k in range(5):
        kNearestNeighbors = usableNeighbors[k]

        if kNearestNeighbors is not 0 and count is not numNeighbors:
            cosSim = cosineSimilarity(userIndex, kNearestNeighbors)
            totalSim += cosSim
            simXRating += cosSim * userList[kNearestNeighbors].moviesList[testMovie]
            count += 1

    # if there was no neighbors to use to predict a rating, sets the rating to the average of the highest and lowing ratings
    if totalSim is 0:
        return 3

    return simXRating / totalSim


# given a list of users, predicts all ratings for that list and returns that list
def fillInRatings(givenList):
    currList = [0] * 1683

    # helper function to get a list of predicted movies for the user
    def movieRatings(userIndex):
        for row in testArray:
            if row[0] == userIndex:
                for i in range(1683):
                    if row[1] == i:
                        currList[i] = predictRating(userIndex, i, 5) # manually change the 3rd variable to get different K values

        return currList

    # for the list, appends the user with a list of predicted ratings to the list being returned
    for i in range(len(givenList)):
        for j in range(1683):
            if givenList[i].moviesList[j] is not 0:
                ratingsList.append((user(i, movieRatings(i))))

    return ratingsList


# given a list to calculate for, returns the mean squared error of that list's predictions
def meanSquaredError(ratingsList):
    summation = 0

    # for all users and all movies, calculates the top and bottom parts of the MSE equation
    for i in range(len(ratingsList)):
        for j in range(1683):
            if testUserList[i].moviesList[j] is not 0:
                ave = testUserList[i].moviesList[j] - ratingsList[i].moviesList[j]
                ave = ave * ave
                summation += ave

    return summation / 2458


# K Fold cross validation method
def kFoldValidation():
    datasetSplit = list()
    foldSplit = [10, 20, 30, 40, 50]
    highestAccuracy = 100.0
    mostAccurateK = 0

    # splits the test list into 5 folds
    for i in range(5):
        for j in range(51):
            fold = list()
            while len(fold) <= foldSplit[i]:
                fold.append((user(j, userRatings(j, testArray))))
            datasetSplit.append(fold)

    # for each fold, gets the error of each fold and tests it against the lowest error to get the most accurate K value
    for i in range(5):
        currAccuracy = meanSquaredError(fillInRatings(datasetSplit[i]))
        if currAccuracy < highestAccuracy:
            highestAccuracy = currAccuracy
            mostAccurateK = i + 1

    return mostAccurateK


# simple user class that holds their IDs and their respective lists of all movies
class user:
    def __init__(self, userID, moviesList):
            self.userID = userID
            self.moviesList = moviesList


# opens and reads in base file similar to how readItem.py was implemented
file = open("u1-base.base", "r")
lines = file.readlines()

newArray = list()
userList = list()

for i in lines:
    i = i.rstrip("\n")
    i = i.split("\t")
    newArray.append(i)

# converts all data points to ints
for row in newArray:
    row[0] = int(row[0].strip())
    row[1] = int(row[1].strip())
    row[2] = int(row[2].strip())
    row[3] = int(row[3].strip())

# gets the base list's ratings
for i in range(501):
    userList.append((user(i, userRatings(i, newArray))))


# similarly reads in test file
testFile = open("u1-test.test", "r")
testLines = testFile.readlines()

testArray = list()
testUserList = list()
ratingsList = list()

for i in testLines:
    i = i.rstrip("\n")
    i = i.split("\t")
    testArray.append(i)

for row in testArray:
    row[0] = int(row[0].strip())
    row[1] = int(row[1].strip())
    row[2] = int(row[2].strip())
    row[3] = int(row[3].strip())

for i in range(501):
    testUserList.append((user(i, userRatings(i, testArray))))

print(meanSquaredError(fillInRatings(testUserList)))
