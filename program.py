# Nili Alfia 314880873
# Noy Israeli 208577692

import numpy as np
import pulp as pp
from collections import defaultdict
import itertools


#####################
#  a function to calculate the personal cost of a worker: #
#####################
def attributesPersonalCosts(attributes, weight):
    sum = 0
    for k in range(len(attributes)):
        sum += attributes[k] * weight[k]
    avg = sum / len(attributes)
    return avg


#####################
#  a function to calculate the professional cost of a worker: #
#####################
def attributesProCosts(attributes, weight, seniority, sen_w):
    sum = 0
    for k in range(len(attributes)):
        sum += attributes[k] * weight[k]
    sum += seniority * sen_w
    avg = sum / len(attributes) + 1
    return avg


#####################
#  Class for job reader data: #
#####################
class JobsReader():
    def __init__(self, file_name):
        self.name = file_name

    def readFile(self):
        numJobs = 0
        jobs = []
        job_i = []
        try:
            file = open(self.name, "r")
        except FileNotFoundError:
            print("File not found. Please try again.")
            return "not_found", None, None
        for line in file:
            try:
                job_i = []
                delimSpot = line.split(".")
                name = delimSpot[0]
                job_i.append(name)
                hours = int(delimSpot[1])
                job_i.append(hours)
                seniority = int(delimSpot[2])
                job_i.append(seniority)
                jobs.append(job_i)
                numJobs += 1
            except:
                print("Error at line: " + str(numJobs+1))
                print("File format is incorrect.")
                print("Please check your jobs file format and run again.")
                exit(0)
        return "successful", numJobs, jobs


#####################
#  Class for candidate reader data: #
#####################
class WorkerReader():
    def __init__(self, file_name):
        self.name = file_name

    def readFile(self):
        # output list
        workers = []
        worker_i = []
        numI = 0
        try:
            file = open(self.name, "r")
        except :
            print("File not found. Please try again.")
            return "not_found", None, None
        for line in file:
            try:
                # init
                worker_i = []
                job_name = ""
                seniority = 0
                personal = []
                professional = []
                payment = 0
                hours = 0
                gender = ""
                handicapped = ""
                versatile = ""
                delimSpot = line.split(".")
                name = delimSpot[0]
                worker_i.append(name)
                job_name = delimSpot[1]
                worker_i.append(job_name)
                seniority = delimSpot[2]
                worker_i.append(int(seniority))
                personal = delimSpot[3]
                personal = personal[1:len(personal) - 1]
                personal = np.fromstring(personal, dtype=int, sep=',')
                worker_i.append(personal)
                pro = delimSpot[4]
                pro = pro[1:len(pro) - 1]
                pro = np.fromstring(pro, dtype=int, sep=',')
                worker_i.append(pro)
                payment = delimSpot[5]
                worker_i.append(int(payment))
                hours = delimSpot[6]
                worker_i.append(int(hours))
                gender = delimSpot[7]
                worker_i.append(gender)
                handicapped = delimSpot[8]
                worker_i.append(handicapped)
                versatile = delimSpot[9]
                versatile = versatile[0:len(versatile) - 1]
                worker_i.append(versatile)
                workers.append(worker_i)
                numI += 1
            except:
                print("Error at line: " + str(numI+1))
                print("File format is incorrect.")
                print("Please check your candidates file format and run again.")
                exit(0)
        return "successful", numI, workers


#####################
#  jobsBuilder: a function that reads the jobs file and check for errors #
#####################
def jobsBuilder():
    print("please enter a path for a jobs file, with the following structure:")
    print("1. The file most be a text file.")
    print("2. format:")
    print("JOB_NAME.REQUIRED_HOURS.REQUIRED_SENIORITY")
    print("3. Must end with enter.")
    print("4. For example: CEO.500.10")
    not_read = 1
    while not_read:
        print("Enter now: ")
        file_jobs = input()
        jr = JobsReader(file_jobs)
        answer, numJobs, jobs_arr = jr.readFile()
        if answer != "not_found":
            not_read = 0
    #####################
    #  two dictionaries: seniority of the jobs, hours per project#
    S_j = {}
    H_j = {}
    for k in range(len(jobs_arr)):
        job = jobs_arr[k]
        jobName = str(job[0])
        if job[1] < 0:
            print("Error: hours element is not in the correct format.")
            print("Please check your jobs file format and run again.")
            exit(0)
        else:
            H_j[jobName] = job[1]
        if job[2] < 0:
            print("Error: seniority element is not in the correct format.")
            print("Please check your jobs file format and run again.")
            exit(0)
        else:
            S_j[jobName] = job[2]
    return H_j, S_j, jobs_arr, numJobs


#####################
#  candidatesBuilder: a function that reads the candidates file and check for errors #
#####################
def candidatesBuilder():
    print("please enter a path for a candidates file, with the following structure:")
    print("1. The file most be a text file.")
    print("2. format:")
    print("NAME.JOB_NAME.SENIORITY_AT_THIS_JOB.{LIST_OF_PERSONAL_ATTRIBUTES}.{"
          "LIST_OF_PROFESSIONAL_ATTRIBUTES}.REQUIRED_SALARY.HOUR.GENDER.HANDICAPPED_OR_NOT.VERSATILE_OR_NOT")
    print("3. Must end with enter.")
    print("4. For example: Bob.CEO.20.{1,2,4,1,3,1}.{6,1,3,3,4}.150.800.m.not_handicapped.v")
    print("Note: for the attributes - the more the number is bigger, it means that the candidate is less fit.")
    not_read = 1
    while not_read:
        print("Enter file name: ")
        file_worker = input()
        wr = WorkerReader(file_worker)
        answer, numInterview, candidates_arr = wr.readFile()
        if answer != "not_found":
            print("Please enter also a number between 11-110, an integer.")
            print("The number will represent the sum of acceptance threshold of the attributes.")
            print("For example: if these are the attributes: {1,5,2,1,7,1}.{3,2,6,4,6} you must enter a number bigger "
                  "then 38.")
            print("If you will enter 110, you can accept each worker, and if you enter 11 you can't accept anyone.")
            threshold = input("enter threshold: ")
            try:
                threshold = int(threshold)
                if 11 <= threshold <= 110:
                    not_read = 0
                else:
                    print("Please try again. enter file name and threshold.")
            except:
                print("Please try again. enter file name and threshold.")
    return numInterview, candidates_arr, threshold

#####################
#  main: #
#####################
if __name__ == '__main__':
    print("Welcome to Optimal Team Builder System.")
    print("Please follow the instructions.")
    H_j, S_j, jobs_arr, numJobs = jobsBuilder()
    #####################
    print("Now, please enter the following information:")
    #  inputs from user: #
    print("Please enter the general expenses for day.")
    print("Please enter an integer number.")
    print("If you will enter a non-integer, the system will request you to try again.")
    not_read = 1
    while not_read:
        gExpenses = input()
        try:
            gExpenses = int(gExpenses)
            if gExpenses < 0:
                print("Please try again.")
            else:
                not_read = 0
        except:
            print("Please try again.")
    not_read = 1
    print("Please enter the amount of extra hours payment.")
    print("For example: for 25% more for each extra hour, please enter 1.25.")
    while not_read:
        extraHPayment = input()
        try:
            extraHPayment = float(extraHPayment)
            if extraHPayment < 0:
                print("Please try again.")
            else:
                not_read = 0
        except:
            print("Please try again.")
    print("Now please enter the 'cost' for each personal and professional attribute of the candidates.")
    print("The more the number is bigger, the attribute is more important for you.")
    print("The numbers must be at range of 1-10 and integers. If not, the system will request you to try again.")
    print("Personal attributes:")
    team = 0
    selfLearn = 0
    loyal = 0
    passion = 0
    persistence = 0
    adaptability = 0
    analytic = 0
    creative = 0
    planning = 0
    communication = 0
    problemsolve = 0
    # team player
    not_read = 1
    while not_read:
        team = input("team player: ")
        try:
            team = int(team)
            if 1 <= team <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # self learning
    not_read = 1
    while not_read:
        selfLearn = input("self learning: ")
        try:
            selfLearn = int(selfLearn)
            if 1 <= selfLearn <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # loyalty
    not_read = 1
    while not_read:
        loyal = input("loyalty: ")
        try:
            loyal = int(loyal)
            if 1 <= loyal <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # passionate
    not_read = 1
    while not_read:
        passion = input("passionate:")
        try:
            passion = int(passion)
            if 1 <= passion <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # persistence
    not_read = 1
    while not_read:
        persistence = input("persistence: ")
        try:
            persistence = int(persistence)
            if 1 <= persistence <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # adaptability
    not_read = 1
    while not_read:
        adaptability = input("adaptability: ")
        try:
            adaptability = int(adaptability)
            if 1 <= adaptability <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    print("Professional attributes:")
    # analytic
    not_read = 1
    while not_read:
        analytic = input("analytic: ")
        try:
            analytic = int(analytic)
            if 1 <= analytic <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # creative
    not_read = 1
    while not_read:
        creative = input("creative: ")
        try:
            creative = int(creative)
            if 1 <= creative <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # planning
    not_read = 1
    while not_read:
        planning = input("planning: ")
        try:
            planning = int(planning)
            if 1 <= planning <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # communication
    not_read = 1
    while not_read:
        communication = input("communication: ")
        try:
            communication = int(communication)
            if 1 <= communication <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    # problem solving
    not_read = 1
    while not_read:
        problemsolve = input("problem solving: ")
        try:
            problemsolve = int(problemsolve)
            if 1 <= problemsolve <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    ############
    print("Now select the importance of the seniority of the candidates.")
    not_read = 1
    while not_read:
        seniority_w = input()
        try:
            seniority_w = int(seniority_w)
            if 1 <= seniority_w <= 10:
                not_read = 0
            else:
                print("Please try again.")
        except:
            print("Please try again.")
    personal_weight = [team, selfLearn, loyal, passion, persistence, adaptability]
    pro_weight = [analytic, creative, planning, communication, problemsolve]
    print("Now please choose the cost of each objective.")
    print("The more the number is bigger, the objective is more important for you.")
    print("The target is to minimize the objective function, and to minimize each category.")
    print("The sum of the costs should be 10. If not, the system will request you to try again.")
    not_read = 1
    while not_read:
        cost_f1 = input("minimal payment cost: ")
        try:
            cost_f1 = float(cost_f1)
        except:
            print("Please try again.")
            continue
        cost_f2 = input("minimal personal cost: ")
        try:
            cost_f2 = float(cost_f2)
        except:
            print("Please try again.")
            continue
        cost_f3 = input("minimal professional cost: ")
        try:
            cost_f3 = float(cost_f3)
        except:
            print("Please try again.")
            continue
        if cost_f1 + cost_f2 + cost_f3 != 10:
            print("Please try again.")
        else:
            not_read = 0
    #####################
    #  reads and fill candidates file data: #
    numInterview, candidates_arr, threshold = candidatesBuilder()
    #####################
    #  three dictionaries: payment per hour, hours per day, attribute: per candidate#
    R_i = {}
    H_i = {}
    personal_w_i = {}
    professional_w_i = {}
    sum_attributes_i = {}
    isCandidate_ij = defaultdict(dict)
    S_ij = defaultdict(dict)
    isPro_ij = defaultdict(dict)
    payment_ij = defaultdict(dict)
    gender_i = {}
    handicapped_i = {}
    versatile_i = {}
    # initialization
    for k in range(numInterview):
        for j in jobs_arr:
            candidate = candidates_arr[k]
            candidateName = str(candidate[0])
            for j in jobs_arr:
                position = j[0]
                isCandidate_ij[candidateName][position] = 0
                S_ij[candidateName][position] = -1
                isPro_ij[candidateName][position] = 0
                payment_ij[candidateName][position] = 0
    # fill
    num_of_females = 0
    for k in range(numInterview):
        candidate = candidates_arr[k]
        candidateName = str(candidate[0])
        jobName = str(candidate[1])
        for j in jobs_arr:
            position = j[0]
            if position == jobName:
                isCandidate_ij[candidateName][position] = 1
            else:
                isCandidate_ij[candidateName][position] = 0
        for j in jobs_arr:
            position = j[0]
            if position == jobName:
                if candidate[2] < 0:
                    print("Error: seniority element is not in the correct format.")
                    print("Please check your candidates file format and run again.")
                    exit(0)
                else:
                    S_ij[candidateName][position] = candidate[2]
            else:
                S_ij[candidateName][position] = -1
            # isPro_ij fill
            if S_ij[candidateName][position] - S_j[position] >= 0:
                isPro_ij[candidateName][position] = 1
            else:
                isPro_ij[candidateName][position] = 0
        # end of fill
        personal = candidate[3]
        personal_w_i[candidateName] = attributesPersonalCosts(personal, personal_weight)
        professional = candidate[4]
        professional_w_i[candidateName] = attributesProCosts(professional, pro_weight,
                                                             S_ij[candidateName][jobName], seniority_w)
        sum_attributes_i[candidateName] = sum(personal) + sum(professional)
        if candidate[5] < 0:
            print("Error: revenue element is not in the correct format.")
            print("Please check your candidates file format and run again.")
            exit(0)
        else:
            R_i[candidateName] = candidate[5]
        if candidate[6] < 0:
            print("Error: hours element is not in the correct format.")
            print("Please check your candidates file format and run again.")
            exit(0)
        else:
            H_i[candidateName] = min(candidate[6], H_j[jobName])
        g = candidate[7]
        if g == "f":
            gender_i[candidateName] = 1
            num_of_females += 1
        elif g == "m":
            gender_i[candidateName] = 0
        else:
            print("Error: gender element is not in the correct format.")
            print("Please check your candidates file format and run again.")
            exit(0)
        h = candidate[8]
        if h == "handicapped":
            handicapped_i[candidateName] = 1
        elif h == "not_handicapped":
            handicapped_i[candidateName] = 0
        else:
            print("Error: handicapped element is not in the correct format.")
            print("Please check your candidates file format and run again.")
            exit(0)
        v = candidate[9]
        if v == "v":
            versatile_i[candidateName] = 1
        elif v == "nv":
            versatile_i[candidateName] = 0
        else:
            print("Error: versatile element is not in the correct format.")
            print("Please check your candidates file format and run again.")
            exit(0)
    handicapped_scholarship = 1
    for i in range(numInterview):
        candidate = candidates_arr[i]
        cn = str(candidate[0])
        jn = str(candidate[1])
        if handicapped_i[cn] == 1:
            handicapped_scholarship = 0.85
        else:
            handicapped_scholarship = 1
        for j in jobs_arr:
            position = j[0]
            if position == jn:
                regular = H_i[cn] * R_i[cn] * handicapped_scholarship
                add = (H_j[position] - H_i[cn]) * R_i[cn] * handicapped_scholarship * extraHPayment
                payment_ij[cn][position] = regular + add
    #####################
    #  create problem: #
    prob = pp.LpProblem("optimal team problem", pp.LpMinimize)
    #####################
    #  create indices: #
    job_inds = []
    for j in jobs_arr:
        job_inds.append(j[0])
    worker_inds = []
    for i in candidates_arr:
        worker_inds.append(i[0])
    matrix_inds = list(itertools.product(worker_inds, job_inds))
    #####################
    # create decision variables: #
    #  isJob_ij: #
    isJob_ij = pp.LpVariable.dicts('isJob_ij', matrix_inds, lowBound=0, upBound=1, cat=pp.LpBinary)
    #####################
    # fill another dictionaries: #
    allPay_i = {}
    for i in candidates_arr:
        sum = 0
        for j in jobs_arr:
            job_idx = j[0]
            can_idx = i[0]
            sum += isJob_ij[(can_idx, job_idx)] * payment_ij[can_idx][job_idx]
        allPay_i[can_idx] = sum
    #######################
    # create constraints: #
    #  1: a candidate can't work at a job he isn't a candidate for#
    #  2: a candidate can work only if his seniority fits the job #
    for i, j in matrix_inds:
        prob += pp.LpConstraint(e=isJob_ij[(i, j)] - isCandidate_ij[i][j], sense=-1, rhs=0)
        prob += pp.LpConstraint(e=isJob_ij[(i, j)] - isPro_ij[i][j], sense=-1, rhs=0)
    #  3: sum of the expenses for the project can't acceded the limit gExpenses #
    prob += pp.lpSum(allPay_i[i] for i in worker_inds) <= gExpenses
    #  4: a candidate can work only in one job he applied to #
    for i in worker_inds:
        prob += pp.lpSum(isJob_ij[(i, j)] for j in job_inds) <= 1
    #  5: all the jobs need to be staffed #
    for j in job_inds:
        prob += pp.lpSum(isJob_ij[(i, j)] for i in worker_inds) == 1
    #  6: number of jobs needs to be as the number of workers #
    prob += pp.lpSum(isJob_ij[(i, j)] for i in worker_inds for j in job_inds) == numJobs
    #  7: minimum percent of females #
    f_percent = int(0.25 * numJobs)
    prob += pp.lpSum(isJob_ij[(i, j)] * gender_i[i] for i in worker_inds for j in job_inds) >= f_percent
    #  8: minimum percent of versatile workers #
    v_percent = int(0.2 * numJobs)
    prob += pp.lpSum(isJob_ij[(i, j)] * versatile_i[i] for i in worker_inds for j in job_inds) >= v_percent
    #  9: a candidate's sum of attributes must not accede the threshold #
    for i in worker_inds:
        prob += pp.lpSum(isJob_ij[(i, j)]*sum_attributes_i[i] for j in job_inds) <= threshold
    #####################
    # create objective: #
    prob += cost_f1 * pp.lpSum(allPay_i[i] for i in worker_inds) + cost_f2 * pp.lpSum(personal_w_i[i] * isJob_ij[(i, j)]
                                                                                      for i in worker_inds for j in
                                                                                      job_inds) + cost_f3 * pp.lpSum(
        professional_w_i[i] * isJob_ij[(i, j)] for i in worker_inds for j in job_inds)
    #####################
    # solve: #
    prob.solve()
    # The status of the solution is printed to the screen
    print("This is the solution:")
    if pp.LpStatus[prob.status] != "Optimal":
        print("Error, fails to meet all constraints.")
        print("Please start again.")
        print("Check your files and your parameters.")
    else:
        # The optimised objective function value is printed to the screen
        print("Optimal solution found!")
        print("This is the minimal cost of the objective that meets all the constraints:")
        print("Total Costs = ", pp.value(prob.objective))
        money = 0
        for i, j in itertools.product(worker_inds, job_inds):
            if isJob_ij[(i, j)].varValue > 0:
                money += payment_ij[i][j]
        print("Total payment: " + str(money))
        print("The following workers were selected: ")
        for i, j in itertools.product(worker_inds, job_inds):
            if isJob_ij[(i, j)].varValue > 0:
                print(i + ": " + j)
