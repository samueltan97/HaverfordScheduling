import optparse
import sys
import re
from .var_loading import read_constraints, read_preferences

def parse_args(description):
    parser = optparse.OptionParser(description=description)
    parser.add_option("-p", "--pref_filename", type="string", \
                      help="input file with student preferences")
    parser.add_option("-c", "--constraint_filename", type="string", \
                      help="input file with scheduling constraints")
    parser.add_option("-s", "--schedule_filename", type="string", \
                      help="input file with proposed schedule")

    mandatories = ["pref_filename", "constraint_filename","schedule_filename"]
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


def test(schedule_filename, constraint_filename, pref_filename):
    num_students, student_dict = read_preferences(pref_filename)
    num_rooms, num_classes, num_class_times, num_teachers, room_dict, class_dict, teacher_dict = read_constraints(constraint_filename)
    
    s_file = open(schedule_filename, "r")
    s_data = s_file.readlines()
    s_file.close()
    student_dict = dict()
    header_pattern = re.compile("Course\tRoom\tTeacher\tTime\tStudents$")
    content_line_pattern = re.compile()
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

                    if class_size > room_dict[room]:
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

                    if time_room.get(time).get(room) is not None:
                        print("Multiple courses scheduled for time", time, "and room", room)
                        sys.exit()
                    else:
                        time_room[time][room] = course
                    
                    course_students[course] = students

                    for student in students:
                        if student_courses.get(student) is not None:
                            for cour in student_courses:
                                if course_time[cour] == time:
                                    print("Student", student, "assigned to time conflicting courses", cour, "and", course)
                                    sys.exit()

                            student_courses[student].append(course)
                        
                        else:
                            temp = set([course])
                            student_courses[student] = temp
                        
                        if course not in student_dict[student]:
                            print("student", student, "assigned to unrequested course", course)
                            sys.exit()
                    
                        student_preferences += 1

    print("Schedule is valid")
    print("Student preferences value:", student_preferences)

def evaluate_runtime()