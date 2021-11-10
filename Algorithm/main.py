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


def sort_classes(S,C):
    """
    :param S: List[Student]
    :param C: List[Class]
    :return: List[Class] -> C sorted by total interest.
    """

    class_interest_count = {k.id:0 for k in C}
    #print(class_interest_count)
    for s in S:
        for p in s.preferences:
            course = get_obj_by_id(C, p)
            #  and p is not a first year seminar
            if course in class_interest_count.keys() and not course.writing_seminar and not course.language:
                #CHECK IF THIS IS SUPPOSED TO INCREMENT OR SIMPLY SET TO 1
                class_interest_count[p] += 1
            else:
                if course.writing_seminar and course.language:
                    class_interest_count[course] = 0
                #i  f p first year seminar, classInterestCount[p] = 0
                else:
                    class_interest_count[course] = 1
    #  sort by highest interest, descending order
    # print([str(c) for c in C])
    # print(class_interest_count)
    sorted_class_interest_count = sorted(C, key=lambda c: class_interest_count[c.id], reverse=True)
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
    return sorted_class_times, conflict_dict


def identify_rooms_for_class(R,C):
    """
    :param R: List[Room]
    :param C: List[Class]
    :return: Dict[Class : List[Rooms] -> the rooms that each class can occupy.
    """
    rooms_for_classes = {}
    # sorted_rooms = sorted(R, key=lambda r: r.capacity, reverse=True)
    # for cur_class in C:
    #     rooms_for_classes[cur_class] = sorted_rooms

    for classes in C:
        for rooms in R:
            if rooms.building_code in classes.valid_buildings():
                if classes in rooms_for_classes.keys():
                    rooms_for_classes[classes].append(rooms)
                else:
                    rooms_for_classes[classes] = [rooms]
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
    overlapping_days = list(set(first_slot.days) & set(second_slot.days))
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


def interval_scheduling(matches, preferences, C, student):
    """
    :param matches: Dict[Class : Dict[str : Obj]]
    :param preferences: List[Class] the classes that some student s wishes to take.
    :return: a list of classes, representing their optimal schedule without conflicts.

    """

    scheduled = []
    test = [matches[get_obj_by_id(C, x)]["timeslot"].end_times for x in preferences]
    sorted_preferences = sorted(preferences, key=lambda class_id: matches[get_obj_by_id(C, class_id)]["timeslot"].end_times[0])
    if student.id == 3452561:
                    raise ValueError(matches[get_obj_by_id(C, 2659)]['timeslot'].end_times)
    previous_class = None
    
    for current_class_id in sorted_preferences:
        current_class = get_obj_by_id(C, current_class_id)
        current_time_slot = matches[current_class]["timeslot"]

        if previous_class is None:
            scheduled.append(current_class)
            previous_class = current_class

        else:
            previous_time_slot = matches[previous_class]["timeslot"]
            
            if not does_conflict(previous_time_slot, current_time_slot):
                if student.id == 3452561 and previous_time_slot.id == '13':
                    raise ValueError(previous_time_slot.end_times[0], current_class_id, previous_class.id)
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

def doesCorrespond(class1, class2):
    set_class_correspond = set([("MATH", "PHYS"), ("MATH", "CMSC"), ("CHEM", "BIOL"), ("COML", "ENGL"), ("HART", "ARTD")])
    check_tuple = tuple(sorted((class1, class2)))
    if check_tuple in set_class_correspond:
        return True
    else:
        return False


def class_schedule(T,S,C,R,P, pandemic=False):
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


    sorted_class, class_interest_count = sort_classes(S,C)
    sorted_class_times, conflict_dict = sort_class_times(T)
    rooms_for_classes = identify_rooms_for_class(R,C)
    room_availability = set_up_availabilty(R, sorted_class_times)
    prof_availability = set_up_availabilty(P, sorted_class_times)
    matches = {}
    for c in sorted_class:
        #  define professor
        p_objects = c.professor
        for p in p_objects:
            if len(p.assigned_classes) == 2 or c.chosen_professor is not None:
                break
            for conflicts in conflict_dict:
                #loop through each entry in conflict dict, sorted by increasing number of conflicts
                valid_timeslots = []
                if c in matches.keys():
                    break
                for t in conflicts:
                    overlap = False
                    print('here', type(c), type(p))
                    for classes, timeslots in matches.items():
                        if doesCorrespond(c.department, classes.department) and does_conflict(timeslots[t], t):
                            overlap = True
                    #only valid when prof is available and no overlapping time slot
                    if prof_availability[p][t] == True and overlap == False:
                        valid_timeslots.append(t)

                if valid_timeslots:
                    #check each valid timeslot, and see if professors already teach on that day and try and schedule a timeslot which fits that day
                    if p.assigned_classes:
                        for time in valid_timeslots:
                            if p.assigned_classes_slot.days == time.days:
                                match_class(rooms_for_classes, room_availability, prof_availability, class_interest_count, c, time, p)
                                break
                    #case in which professors don't have assigned class yet, or no valid timeslots with overlapping days
                    match_class(rooms_for_classes, room_availability, prof_availability, class_interest_count, c, valid_timeslots[0],
                                p)

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
        
    score, matches = enroll_students(matches, S, R, T, C)
    return score, matches

def match_class(rooms_for_classes, room_availability,prof_availability, class_interest_count, c,t,p):
    for r in rooms_for_classes[c]:
        if room_availability[r][t] == True:
            matches[c] = {"timeslot": t, "room": r}
            room_availability[r][t] = False
            prof_availability[p][t] = False
            c.chosen_professor = p
            p.assigned_classes_slot.append(t)
            # TODO: Confused what # of students refers to pseudocode. Also, This line is broken.
            t.conflicts *= min(r.capacity, class_interest_count[c])
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


