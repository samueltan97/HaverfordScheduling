
class Class:
    def __init__(self, id, professor, writing_seminar=False, language=False):
        self.id = id
        self.professor = professor
        self.writing_seminar = writing_seminar
        self.language = language

    def copy(self):
        return self.__init__(self.id, self.professor, self.writing_seminar, self.language)


class TimeSlot:
    def __init__(self, id, days, start_time, end_time, conflicts = 0):
        self.id = id
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.conflicts = conflicts

    def __str__(self):
        return f"({self.id}) {self.days}:{self.start_time}-{self.end_time}"


class Room:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity


class Student:
    def __init__(self, id, preferences):
        self.id = id
        self.preferences = preferences # A list of class objects.


class Professor:
    def __init__(self, id, classes):
        self.id = id
        self.classes = classes
