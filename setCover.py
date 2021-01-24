#####################
#  Class for job reader data: #
#####################
class JobsReader():
    def __init__(self, file_name):
        self.name = file_name

    def readFile(self):
        try:
            numJobs = 0
            jobs = []
            file = open(self.name, "r")
            for line in file:
                line = line[0:len(line) - 1]
                jobs.append(line)
                numJobs += 1
        except:
            print("Error: can't read the file.")
            print("Please check the format or file name and run again.")
            exit(0)
        return numJobs, jobs


#####################
#  Class for candidate reader data: #
#####################
class WorkerReader():
    def __init__(self, file_name):
        self.name = file_name

    def readFile(self):
        try:
            # output list
            workers = []
            worker_i = []
            numI = 0
            file = open(self.name, "r")
            for line in file:
                # init
                worker_i = []
                name = ""
                list_of_jobs = []
                delimSpot = line.split(".")
                name = delimSpot[0]
                worker_i.append(name)
                list_of_jobs = delimSpot[1]
                list_of_jobs = list_of_jobs[1:len(list_of_jobs) - 2]
                list_of_jobs = list_of_jobs.split(",")
                worker_i.append(list_of_jobs)
                workers.append(worker_i)
                numI += 1
        except:
            print("Error: can't read the file.")
            print("Please check the format or file name and run again.")
            exit(0)
        return numI, workers


################
# method that returns the key from a dict when a value is given:   #
################
def get_key(val, dict):
    val_list = list(val)
    val_list.sort()
    for key, value in dict.items():
        value.sort()
        if val_list == value:
            return key


################
# set cover:   #
################
def set_cover(universe, subsets):
    try:
        """Find a family of subsets that covers the universal set"""
        elements = set(e for s in subsets for e in s)
        # Check the subsets cover the universe
        sorted(univers)
        sorted(elements)
        if elements != universe:
            return None
        covered = set()
        cover = []
        # Greedily add the subsets with the most uncovered points
        while covered != elements:
            subset = max(subsets, key=lambda s: len(s - covered))
            cover.append(subset)
            covered |= subset
    except:
        print("Error: problem with set cover.")
        print("Please check the formats or file names and run again.")
        exit(0)
    return cover


#####################
#  main: #
#####################
if __name__ == '__main__':
    #####################
    #  reads and fill jobs file data: #
    file_jobs = input("Enter the name of a jobs files:")
    jr = JobsReader(file_jobs)
    numJobs, jobs_arr = jr.readFile()
    #####################
    #  reads and fill candidates file data: #
    file_worker = input("Enter the name of a candidates files:")
    wr = WorkerReader(file_worker)
    numInterview, candidates_arr = wr.readFile()
    univers = set(jobs_arr)
    dict_can = {}
    subset = []
    for e in candidates_arr:
        name = e[0]
        elem = e[1]
        dict_can[name] = elem
        subset.append(set(elem))
    cover = set_cover(univers, subset)
    if cover == None:
        print("No cover.")
        exit(0)
    else:
        print("This is the cover:")
        print("The following workers selected:")
        for e in cover:
            print("Worker: " + str(get_key(e, dict_can)) + ", Jobs: " + str(e))