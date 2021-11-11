from var_loading import load_variables_into_obj
from args import parse_args
from output import *


def get_obj_by_id(obj_list, id):
    """
    :param obj_list: List[Obj]
    :param id: Int
    :return: Obj -> Return the object with corresponding id.
    """

    for obj in obj_list:
        if obj.id == id:
            return obj

    return None


def sort_classes(S,C, first_year_seminar):
    """
    :param S: List[Student]
    :param C: List[Class]
    :return: List[Class] -> C sorted by total interest.
    """

    class_interest_count = {k: 0 for k in C}

    for s in S:
        for p in s.preferences:
            course = get_obj_by_id(C, p)
            if course == None:
                print(p)
                continue
            if first_year_seminar:
            #  and p is not a first year seminar
                if course in class_interest_count and not course.writing_seminar and not course.language:
                    #CHECK IF THIS IS SUPPOSED TO INCREMENT OR SIMPLY SET TO 1
                    class_interest_count[course] += 1
                else:
                    if course.writing_seminar or course.language:
                        class_interest_count[course] = 0
                    #i  f p first year seminar, classInterestCount[p] = 0
                    else:
                        class_interest_count[course] = 1
            else:
                if course in class_interest_count:
                    class_interest_count[course] += 1
                else:
                    class_interest_count[course] = 1
    #  sort by highest interest, descending order

    sorted_class_interest_count = sorted(C, key=lambda c: class_interest_count[c], reverse=True)
    return sorted_class_interest_count, class_interest_count


def sort_class_times(T):
    """
    :param T: List[TimeSlot]
    :return: List[TimeSlot] -> sorted by potential conflicts with other time slots.
    """
    #TODO: Primary key secondary key... NOt sure if this is what this does.
    T_sorted = sorted(T, key=lambda x: x.start_times, reverse=True)
    conflict_dict = {}
    for t in T_sorted:
        T_copy  = T_sorted
        T_copy.remove(t)
        for t_1 in T_copy:
            if does_conflict(t, t_1):
                t_1.conflicts += 1
    sorted_class_times = sorted(T, key=lambda x: x.conflicts)
    for t in T:
        if t.conflicts in conflict_dict.keys():
            conflict_dict[t.conflicts].append(t)
        else:
            conflict_dict[t.conflicts] = [t]
    conflict_dict = sorted(conflict_dict.items())

    conflict_dict = [list(x) for x in conflict_dict]
    #print(conflict_dict)
    return sorted_class_times, conflict_dict


def identify_rooms_for_class(R,C, rooms_buildings):
    """
    :param R: List[Room]
    :param C: List[Class]
    :return: Dict[Class : List[Rooms] -> the rooms that each class can occupy.
    """
    rooms_for_classes = {}
    # sorted_rooms = sorted(R, key=lambda r: r.capacity, reverse=True)
    # for cur_class in C:
    #     rooms_for_classes[cur_class] = sorted_rooms
    if rooms_buildings:
        for classes in C:
            for rooms in R:
                if rooms.building_code in classes.valid_buildings():
                    if classes in rooms_for_classes.keys():
                        rooms_for_classes[classes].append(rooms)
                    else:
                        rooms_for_classes[classes] = [rooms]
    else:
        sorted_rooms = sorted(R, key=lambda r: r.capacity, reverse=True)
        for cur_class in C:
            rooms_for_classes[cur_class] = sorted_rooms
    return rooms_for_classes


def set_up_availabilty(input, sorted_class_times):
    """
    :param input: List[Obj] either rooms or professors
    :param sorted_class_times:
    :return: Dict[Obj : Dict[TimeSlot : True]] -> Initialize all professors and rooms to be available at all time slots.
    """
    availability = {}
    for r in input:
        isOpen = {}
        for t in sorted_class_times:
            isOpen[t] = True
        availability[r] = isOpen
    return availability


def does_conflict(first_slot, second_slot):
    """

    :param first_slot: Timeslot Object
    :param second_slot: Timeslot Object
    :return: Whether or not they conflict. (Assuming second slot starts after first slot.)
    """
    interval_list = [first_slot, second_slot]
    intervals_sorted = sorted(interval_list, key=lambda x:x.start_times)

    first_slot = intervals_sorted[0]
    second_slot = intervals_sorted[1]

    for index1, first_day in enumerate(first_slot.days):
        for index2, second_day in enumerate(second_slot.days):
            if first_day == second_day:
                if first_slot.end_times[index1] > second_slot.start_times[index2]:
                    return True

    return False

    # if overlapping_days != [] and first_slot.end_time > second_slot.start_time:
    #     return True
    # else:
    #     return False


def make_time_absolute(day, time):
    ordering = ["M", "T", "W", "Th", "F"]

    day_order = ordering.index(day)
    abs_time = day_order*100 + time
    return abs_time


def abs_time_for_course(course, matches, C):
    course_obj = get_obj_by_id(C, course)
    assigned_time_slot = matches[course_obj]["timeslot"]
    day = assigned_time_slot.days[0]
    time = assigned_time_slot.end_times[0]
    abs_time = make_time_absolute(day, time)

    return abs_time


def sort_student_preferences(matches, preferences, C):

    sorted_prefs = sorted(preferences, key=lambda course: abs_time_for_course(course, matches, C))
    return sorted_prefs


def interval_scheduling(matches, preferences, C, student):
    """
    :param matches: Dict[Class : Dict[str : Obj]]
    :param preferences: List[Class] the classes that some student s wishes to take.
    :return: a list of classes, representing their optimal schedule without conflicts.

    """

    scheduled = []
    scheduled_preferences = [class_id for class_id in preferences if get_obj_by_id(C, class_id) in matches]
    # sorted_preferences = sorted(scheduled_preferences, key=lambda class_id: matches[get_obj_by_id(C, class_id)]["timeslot"].end_times[0])
    sorted_preferences = sort_student_preferences(matches, scheduled_preferences, C)
    # if student.id == 3411018:
    #     raise ValueError(matches[get_obj_by_id(C, 2659)]['timeslot'].end_times)
    previous_class = None
    # error_student = student.id == 3411018
    # if error_student:
    #     print([str(matches[get_obj_by_id(C, c)]["timeslot"]) for c in sorted_preferences])
    for current_class_id in sorted_preferences:

        current_class = get_obj_by_id(C, current_class_id)
        current_time_slot = matches[current_class]["timeslot"]

        if previous_class is None:
            scheduled.append(current_class)
            previous_class = current_class

        else:
            previous_time_slot = matches[previous_class]["timeslot"]
            
            if not does_conflict(previous_time_slot, current_time_slot):
                # if student.id == 3411018 and previous_time_slot.id == '31':
                #     raise ValueError(previous_time_slot.end_times[0], current_class_id, previous_class.id)
                scheduled.append(current_class)
                previous_class = current_class
    return scheduled


def enroll_students(matches, S, R, T, C):
    """
        :param matches: Dictionary of dictionaries containing rooms, timeslots, professors assigned to each class.
        :param S: List[Student]
        :param R: List[Room]
        :param T: List[TimeSlot]
        :return: # of classes we were able to enroll students in and the updated matches dictionary that has the students enrolled in each class.
        """

    room_capacities = {}
    score = 0

    for room in R:
        room_capacities[room] = {}
        for timeslot in T:
            room_capacities[room][timeslot] = room.capacity

    for student in S:
        enrolled_classes = interval_scheduling(matches, student.preferences, C, student)

        for desired_class in enrolled_classes:  # Attempt to enroll student in each class from interval scheduling.
            room = matches[desired_class]["room"]
            timeslot = matches[desired_class]["timeslot"]

            if room_capacities[room][timeslot] > 0:  # There is still room in this class.
                score += 1
                room_capacities[room][timeslot] -= 1
                if matches[desired_class].get("students") is None:
                    matches[desired_class]["students"] = [student]
                else:
                    matches[desired_class]["students"].append(student)

    return score, matches


def enroll_students2(matches, S, R, T, C):
    """
    :param matches: Dictionary of dictionaries containing rooms, timeslots, professors assigned to each class.
    :param S: List[Student]
    :param R: List[Room]
    :param T: List[TimeSlot]
    :return: # of classes we were able to enroll students in and the updated matches dictionary that has the students enrolled in each class.
    """

    room_capacities = {}
    score = 0

    for room in R:
        room_capacities[room] = {}
        for timeslot in T:
            room_capacities[room][timeslot] = room.capacity

    sorted_students = sorted(S, key=lambda s: len(s.preferences), reverse=False)
    time_conflicts = 0
    for student in sorted_students:
        cur_schedule = []
        class_objs = [get_obj_by_id(C, c) for c in student.preferences]
        sorted_objs = sorted(class_objs, key=lambda c: matches[c]["room"].capacity, reverse=True)
        for desired_class in sorted_objs:
            room = matches[desired_class]["room"]
            timeslot = matches[desired_class]["timeslot"]
            able_to_enroll = True

            for enrolled_class in cur_schedule:
                if does_conflict(timeslot, enrolled_class["timeslot"]):
                    able_to_enroll = False
                    break

            if not able_to_enroll:
                continue

            if room_capacities[room][timeslot] > 0:
                score += 1
                room_capacities[room][timeslot] -= 1
                cur_schedule.append(matches[desired_class])
                if matches[desired_class].get("students") is None:
                    matches[desired_class]["students"] = [student]
                else:
                    matches[desired_class]["students"].append(student)

    return score, matches


def doesCorrespond(class1, class2):
    set_class_correspond = set([("MATH", "PHYS"), ("MATH", "CMSC"), ("CHEM", "BIOL"), ("COML", "ENGL"), ("HART", "ARTD")])
    check_tuple = tuple(sorted((class1, class2)))
    if check_tuple in set_class_correspond:
        return True
    else:
        return False


def class_schedule(T,S,C,R,P, pandemic=False, room_building=True, corresponding_class=True, first_year_seminar=True, prof_days = True):
    """

    :param T: List[TimeSlot]
    :param S: List[Student]
    :param C: List[Classes]
    :param R: List[Rooms]
    :param P: List[Professor]
    :return: Tuple[Int, Dict[Class : Dict[str : Obj]]] Score of the schedule + the matches it generated.
    """
    if pandemic:
        for room in R:
            room.capacity = room.capacity//3


    sorted_class, class_interest_count = sort_classes(S,C, first_year_seminar)
    sorted_class_times, conflict_dict = sort_class_times(T)
    rooms_for_classes = identify_rooms_for_class(R,C, room_building)
    room_availability = set_up_availabilty(R, sorted_class_times)
    prof_availability = set_up_availabilty(P, sorted_class_times)
    matches = {}
    for c in sorted_class:
        #  define professor
        p_objects = c.professor
        for p in p_objects:
            if len(p.assigned_classes_slot) == 2 or c.chosen_professor is not None:
                break
            if prof_days:
                for conflicts in conflict_dict:
                    #loop through each entry in conflict dict, sorted by increasing number of conflicts
                    valid_timeslots = []
                    if c in matches.keys():
                        break
                    for t in conflicts[1]:
                        overlap = False
                        if corresponding_class:
                            for classes, timeslots in matches.items():
                                if doesCorrespond(c.department, classes.department) and does_conflict(timeslots["timeslot"],t):
                                    overlap = True
                        #only valid when prof is available and no overlapping time slot
                        if prof_availability[p][t] == True and overlap == False:
                            valid_timeslots.append(t)

                    if len(valid_timeslots) > 0:
                        #check each valid timeslot, and see if professors already teach on that day and try and schedule a timeslot which fits that day
                        if p.assigned_classes_slot:
                            for time in valid_timeslots:
                                current_assigned_days = set()
                                for slot in p.assigned_classes_slot:
                                    for day in slot.days:
                                        current_assigned_days.add(day)
                                if len(set(time.days) & current_assigned_days)>0:
                                    for r in rooms_for_classes[c]:
                                        if room_availability[r][time] == True:
                                            matches[c] = {"timeslot": time, "room": r}
                                            room_availability[r][time] = False
                                            prof_availability[p][time] = False
                                            c.chosen_professor = p
                                            p.assigned_classes_slot.append(time)
                                            # TODO: Confused what # of students refers to pseudocode. Also, This line is broken.
                                            print(time.conflicts)
                                            print(conflict_dict[time.conflicts][1])
                                            conflict_dict[time.conflicts][1].remove(time)

                                            time.conflicts *= min(r.capacity, class_interest_count[c])
                                            conflict_dict[time.conflicts][1].append(time)
                                            break


                                    break
                        #case in which professors don't have assigned class yet, or no valid timeslots with overlapping days
                        match_class(matches, rooms_for_classes, room_availability, prof_availability, class_interest_count, c, valid_timeslots[0],
                                    p)


            else:
                for t in sorted_class_times:
                    overlap = False
                    print('here', type(c), type(p))
                    if corresponding_class:
                        for classes, timeslots in matches.items():
                            if doesCorrespond(c.department,classes.department) and does_conflict(timeslots[t], t):
                                overlap=True
                    if c in matches.keys():
                        break
                    elif prof_availability[p][t] == True and overlap == False:
                        for r in rooms_for_classes[c]:
                            if room_availability[r][t] == True:
                                matches[c] = {"timeslot": t, "room": r}
                                room_availability[r][t] = False
                                prof_availability[p][t] = False
                                c.chosen_professor = p
                                # TODO: Confused what # of students refers to pseudocode. Also, This line is broken.
                                t.conflicts *= min(r.capacity, class_interest_count[c])
                                # t.conflicts *= r.capacity
                                #  time conflicts
                                break
            sorted_class_times = sorted(sorted_class_times, key=lambda x: x.conflicts)


            # for t in sorted_class_times:
            #     overlap = False
            #     print('here', type(c), type(p))
            #     for classes, timeslots in matches.items():
            #         if doesCorrespond(c.department,classes.department) and does_conflict(timeslots[t], t):
            #             overlap=True
            #     if c in matches.keys():
            #         break
            #     elif prof_availability[p][t] == True and overlap == False:
            #         for r in rooms_for_classes[c]:
            #             if room_availability[r][t] == True:
            #                 matches[c] = {"timeslot": t, "room": r}
            #                 room_availability[r][t] = False
            #                 prof_availability[p][t] = False
            #                 c.chosen_professor = p
            #                 p.assigned_classes_slot.append(t)
            #                 # TODO: Confused what # of students refers to pseudocode. Also, This line is broken.
            #                 t.conflicts *= min(r.capacity, class_interest_count[c])
            #                 #t.conflicts *= r.capacity
            #                 #  time conflicts
            #                 break

        sorted_class_times = sorted(sorted_class_times, key=lambda x: x.conflicts)
        
    score, matches = enroll_students2(matches, S, R, T, C)
    return score, matches


def match_class(matches, rooms_for_classes, room_availability,prof_availability, class_interest_count, c,t,p):
    for r in rooms_for_classes[c]:
        if room_availability[r][t] == True:
            matches[c] = {"timeslot": t, "room": r}
            room_availability[r][t] = False
            prof_availability[p][t] = False
            c.chosen_professor = p
            p.assigned_classes_slot.append(t)
            # TODO: Confused what # of students refers to pseudocode. Also, This line is broken.

            t.conflicts *= min(r.capacity, class_interest_count[c])

            break

if __name__ == "__main__":
    """
    example run: python main.py -p /misc/test_cases/k10r4c14t4s50/prefs_0 -c /misc/test_cases/k10r4c14t4s50/constraints_0
    python main.py -p misc/test_cases/k10r20c42t8s150/prefs_0 -c misc/test_cases/k10r20c42t8s150/constraints_0
    """

    args = parse_args('Set up student dictionary')

    R, C, P, S, T = load_variables_into_obj(args.pref_filename, args.constraint_filename)
    score, matches = class_schedule(T, S, C, R, P)
    file = (matches, "schedule_file.txt")
    str_matches = matches_to_string(matches)
    print(str_matches)
    print("Wrote to file: "+file)


