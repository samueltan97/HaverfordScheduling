#!/usr/bin/python

import csv
import sys
import os


def get_data_list_of_dicts(filename):
  list = []
  with open(filename) as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
      list.append(row)
  return list

def get_room_sizes(list_of_dicts):
  room_sizes_dict = {}
  for dict in list_of_dicts:
    room = dict["Facil ID 1"]
    status = dict["Status"]
    course = dict["Course ID"]
    campus = dict["Catalog"][0]
    if status == "E" and campus == "B" and not room == "":
      if room in room_sizes_dict:
        if course in room_sizes_dict[room]:
          room_sizes_dict[room][course] = room_sizes_dict[room][course] + 1
        else:
          room_sizes_dict[room][course] = 1
      else:
        room_sizes_dict[room] = {}
        room_sizes_dict[room][course] = 1

  room_capacities = {}
  for room in room_sizes_dict:
    capacity = 0
    for course in room_sizes_dict[room]:
      if room_sizes_dict[room][course] > capacity:
        capacity = room_sizes_dict[room][course]
    room_capacities[room] = capacity
  return room_capacities

def get_student_prefs_enrolled(list_of_dicts):
  student_prefs = {}
  for dict in list_of_dicts:
    student = dict["Student ID"]
    course = dict["Course ID"]
    status = dict["Status"]
    room = dict["Facil ID 1"]
    if status == "E" and room != "":
      if student in student_prefs:
        student_prefs[student].append(course)
      else:
        student_prefs[student] = [course]
  return student_prefs

def get_courses(list_of_dicts):
  courses = {}
  for dict in list_of_dicts:
    course = dict["Course ID"]
    prof = dict["Instructor ID"]
    campus = dict["Catalog"][0]
    room = dict["Facil ID 1"]
    if not course in courses and campus == "B" and room !="" and prof != '#Value!':
      courses[course] = dict
  return courses

def get_building(list_of_dicts):
  building = {}
  for dict in list_of_dicts:
    subject = dict["Subject"]
    room = dict["Facil ID 1"]
    if room == None or room == "":
      continue
    if subject in building:
        building[subject].append(room)
    else:
        building[subject] = [room]
  return building

# Issue: didn't handle the case where a course number is corresponded to multiple courses.
def get_subject_level(list_of_dicts):
    subject_level = {}
    for dict in list_of_dicts:
        course = dict["Course ID"]
        department = dict["Subject"]
        campus = dict["Catalog"][0]
        level = dict["Catalog"][1]
        if not course in subject_level and campus == "B":
            subject_level[course] = (department,level)
    return subject_level

def get_prof_courses(list_of_dicts):
  profs = {}
  for dict in list_of_dicts:
    prof = dict["Instructor ID"]
    course = dict["Course ID"]
    campus = dict["Catalog"][0]
    if not prof == "" and campus == "B" and prof != "#Value!":
      if prof in profs:
        if not course in profs[prof]:
          profs[prof].append(course)
      else:
        profs[prof] = [course]
  return profs

def get_class_times(list_of_dicts):
  times = []
  for dict in list_of_dicts:
    start = dict["Srt1 AM/PM"]
    end = dict["End 1 AMPM"]
    days = dict["Days 1"]
    class_time = (start, end, days)
    campus = dict["Catalog"][0]
    if not class_time in times and campus == "B" and not start == "" \
        and not end == "" and not days == "":
      times.append(class_time)
  return times

# One possibility for how to find out which labs go with which courses.
# Currently catches some "labs" that aren't actually labs for those courses.
# Course '333' seems especially to be a strange corner case.
# The issue may also be that this doesn't take sections into account in matching.
#def get_lab_courses(list_of_dicts):
#  lab_courses = {}
#  student_courses = get_student_prefs_enrolled(list_of_dicts)
#  courses = get_courses(list_of_dicts)
#  for dict in list_of_dicts:
#    course = dict["Course ID"]
#    dept = dict["Subject"]
#    level = dict["Level"]
#    student = dict["Student"]
#    units = dict["Unit Taken"]
#    campus = dict["College"]
#    if units == "0" and campus == "H":  # we think this is a lab class
#      all_courses = student_courses[student]
#      for enrolled_course in all_courses:
#        if not enrolled_course == course and enrolled_course in courses:
#          course_dict = courses[enrolled_course]
#          enrolled_dept = course_dict["Subject"]
#          enrolled_level = course_dict["Level"]
#          enrolled_units = course_dict["Unit Taken"]
#          enrolled_campus = course_dict["College"]
#          if enrolled_units > 0 and enrolled_dept == dept and enrolled_level == level \
#              and enrolled_campus == campus:
#            print enrolled_course + " " + course
#            if enrolled_course in lab_courses:
#              if not course in lab_courses[enrolled_course]:
#                lab_courses[enrolled_course].append(course)
#            else:
#              lab_courses[enrolled_course] = [course]
#  return lab_courses

def write_building_to_file(list_of_dicts, filename):
    building = get_building(list_of_dicts)
    f = open(filename, 'w')
    f.write("Building\t" + str(len(building)) + "\n")
    for subject in building:
        towrite = subject + "\t"
        for room in building[subject]:
            towrite = towrite + room + " "
        towrite = towrite + "\n"
        f.write(towrite)

def write_prefs_to_file(list_of_dicts, filename, unique_courses):
  student_prefs = get_student_prefs_enrolled(list_of_dicts)
  f = open(filename, 'w')
  f.write("Students\t" + str(len(student_prefs)) + "\n")
  for student in student_prefs:
    towrite = student + "\t"
    for course in student_prefs[student]:
      if course in unique_courses:
        towrite = towrite + course + " "
    towrite = towrite + "\n"
    f.write(towrite)

def write_class_times_to_file(list_of_dicts, f):
  class_times = get_class_times(list_of_dicts)
  f.write("Class Times\t" + str(len(class_times)) + "\n")
  i = 1
  for (start, end, days) in class_times:
    f.write(str(i) + "\t" + start + " " + end + " " + days + "\n")
    i = i + 1

def write_rooms_to_file(list_of_dicts, f):
  room_capacities = get_room_sizes(list_of_dicts)
  f.write("Rooms\t" + str(len(room_capacities)) + "\n")
  for room in room_capacities:
    f.write(room + "\t" + str(room_capacities[room]) + "\n")

def write_num_classes_to_file(list_of_dicts, f):
  num_classes = len(get_courses(list_of_dicts))
  f.write("Classes\t" + str(num_classes) + "\n")


def write_teachers_to_file(list_of_dicts, f):
  prof_courses = get_prof_courses(list_of_dicts)
  num_profs = len(prof_courses)
  courses = get_courses(list_of_dicts)
  subject_level = get_subject_level(list_of_dicts)
  building = get_building(list_of_dicts)

  f.write("Teachers\t" + str(num_profs) + "\n")
  for prof_id in prof_courses:
    courses_prof_teaches = prof_courses[prof_id]
    cur_line = prof_id + "\t"
    cur_line += " ".join(courses_prof_teaches) + "\n"
    f.write(cur_line)

  # for course in courses:
  #   #print(course)
  #   f.write(course + "\t")
  #   f.write(courses[course]["Instructor ID"] + "\t")
  #   f.write(subject_level[course][0] + "\t")
  #   for b in building[subject_level[course][0]]:
  #       f.write(b + "\t")
  #   f.write("\n")


def write_classes_to_file(list_of_dicts, f):
  courses_dict = get_courses(list_of_dicts)

  unique_courses = {}
  language = ["FREN", "SPAN", "GERM", "GREK", "HEBR", "RUSS", "ITAL", "CNSE", "JAPN", "LATN"]

  for course_id in courses_dict:
    course = courses_dict[course_id]
    if course_id not in unique_courses:
      unique_courses[course_id] = {}
      unique_courses[course_id]["labels"] = []
      cur_subject = course["Subject"]

      unique_courses[course_id]["level"] = courses_dict[course_id]["Catalog"][1] + '00'
      unique_courses[course_id]["department"] = cur_subject
      if cur_subject == "CSEM":
        unique_courses[course_id]["labels"].append("SEM")

      if cur_subject in language and "Elementary" in course["Crs Descr"]:
        unique_courses[course_id]["labels"].append("LANG")

  for course in unique_courses:
    to_write = course + "\t"
    to_write += unique_courses[course]["department"] + "\t"
    to_write += unique_courses[course]["level"] + "\t"
    labels = " ".join(unique_courses[course]["labels"])
    to_write += labels + "\n"
    f.write(to_write)
  return unique_courses

def write_constraints_to_file(list_of_dicts, filename):
  f = open(filename, 'w')
  write_class_times_to_file(list_of_dicts, f)
  write_rooms_to_file(list_of_dicts, f)
  write_num_classes_to_file(list_of_dicts, f)
  unique_courses = write_classes_to_file(list_of_dicts, f)
  write_teachers_to_file(list_of_dicts, f)
  f.close()
  return unique_courses

def unique_buildings_for_subject(list_of_dicts):
  rooms_dict = get_building(list_of_dicts)
  new_dict = {}
  for subj in rooms_dict:

    unique_buildings = []
    for room in rooms_dict[subj]:
      building = ""
      index = 0
      # seperate building and classroom
      while index < len(room) and not room[index].isdigit():
        building += room[index]
        index += 1
      if building not in unique_buildings:
        unique_buildings.append(building)
    new_dict[subj] = unique_buildings

  return new_dict

def merge_dictionaries(dict1, dict2):
  for key in dict2:
    if key not in dict1:
      dict1[key] = dict2[key]
    else:
      dict1[key] = list(set(dict1[key] + dict2[key]))
  return dict1

def generate_unique_buildings_for_subject(enrollment_path):
  import json

  enrollment_files = [os.path.join(enrollment_path, file) for file in os.listdir(enrollment_path)]
  dicts = [get_data_list_of_dicts(file) for file in enrollment_files]
  building_dicts = [unique_buildings_for_subject(d) for d in dicts]
  final_dict = building_dicts[0]
  for other_dict in building_dicts[1:]:
    final_dict = merge_dictionaries(final_dict, other_dict)

  with open("valid_buildings.json", "w") as output:
    json.dump(final_dict, output, indent=4)


# p = "enrollment_files"
# generate_unique_buildings_for_subject(p)

if ".csv" not in sys.argv[1]:
  enrollment_path = sys.argv[1]
  enrollment_files = [os.path.join(enrollment_path, file) for file in os.listdir(enrollment_path)]
  dicts = [get_data_list_of_dicts(file) for file in enrollment_files]
  for index, d in enumerate(dicts):
    output_dir = "parsed_data"
    label = os.path.basename(enrollment_files[index].split(".")[0])
    test_dir = os.path.join(output_dir, label)
    if not os.path.exists(test_dir):
      os.makedirs(test_dir)

    pref_file = os.path.join(test_dir, "prefs.txt")
    constraint_file = os.path.join(test_dir, "constraints.txt")
    unique_courses = write_constraints_to_file(d, constraint_file)
    write_prefs_to_file(d, pref_file, unique_courses)


else:
  if len(sys.argv) != 4:
    print("Usage: " + sys.argv[0] + " <enrollment.csv> <student_prefs.txt> <constraints.txt>")
    exit(1)
  print(list_of_dicts)
  list_of_dicts = get_data_list_of_dicts(sys.argv[1])
  write_prefs_to_file(list_of_dicts, sys.argv[2])
  write_constraints_to_file(list_of_dicts, sys.argv[3])
