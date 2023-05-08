#** ***********************************************************
#    @file virtualmem.py
#    @author Snow Tempest
#    @date Nov 22, 2022
#    @brief  Virtual "Virtual Memory" simulation program. Accepts an input file and 4 numbers given as number of frames given to each process.

# This algorithm is based on 4 processes with given page frame sizes. LRU is use for cache hits and misses.

#Compiler: None
#Company: Me

# How to run: python prog4.py INPUTFILE CAPACITY1 CAPACITY2 CAPACITY3 CAPACITY4
# Notes: Hit Rate = number of times a value is found already in the process / total number of hits
#*************************************************************** **/

import sys
global CAPACITIES
global FILE
global JOBS

#Process class.
class Process: 
    def __init__(self,  hitCount, jobTotal, numFrames):
        self.hitCount = hitCount
        self.jobTotal = jobTotal
        self.numFrames = numFrames
        self.FRAMES = []

    def __str__(self): 
        return "Frame Size: %s" % (self.numFrames)
    
#Job Class. Includes the Process number for the job and the page frame number the job is referencing.
class Job:
    def __init__(self,  processNum, pageFrameNum):
        self.processNum = processNum
        self.pageFrameNum = pageFrameNum
    
    def __str__(self): 
        return "Required Process: %d, Page Frame Number: %d" % (self.processNum, self.pageFrameNum)

def main():
    global CAPACITIES
    global FILE
    global JOBS

    CAPACITIES = []
    i = 0
    

    if (len(sys.argv) < 6):
        print("Not enough arguments given.")
        print("USAGE: INPUTFILE CAPACITY1 CAPACITY2 CAPACITY3 CAPACITY4")
    elif (len(sys.argv) > 6):
        print("Too many arguments entered.")
        print("USAGE: INPUTFILE CAPACITY1 CAPACITY2 CAPACITY3 CAPACITY4")

    FILE = sys.argv[1]    
    
    while i < len(sys.argv):
        if i > 1:
            CAPACITIES.append(int(sys.argv[i]))
        i = i + 1

        
    getJobs()

    print("P1        P2        P3        P4        PAVG") 

    LRU()

# Create the 4 processes and go through all of the jobs to determine the hit rate for the processes.
def LRU():

    index = 0
    ProcessList = []
    process1 = Process(0,0,CAPACITIES[0])
    process2 = Process(0,0,CAPACITIES[1])
    process3 = Process(0,0,CAPACITIES[2])
    process4 = Process(0,0,CAPACITIES[3])

    ProcessList.append(process1)
    ProcessList.append(process2)
    ProcessList.append(process3)
    ProcessList.append(process4)

    while (index < len(JOBS)):
        currentJob = Job(JOBS[index].processNum, JOBS[index].pageFrameNum)
        
        if currentJob.processNum == 1:
             
            pageFrameJob(currentJob, ProcessList[0])

        elif currentJob.processNum == 2:

            pageFrameJob(currentJob, ProcessList[1])

        elif currentJob.processNum == 3:

            pageFrameJob(currentJob, ProcessList[2])

        elif currentJob.processNum == 4:

           pageFrameJob(currentJob, ProcessList[3])
            
        index = index + 1

    p1Results = (process1.hitCount / process1.jobTotal) * 100
    p2Results = (process2.hitCount / process2.jobTotal) * 100
    p3Results = (process3.hitCount / process3.jobTotal) * 100
    p4Results = (process4.hitCount / process4.jobTotal) * 100
    pResults =  (p1Results + p2Results + p3Results + p4Results) / 4
    print("%.2f%%    %.2f%%    %.2f%%    %.2f%%    %.2f%%" % (p1Results, p2Results, p3Results, p4Results, pResults))

# Get all the Jobs from the given input file. Stores them in the global value.
def getJobs():
    global JOBS
    JOBS = []

    with open (FILE, 'r') as f:
        for line in f:
            parse = line.split(" ")
            parse[1] = parse[1].strip()
            job = Job(int(parse[0]),int(parse[1]))
            JOBS.append(job)
    
    f.close()


#Uses the actual LRU algorithm. Given a current job from the list of all jobs and the equivalent process.
def pageFrameJob(current, process):
     
        if (current.pageFrameNum not in process.FRAMES) and (len(process.FRAMES) < process.numFrames):

            process.FRAMES.append(current.pageFrameNum)
           
        elif (current.pageFrameNum not in process.FRAMES) and (len(process.FRAMES) == process.numFrames):
                    
            process.FRAMES.pop(0)
            process.FRAMES.append(current.pageFrameNum)

        elif (current.pageFrameNum in process.FRAMES):

            pageIndex = process.FRAMES.index(current.pageFrameNum)

            page = process.FRAMES.pop(pageIndex)

            process.FRAMES.append(page)
            process.hitCount = process.hitCount + 1

        process.jobTotal = process.jobTotal + 1

#Prints the array.
def printArray(array):
    for item in array:
        print (item)

main()