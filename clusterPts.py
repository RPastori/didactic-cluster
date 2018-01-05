'''
Ronald Pastori
12/02/17
'''

import random
import sys

def usage( message ):
    print( message, file = sys.stderr )

# Calculate the Euclidian distance between two three dimensional points
dist = lambda a, b: ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)**(.5)

# Generates a dataset of an n-number of random three dimensional points
def generate(n):
    rtn = []
    for i in range(n):
        pt = (random.randint(-100, 100), # I chose the range arbitrarily
              random.randint(-100, 100), # It will still work with a different
              random.randint(-100, 100)) # range, but the variance distance will
        rtn.append(pt) # change
    return rtn

def generateToFile(n):
    with open("dataset.txt", "w") as o:
        for i in range(n):
            o.write(str(random.randint(-100, 100)) + " " +
                    str(random.randint(-100, 100)) + " " +
                    str(random.randint(-100, 100)) + " " +
                    "\n")
    return "dataset.txt"

def generateToFile(n, filename):
    with open(filename, "w") as o:
        for i in range(n):
            o.write(str(random.randint(-100, 100)) + " " +
                    str(random.randint(-100, 100)) + " " +
                    str(random.randint(-100, 100)) + " " +
                    "\n")
    return filename

def parseFile(filename):
    rtn = []
    with open(filename) as f:
        content = f.readlines()
    for line in content:
        nums = line.split()
        for i in range(len(nums)):
            nums[i] = int(nums[i])
        rtn.append(tuple(nums))
    return rtn

def openFirstArg(arg):
    try:
        dataset = parseFile(arg)
        return dataset
    except:
        return "File could not be opened"

# This function assigns each point in a given dataset to its nearest centroid
# and returns the clusters in the form of a dictionary
def assignCentroids(centroids, dataset):
    rtn = {}
    for c in centroids: # Initialize return value
        rtn[c] = []

    for p in dataset:
        idx = 0 # Keeps track of the point with the shortest distance
        currDist = dist(p, centroids[idx]) # Initialize distance
        for i in range(1, len(centroids)):
            if currDist > dist(p, centroids[i]):
                idx = i
                currDist = dist(p, centroids[idx])
        rtn[centroids[idx]].append(p)
    return rtn

def findClusterAvgs(centroids, cluster):
        avgs = {} # Now that we have the points, let's find each cluster's avg
        for c in centroids: # From the current center
            avX = 0
            avY = 0
            avZ = 0
            points = cluster[c]
            for p in points:
                avX += p[0]
                avY += p[1]
                avZ += p[2]
            avgs[c] = (avX//len(points), avY//len(points), avZ//len(points))
        return avgs


# Clustering algorithm that also highlights outliers
def cleanOutliers(centroid, points, outliers):
    distances = []
    for p in points:
        distances.append(dist(centroid, p))

    avg = sum(distances)/len(points)
    # Now that we have the average, let's find the furthest points
    differences = []
    for d in distances:
        differences.append(abs(avg - d))

    olList = []
    # Now, for the removal
    for i in range(outliers):
        olList.append(points[differences.index(max(differences))])
        points.remove(points[differences.index(max(differences))])

    return points, olList

# Uses k-clustering method
def kCluster(ds, k):

    centroids = generate(k) # Gets k random starting points
    cluster = assignCentroids(centroids, ds) # Initial clustering
    avgs = findClusterAvgs(centroids, cluster)

    newCluster = {}
    while cluster != newCluster:

        tempCluster = {}
        for i in range(len(centroids)):
            c = centroids[i]
            tempCluster[avgs[c]] = cluster[c]
            centroids[i] = avgs[c]

        newCluster = tempCluster

        cluster = assignCentroids(centroids, ds)
        avgs = findClusterAvgs(centroids, cluster)

    # Now that we have our finalized centroids, it's time to purge the outliers
    outlierTgt = int(0.1*len(ds)) # ~10% of dataset will be declared as outliers
    olPerClust = outlierTgt//k # Number of outliers from each cluster

    olCluster = {}
    for i in range(len(centroids)):
        newPts, olList = cleanOutliers(centroids[i], cluster[centroids[i]], olPerClust)
        cluster[centroids[i]] = newPts
        olCluster[centroids[i]] = olList

    return cluster, olCluster

def main():
    if len(sys.argv) == 2:
        if int(sys.argv[1]) == 500: # I'll change this later
            dataset = generate(int(sys.argv[1]))
        #elif type(sys.argv[1] == str):
        #    dataset = openFirstArg(sys.argv[1])
    elif len(sys.argv) == 1:
        usage("No argument given.\n")
        usage("Please enter the number of data points you want"
              + "or a filename of a dataset.")
        return 1
    else:
        usage("Too many arguments given.\n")
        usage("Please enter the number of data points you want"
              + "or a filename of a dataset.")
        return 1

    if type(dataset) == str:
        usage(dataset) # File could not be opened.
        return 1

    k = 6 # I may add something to get k value from user later

    cluster, outliers = kCluster(dataset, k)

    for c in cluster:
        print()
        print("Centroid:", c)
        print()
        print("Points:", cluster[c])
        print()
        print("Outliers:", outliers[c])

main()
