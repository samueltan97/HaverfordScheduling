import optparse
import sys
import os
import re
import time
import pathlib
import statistics
from main import class_schedule
from var_loading import load_variables_into_obj
"""
Example runs from command line:
WINDOWS: python .\test.py -p .\misc\k10r4c14t4s50\prefs_0 -c .\misc\k10r4c14t4s50\constraints_0 -s .\schedule_file.txt -f .\misc\k10r4c14t4s50\ -a
MAC: 
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

    mandatories = []
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

def read_preferences(pref_filename):
    p_file = open(pref_filename, "r")
    p_data = p_file.readlines()
    p_file.close()
    student_dict = dict()
    num_students = p_data[0].strip().split()[1]
    p_data = p_data[1:]
    for row in p_data:
        row_data = row.strip().split()
        student_dict[row_data[0]] = row_data[1:]
    return num_students, student_dict

def read_constraints(constraint_filename):
    c_file = open(constraint_filename, "r")
    c_data = c_file.readlines()
    c_file.close()
    class_dict = dict()
    num_class_times = c_data[0].strip().split()[2]
    num_rooms = c_data[1].strip().split()[1]
    end_room_index = 2+int(num_rooms)
    room_dict = dict()
    for row in c_data[2:end_room_index]:
        row_data = row.strip().split()
        room_dict[row_data[0]] = row_data[1]
    num_classes = c_data[end_room_index].strip().split()[1]
    num_teachers = c_data[end_room_index + 1].strip().split()[1]
    teacher_dict = dict()
    class_dict = dict()
    for row in c_data[end_room_index + 2:]:
        row_data = row.strip().split()
        if class_dict.get(row_data[0]) is None:
            class_dict[row_data[0]] = row_data[1]
        if teacher_dict.get(row_data[1]) is None:
            teacher_dict[row_data[1]] = {'class':[row_data[0]]}
        else:
            teacher_dict[row_data[1]]['class'].append(row_data[0])
    return num_rooms, num_classes, num_class_times, num_teachers, room_dict, class_dict, teacher_dict


def test(schedule_filename, constraint_filename, pref_filename, debug=False):
    num_students, student_dict = read_preferences(pref_filename)
    num_rooms, num_classes, num_class_times, num_teachers, room_dict, class_dict, teacher_dict = read_constraints(constraint_filename)
    
    s_file = open(schedule_filename, "r")
    s_data = s_file.readlines()
    s_file.close()
    student_dict = dict()
    if re.match(r"Course\tRoom\tTeacher\tTime\tStudents", s_data[0]) is False:
        print("Header line has incorrect format.")
        sys.exit()
    else:
        s_data = s_data[1:]
        course_room = dict()
        course_time = dict()
        course_students = dict()
        teacher_course_1 = dict()
        teacher_course_2 = dict()
        student_courses = dict()
        time_room = dict()
        student_preferences = 0
        for row in s_data:
            if re.match(r"(\d+)\t(.+)\t(\d+)\t(\d+)\t(.*)", row) is False:
                print('Content line has incorrect format.')
                sys.exit() 
            else:
                row_data = row.strip().split()
                course = row_data[0]
                room = row_data[1]
                teacher = row_data[2]
                time = row_data[3]
                students = ' '.join(row_data[4:])
                if re.match(r"(\d+ )*(\d+)?", students) is False:
                    print("Students have incorrect format.")
                    print("Students:",course)
                    sys.exit()
                else:
                    students = students.strip().split()
                    class_size = len(students)
                    if course_room.get(course) is not None:
                        print("Course", course, "defined more than once.")
                        sys.exit()

                    course_room[course] = room
                    if class_size > int(room_dict[room]):
                        print("Room", room, "is too small to hold course", course, "with", class_size, "students.")
                        sys.exit()
                    
                    if class_dict[course] != teacher:
                        print("Course", course, "does not have the correct teacher.")
                        sys.exit()

                    if teacher_course_1.get(teacher) is None:
                        teacher_course_1[teacher] = course
                    else:
                        if time == course_time[teacher_course_1[teacher]]:
                            print("Teacher", teacher, "scheduled for two courses at time", time)
                            sys.exit()
                    
                    course_time[course] = time

                    if time_room.get(time) is not None and time_room.get(time).get(room) is not None:
                        print("Multiple courses scheduled for time", time, "and room", room)
                        sys.exit()
                    else:
                        time_room[time] = dict()
                        time_room[time][room] = course
                    
                    course_students[course] = students

                    for student in students:
                        if student_courses.get(student) is not None:
                            for cour in student_courses[student]:
                                if course_time[cour] == time:
                                    print("Student", student, "assigned to time conflicting courses", cour, "and", course)
                                    sys.exit()

                            student_courses[student].add(course)
                        
                        else:
                            temp = set([course])
                            student_courses[student] = temp

                        if student_dict.get(student) is not None and course not in student_dict[student]:
                            print("student", student, "assigned to unrequested course", course)
                            sys.exit()
                    
                        student_preferences += 1

    if debug:
        print("Schedule is valid")
        print("Student preferences value:", student_preferences)
    return student_preferences


def convert_matches_to_schedule_file(matches,schedule_file):
    lines = ['Course\tRoom\tTeacher\tTime\tStudents']
    f = open(schedule_file, 'w')
    for key,value in matches.items():
        line = []
        line.append(str(key.id))
        line.append(str(value['room'].id))
        line.append(str(key.professor))
        line.append(str(value['timeslot'].id))
        if "students" in value:  # If we have students in the class
            line.append(' '.join([str(x.id) for x in value['students']]))
        lines.append('\t'.join(line))
    for x in lines:
        f.write("{}\n".format(x))
    f.close()


def evaluate_runtime_and_performance(class_schedule_function, pref_file, constraint_file, schedule_file, debug=False):
    R, C, P, S, T = load_variables_into_obj(pref_file, constraint_file)
    start_time = time.time()
    score, matches = class_schedule_function(T, S, C, R, P)
    runtime = time.time() - start_time

    if debug:
        print("--- %s seconds ---" % runtime)

    convert_matches_to_schedule_file(matches, schedule_file)
    student_pref_score = test(schedule_file, constraint_file, pref_file, debug)
    return student_pref_score, runtime


def run_all_test_cases_in_test_folder(folder_name, offset=0, debug=False):
    """
    :param folder_name: str -> folder_name containing test
    :param offset: int -> used when running on multiple folders to allow merging of results.
    :param debug: Bool -> whether or not to print
    :return: Dict[int, Tuple[int, int]] -> ditionary keyed by file index of run result.
    """
    iteration_count = int(folder_name.split('r')[0].split('k')[1])
    num_students = int(folder_name.split('s')[-1])
    results_dict = dict()
    for i in range(iteration_count):
        pref_filename = os.path.join(folder_name, "prefs_" + str(i))
        constraint_filename = os.path.join(folder_name, "constraints_" + str(i))
        schedule_filename = os.path.join(folder_name, "schedule_" + str(i))
        student_pref_score, runtime = evaluate_runtime_and_performance(class_schedule, pref_filename, constraint_filename, schedule_filename, debug)
        results_dict[i+offset] = (student_pref_score/(num_students*4), runtime)
    return results_dict


def run_all_tests(debug=False):
    """
    :param debug: Bool -> whether or not to print.
    :return: Dict[str, Tuple[int, int]] Merged dictionary of test runs.
    """

    test_dir = os.path.join("misc", "test_cases")
    indiv_test_folders = os.listdir(test_dir)
    offset = 0
    full_dict = dict()
    # all_items = []
    # indiv_test_folders.remove("k10r40c90t8s150")
    # indiv_test_folders.remove("k10r40c70t8s150")
    # indiv_test_folders.remove("k10r40c100t8s150")
    # indiv_test_folders.remove("k10r40c40t6s50")
    # indiv_test_folders.remove("k10r40c120t8s150")
    # indiv_test_folders.remove("k10r40c110t8s150")
    # indiv_test_folders.remove("k10r40c130t8s150")
    indiv_test_folders = sorted(indiv_test_folders)

    for test_folder in indiv_test_folders:
        #print(test_folder)
        full_path = os.path.join(test_dir, test_folder)
        test_case = pathlib.PurePath(full_path).name
        results = run_all_test_cases_in_test_folder(full_path, offset, debug)
        averaged_student_pref_score = statistics.mean([y[0] for x,y in results.items()])
        averaged_runtime = statistics.mean([y[1] for x,y in results.items()])
        full_dict[test_case] = ('Score: ' + str(averaged_student_pref_score), 'Runtime: ' + str(averaged_runtime))
        # offset += len(results)
        # all_items += results.items()
    # full_dict = dict(all_items)
    return full_dict


if __name__ == "__main__":
    args = parse_args('Set up student dictionary')
    # print(read_constraints(args.constraint_filename))
    # print(read_preferences(args.pref_filename))

    # print(test(args.schedule_filename, args.constraint_filename, args.pref_filename))
    # print(evaluate_runtime_and_performance(class_schedule, args.pref_filename, args.constraint_filename, args.schedule_filename))
    #print(run_all_test_cases_in_test_folder(args.folder_name))
    if args.all_tests:
        print(run_all_tests(args.debug))
    else:
        print(run_all_test_cases_in_test_folder(args.folder_name, args.debug))
