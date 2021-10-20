import optparse
import sys

def parse_args(description):
    parser = optparse.OptionParser(description=description)
    parser.add_option("-p", "--pref_filename", type="string", \
                      help="input file with student preferences")
    parser.add_option("-c", "--constraint_filename", type="string", \
                      help="input file with scheduling constraints")

    mandatories = ["pref_filename", "constraint_filename"]
    (opts, args) = parser.parse_args()
    for m in mandatories:
        if not opts.__dict__[m]:
            parser.print_help()
            sys.exit()
    return opts

def read_preferences(pref_filename):
    p_file = open(pref_filename, "r")
    p_data = p_file.readlines()
    p_file.close()
    num_students = p_data[0].strip().split()[1]
    student_dict = dict()
    p_data = p_data[1:]
    for row in p_data:
        row_data = row.strip().split()
        student_dict[row_data[0]] = row_data[1:]
    return student_dict

def read_constraints(constraint_filename):
    c_file = open(constraint_filename, "c")
    c_data = c_file.readlines()
    c_file.close()
    




if __name__ == "__main__":
    args = parse_args('Set up student dictionary')
    print(read_preferences(args.pref_filename))