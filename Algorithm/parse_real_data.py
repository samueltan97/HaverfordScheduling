from args import parse_args
import os
import re
from objects import TimeSlot, Room, Student, Professor, Class


def get_day_format(raw_days):
    if raw_days == "M-F":
        days = ["M", "T", "W", "Th", "F"]
        return days

    days = []
    index = 0
    while index != len(raw_days):
        current_day = raw_days[index]
        if current_day != "T":
            days.append(current_day)
        else:
            if index != len(raw_days) - 1 and raw_days[index+1] == "H":
                days.append("Th")
                index +=1
            else:
                days.append(current_day)
        index += 1

    return days


def parse_timeslots(c_data, num_class_times):
    """

    :param c_data: List[str] -> Each line fo the constraint file.
    :param num_class_times: Int -> Number of time slots to parse.
    :return: TimeSlot Objs.
    """
    timeslots = []
    for timeslot_line in range(1, 1 + num_class_times):
        timeslot_info = c_data[timeslot_line].split()
        id = timeslot_info[0]
        start_is_afternoon = timeslot_info[2] == "PM"
        if start_is_afternoon:
            start_time = int(timeslot_info[1].split(":")[0]) + 12
        else:
            start_time = int(timeslot_info[1].split(":")[0])
        end_is_afternoon = timeslot_info[4] == "PM"

        if end_is_afternoon:
            end_time = int(timeslot_info[3].split(":")[0]) + 12
        else:
            end_time = int(timeslot_info[3].split(":")[0])
        # TODO: Merge labs and normal classes.
        days = get_day_format(timeslot_info[5])
        start_times = [start_time] * len(days)
        end_times = [end_time] * len(days)

        new_slot = TimeSlot(id, days, start_times, end_times)
        timeslots.append(new_slot)

    return timeslots


def parse_rooms(c_data, num_class_times, num_rooms):
    end_room_index = num_class_times + num_rooms
    rooms = []

    for room_line in range(num_class_times + 2, end_room_index + 2):
        current_room_line = c_data[room_line]
        line_data = current_room_line.split()
        id = room_line - num_class_times - 2
        building = ""
        code = line_data[0]
        index = 0
        # seperate building and classroom
        while index < len(code) and not code[index].isnumeric():
            building += code[index]
            index += 1

        capacity = int(line_data[1])
        new_room = Room(id, building, capacity)
        rooms.append(new_room)
    return rooms


def read_preferences(pref_filename):
    """
    :param pref_filename: Str path to student pref file.
    :return: List[Student]
    """
    p_file = open(pref_filename, "r")
    p_data = p_file.readlines()
    p_file.close()
    new_students = []
    num_students = int(p_data[0].strip().split()[1])  # Currently unused
    p_data = p_data[1:]
    for row in p_data:
        row_data = row.strip().split()
        id = int(row_data[0])
        preferences = [int(class_id) for class_id in row_data[1:]]
        cur_student = Student(id, preferences)
        new_students.append(cur_student)

    assert num_students == len(new_students)

    return new_students


def parse_professors(c_data, start_line):
    """

    :param c_data: List[Str] -> list of data in constraint file, line by line.
    :param start_line: Int -> Line where professor data starts.
    :return: List[Professor]
    """

    num_of_teachers = int(c_data[start_line].split()[1])
    list_of_profs = []
    for professor_line_num in range(start_line+1, start_line+num_of_teachers+1):
        cur_line = c_data[professor_line_num]
        cur_prof_data = cur_line.split()
        prof_id = int(cur_prof_data[0])
        courses = [int(c) for c in cur_prof_data[1:]]
        new_prof = Professor(prof_id, courses)
        list_of_profs.append(new_prof)

    return list_of_profs


def parse_courses(c_data, courses_line):
    """

    :param c_data: List[str] Raw data from text file, line by line.
    :param courses_line: Int -> Starting line for the courses.
    :return: List[Class]
    """
    num_of_courses = int(c_data[courses_line].split()[1])
    courses = []
    for cur_course_line in range(courses_line+1, courses_line + num_of_courses+1):
        cur_line = c_data[cur_course_line].split()
        course_id = int(cur_line[0])
        lang = "LANG" in cur_line
        sem = "SEM" in cur_line

        cur_class = Class(id=course_id, writing_seminar=sem, language=lang)
        courses.append(cur_class)

    return courses


def read_constraints(constraint_filename):
    """

    :param constraint_filename: Str: path to constraint file.
    :return:
    """
    c_file = open(constraint_filename, "r")
    c_data = c_file.readlines()  # Read constraint file into a list of lines
    c_file.close()

    # Parse the Time slots
    num_class_times = int(c_data[0].strip().split()[2])
    assert type(num_class_times) == int
    timeslots = parse_timeslots(c_data, num_class_times)
    assert num_class_times == len(timeslots)

    # Parse the Rooms
    rooms_line = num_class_times + 1
    num_rooms = int(c_data[rooms_line].split()[1])
    assert type(num_rooms) == int
    rooms = parse_rooms(c_data, num_class_times, num_rooms)
    assert len(rooms) == num_rooms

    # Parse the Rooms
    courses_line = num_class_times + num_rooms + 2
    num_of_courses = int(c_data[courses_line].split()[1])
    courses = parse_courses(c_data, courses_line)
    assert len(courses) == num_of_courses

    # Parse the Professors
    professors_line = courses_line+num_of_courses+1
    num_of_teachers = int(c_data[professors_line].split()[1])
    professors = parse_professors(c_data, professors_line)

    assert len(professors) == num_of_teachers

    return rooms, courses, professors, timeslots


def parse_data_into_objs(constrain_file, pref_file, debug=False):
    S = read_preferences(pref_file)
    R, C, P, T = read_constraints(constraint_file)

    if debug:
        print("Rooms:")
        for room in R:
            print("\t"+str(room))

        print("Classes:")
        for course in C:
            print("\t"+str(course))

        print("Professors:")
        for prof in P:
            print("\t"+str(prof))

        print("Students:")
        for student in S:
            print("\t"+str(student))

        print("Timeslots")
        for ts in T:
            print("\t"+str(ts))
    return R, C, P, S, T


if __name__ == "__main__":
    #args = parse_args("Parse real data.")
    # constraint_file = "../data/new_constraints.txt"
    # pref_file = "../data/new_prefs.txt"
    constraint_file = "../data/constraints_S100C10T7P11R5.txt"
    pref_file = "../data/prefs_S100C10T7P11R5.txt"
    parse_data_into_objs(constraint_file, pref_file, debug=True)

