
from colors import Color

def convert_matches_to_schedule_file(matches, schedule_file):
    """
    :param matches: Dictionary of dictionaries containing rooms, timeslots, professors assigned to each class
    INCLUDING students
    :param schedule_file: path of where to create schedule file.
    :return: schedule_file
    """

    lines = ['Course\tRoom\tTeacher\tTime\tStudents']
    f = open(schedule_file, 'w')
    for key,value in matches.items():
        line = []
        line.append(str(key.id))
        line.append(str(value['room'].id))
        line.append(str(key.professor))
        line.append(str(value['timeslot'].id))
        line.append(' '.join([str(x.id) for x in value['students']]))
        lines.append('\t'.join(line))
    for x in lines:
        f.write("{}\n".format(x))
    f.close()
    return schedule_file


def matches_to_string(matches):
    """

    :param matches: Dictionary of dictionaries containing rooms, timeslots, professors assigned to each class
    INCLUDING students
    :return: str -> matches with color :).
    """

    schedule_colors = Color.BOLD+Color.UNDERLINE+Color.PINK
    end_color = Color.ENDC

    full_string = ""
    for class_obj in matches:
        room_obj = matches[class_obj]['room']
        timeslot_obj = matches[class_obj]['timeslot']
        students_list = [s.id for s in matches[class_obj]['students']]

        class_str = Color.GREEN + str(class_obj) + end_color
        room_str = Color.CYAN + str(room_obj) + end_color
        timeslot_str = Color.BLUE + str(timeslot_obj) + end_color
        students_str = Color.YELLOW + str(students_list) + end_color

        result = "{} in {} at {} with students {}".format(class_str, room_str, timeslot_str, students_str)
        full_string += schedule_colors+"Scheduled:" + end_color + " " + result
        full_string += "\n"
    return full_string