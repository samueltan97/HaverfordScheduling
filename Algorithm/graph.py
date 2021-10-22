import numpy as np
import matplotlib.pyplot as plt
from test import run_all_test_cases_in_test_folder, run_all_tests

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

def create_graph(runtime, indp_var):
    degree = 4
    coeffs = np.polyfit(indp_var,runtime, degree)
    p = np.poly1d(coeffs)
    plt.plot(indp_var, runtime, 'or')
    plt.plot(indp_var, [p(n) for n in indp_var], '-b')

    plt.xlabel(indp_var)
    plt.ylabel("Runtime (seconds)")

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
    
    