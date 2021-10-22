import numpy as np
import matplotlib as mlp
mlp.use('tkagg')
import matplotlib.pyplot as plt
import optparse
import sys
from test import run_all_test_cases_in_test_folder, run_all_tests

"""
Example code to run:

WINDOWS: python .\graph.py -a
MAC: python3 graph.py -a
"""

def parse_args(description):
    parser = optparse.OptionParser(description=description)
    parser.add_option("-p", "--pref_filename", type="string", \
                      help="input file with student preferences")
    parser.add_option("-c", "--constraint_filename", type="string", \
                      help="input file with scheduling constraints")
    parser.add_option("-s", "--schedule_filename", type="string", \
                      help="input file with proposed schedule")
    parser.add_option("-f", "--folder_name", type="string", \
                      help="input name of folder that contains all instances of a certain test case")
    parser.add_option("-a", "--all_tests",
                      action="store_true",
                      help="tells program to run all tests. ")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      help="Tells the program how much to print. ")

    mandatories = ["pref_filename", "constraint_filename","schedule_filename","folder_name"]
    (opts, args) = parser.parse_args()

    if opts.folder_name is not None:  # Make the pref, constraint files only necessary if folder not given.
        mandatories = ["folder_name"]

    if opts.all_tests:
        mandatories = []

    for m in mandatories:
        if not opts.__dict__[m]:
            parser.print_help()
            sys.exit()
    return opts

def create_graph(runtime, indp_var, indp_var_name, filename):
    degree = 4
    #coeffs = np.polyfit(indp_var,runtime, degree)
    #p = np.poly1d(coeffs)
    plt.plot(indp_var, runtime, 'or')
    #plt.plot(indp_var, [p(n) for n in indp_var], '-b')
    plt.xlabel(indp_var_name)
    plt.ylabel(filename)
    plt.title(filename + " dependent on " + indp_var_name)
    plt.ylim(bottom=0)
    plt.xlim(xmin=0)
    plt.savefig(filename)
    plt.show()

if __name__ == "__main__":
    args = parse_args('Set up student dictionary')
    # print(read_constraints(args.constraint_filename))
    # print(read_preferences(args.pref_filename))

    # print(test(args.schedule_filename, args.constraint_filename, args.pref_filename))
    # print(evaluate_runtime_and_performance(class_schedule, args.pref_filename, args.constraint_filename, args.schedule_filename))
    #print(run_all_test_cases_in_test_folder(args.folder_name))
    if args.all_tests:
        results = run_all_tests(args.debug)
        room_sizes = [200,180,160,140,120,100,80,60,40,20]
        no_timeslots = [3,4,5,6,7,9,10]
        no_students = [50,75,100,125,150,175,200,225,250,275]
        no_classrooms = [50,60,70,80,90,100,110,120,130]
        runtimes_R = []
        runtimes_T = []
        runtimes_S = []
        runtimes_C = []
        scores_R = []
        scores_T = []
        scores_S = []
        scores_C = []
        print(results)
        R = ["k10r200c42t8s150", "k10r180c42t8s150","k10r160c42t8s150","k10r140c42t8s150","k10r120c42t8s150","k10r100c42t8s150","k10r80c42t8s150","k10r60c42t8s150", "k10r40c42t8s150",
             "k10r20c42t8s150"]
        T = ["k10r40c40t3s150","k10r40c40t4s150","k10r40c40t5s150","k10r40c40t6s150","k10r40c40t7s150","k10r40c40t9s150","k10r40c40t10s150"]
        S = ["k10r40c40t6s50","k10r40c40t6s75","k10r40c40t6s100","k10r40c40t6s125","k10r40c40t6s150","k10r40c40t6s175","k10r40c40t6s200","k10r40c40t6s225","k10r40c40t6s250","k10r40c40t6s275"]
        C = ["k10r40c50t8s150","k10r40c60t8s150","k10r40c70t8s150","k10r40c80t8s150","k10r40c90t8s150","k10r40c100t8s150","k10r40c110t8s150","k10r40c120t8s150","k10r40c130t8s150"]
        for i in R:
            print(i)
            runtimes_R.append(results[i][1])
            scores_R.append(results[i][0])
        for i in T:
            print(i)
            runtimes_T.append(results[i][1])
            scores_T.append(results[i][0])

        for i in S:
            print(i)
            runtimes_S.append(results[i][1])
            scores_S.append(results[i][0])

        for i in C:
            print(i)
            runtimes_C.append(results[i][1])
            scores_C.append(results[i][0])


        create_graph(runtimes_R, room_sizes, "Rooms", 'runtime_rooms')
        create_graph(runtimes_T, no_timeslots, "Timeslots", 'runtime_timeslots')
        create_graph(runtimes_S, no_students, "Students", 'runtime_students')
        create_graph(runtimes_C, no_classrooms, "Classrooms", 'runtime_classrooms')
        create_graph(scores_R, room_sizes, "Rooms", 'scores_rooms')
        create_graph(scores_T, no_timeslots, "Timeslots", 'scores_timeslots')
        create_graph(scores_S, no_students, "Students", 'scores_students')
        create_graph(scores_C, no_classrooms, "Classrooms", 'scores_classrooms')
        #print(results)
    
