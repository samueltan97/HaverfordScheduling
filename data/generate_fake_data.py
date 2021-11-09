import optparse
import sys
import random


def parse_args(description):
    parser = optparse.OptionParser(description=description)
    parser.add_option("-s", "--num_of_students", type="int", \
                      help="# of students")

    parser.add_option("-c", "--num_of_courses", type="int", \
                      help="# of courses")

    parser.add_option("-t", "--num_of_timeslots", type="int", \
                      help="# of timeslots")

    parser.add_option("-p", "--num_of_professors", type="int",
                      help="# of professors")

    parser.add_option("-r", "--num_of_rooms", type="int",
                      help="# of rooms")


    mandatories = ["num_of_students", "num_of_courses", "num_of_timeslots", "num_of_professors", "num_of_rooms"]
    (opts, args) = parser.parse_args()
    for m in mandatories:
        if not opts.__dict__[m]:
            parser.print_help()
            sys.exit()
    return opts


def generate_file_name(args):
    filename = "S{}C{}T{}P{}R{}.txt".format(args.num_of_students, args.num_of_courses,
                                        args.num_of_timeslots, args.num_of_professors,
                                        args.num_of_rooms)

    return filename


def write_class_times(num_of_timeslots, output_file):

    with open("timeslots.txt", "r") as timeslots_file:
        lines = timeslots_file.readlines()[1:num_of_timeslots+1]
        possible_slots = [" ".join(l.split()[1:]) for l in lines]


    with open(output_file, "w") as output:

        header = "Class Times \t" + str(num_of_timeslots) + "\n"
        output.write(header)

        for i in range(1, num_of_timeslots+1):
            new_line = str(i) + "\t" + possible_slots[i-1] + "\n"
            output.write(new_line)


def write_rooms(num_of_rooms, output_file):
    fake_buildings = ["A", "B", "C", "D", "E"]
    smallest_room_size = 10
    largest_room_size = 100

    with open(output_file, "a") as output:

        header = "Rooms \t" + str(num_of_rooms) + "\n"
        output.write(header)

        for i in range(1, num_of_rooms+1):
            random_building = random.choice(fake_buildings)
            random_room_num = random.randrange(100, 399)
            random_room = random_building+str(random_room_num)
            random_capacity = random.randrange(smallest_room_size, largest_room_size)

            line = random_room + "\t" + str(random_capacity) + "\n"
            output.write(line)


def write_classes(num_of_classes, output_file):
    percent_seminars = 0.05
    percent_language = 0.05

    with open(output_file, "a") as output:
        header = "Classes \t" + str(num_of_classes) + "\n"
        output.write(header)

        for i in range(0, num_of_classes):
            cur_line = str(i) + "\t"
            r_value = random.uniform(0, 1)
            is_seminar = r_value < percent_seminars
            is_language = percent_seminars < r_value < percent_language+percent_seminars

            if is_seminar:
                cur_line += "SEM"
            if is_language:
                cur_line += "LANG"

            cur_line += "\n"
            output.write(cur_line)


def write_professors(num_of_professors, num_of_courses, output_file):

    with open(output_file, "a") as output:
        header = "Teachers \t" + str(num_of_professors) + "\n"
        output.write(header)
        shuffled_courses = range(num_of_courses)
        random.shuffle(shuffled_courses)
        offset = 0

        for i in range(0, num_of_professors):
            cur_line = str(i) + "\t"
            if i == num_of_courses:
                offset += 1
            course = shuffled_courses[i-offset*num_of_courses]
            cur_line += str(course) + "\n"

            output.write(cur_line)


def write_student_prefs(num_of_courses, num_of_students, output_file):
    min_num_classes = 3
    max_num_classes = 5

    with open(output_file, "w") as output:
        header = "Students \t" + str(num_of_students) + "\n"
        output.write(header)

        for student in range(num_of_students):
            num_courses = random.randrange(min_num_classes, max_num_classes+1)
            courses = random.sample(range(num_of_courses), num_courses)
            cur_line = str(student) + "\t" + " ".join([str(c) for c in courses]) + "\n"
            output.write(cur_line)


if __name__ == "__main__":

    """
    Example run:
    python generate_fake_data.py -s 100 -c 10 -t 7 -p 11 -r 5
    """
    args = parse_args('Set up student dictionary')

    # We are assuming that we get at least one professor for each course for random data.
    assert args.num_of_professors >= args.num_of_courses

    constraints_file = "constraints_"+generate_file_name(args)
    write_class_times(args.num_of_timeslots, constraints_file)
    write_rooms(args.num_of_rooms, constraints_file)
    write_classes(args.num_of_courses, constraints_file)
    write_professors(args.num_of_professors, args.num_of_courses, constraints_file)

    prefs_file = "prefs_"+generate_file_name(args)
    write_student_prefs(args.num_of_courses, args.num_of_students, prefs_file)