import optparse
import sys

"Sample code: python .\misc\var_loading.py -p .\misc\k10r4c14t4s50\prefs_0 -c .\misc\k10r4c14t4s50\constraints_0"
"Sample code: python ./misc/var_loading.py -p ./misc/k10r4c14t4s50/prefs_0 -c ./misc/k10r4c14t4s50/constraints_0"

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
    student_dict = dict()
    num_students = int(p_data[0].strip().split()[1])
    p_data = p_data[1:]
    for row in p_data:
        row_data = row.strip().split()
        student_dict[int(row_data[0])] = row_data[1:]
    return num_students, student_dict

def read_constraints(constraint_filename):
    c_file = open(constraint_filename, "r")
    c_data = c_file.readlines()
    c_file.close()
    class_dict = dict()
    num_class_times = int(c_data[0].strip().split()[2])
    assert type(num_class_times) == int
    num_rooms = int(c_data[1].strip().split()[1])
    assert type(num_rooms) == int
    end_room_index = 2+num_rooms
    room_dict = dict()
    for row in c_data[2:end_room_index]:
        row_data = row.strip().split()
        room_dict[int(row_data[0])] = int(row_data[1])
    num_classes = int(c_data[end_room_index].strip().split()[1])
    num_teachers = int(c_data[end_room_index + 1].strip().split()[1])
    teacher_dict = dict()
    class_dict = dict()
    for row in c_data[end_room_index + 2:]:
        row_data = row.strip().split()
        if class_dict.get(int(row_data[0])) is None:
            class_dict[int(row_data[0])] = int(row_data[1])
        if teacher_dict.get(int(row_data[1])) is None:
            teacher_dict[int(row_data[1])] = {'class':[int(row_data[0])]}
        else:
            teacher_dict[int(row_data[1])]['class'].append(int(row_data[0]))
    return num_rooms, num_classes, num_class_times, num_teachers, room_dict, class_dict, teacher_dict

if __name__ == "__main__":
    args = parse_args('Set up student dictionary')
    print(read_constraints(args.constraint_filename))
    print(read_preferences(args.pref_filename))