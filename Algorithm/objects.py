
class Class:
    def __init__(self, id, professor, writing_seminar=False, language=False):
        self.id = id
        self.professor = professor
        self.writing_seminar = writing_seminar
        self.language = language

    def copy(self):
        return self.__init__(self.id, self.professor, self.writing_seminar, self.language)

    def __str__(self):
        return "(Class: {}, " \
            "Professor: {}, " \
            "WritingSem: {}, " \
            "Lang: {})".format(self.id, self.professor, self.writing_seminar, self.language)


class TimeSlot:
    def __init__(self, id, days, start_time, end_time, conflicts = 0):
        self.id = id
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.conflicts = conflicts

    def __str__(self):
        return "(TimeSlot:{} {}:{}-{})".format(self.id, self.days, self.start_time, self.end_time)


class Room:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

    def __str__(self):
        return "(Room:{}, capacity: {})".format(self.id, self.capacity)


class Student:
    def __init__(self, id, preferences):
        self.id = id
        self.preferences = preferences  # A list of class objects.

    def __str__(self):
        return "(Student:{}, preferences: {})".format(self.id, self.preferences)


class Professor:
    def __init__(self, id, classes):
        self.id = id
        self.classes = classes

    def __str__(self):
        return "(Professor:{}, classes: {})".format(self.id, self.classes)
