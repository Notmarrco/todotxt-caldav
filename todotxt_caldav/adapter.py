"""Adapter class between vobject.vTodo and todotxtio.Todo
"""
from datetime import datetime
import json
from todotxtio import Todo
import vobject


class VTodoAdapter(object):
    """Add new methods to Todo object to make it compatible to vobject class.

    :usage:
    o = Todo()
    o = VTodoAdapter(o)
    o.serialize()  # it uses vobject.serialize
    """

    def __init__(self, obj: Todo):
        self.obj = obj
        self._ical = None
        methods = {"serialize": lambda: self.ical.serialize()}
        self.__dict__.update(methods)

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    def original_dict(self):
        return self.obj.__dict__

    @property
    def uid(self):
        return self.ical.vtodo.uid

    @property
    def ical(self):
        """
        Create a VTodo from given object.

        https://github.com/eventable/vobject/blob/master/vobject/icalendar.py#L1175

        VTodoKnownChildren = {
        'DTSTART':        (0, 1, None),  # min, max, behaviorRegistry id
        'CLASS':          (0, 1, None),
        'COMPLETED':      (0, 1, None),
        'CREATED':        (0, 1, None),
        'DESCRIPTION':    (0, 1, None),
        'GEO':            (0, 1, None),
        'LAST-MODIFIED':  (0, 1, None),
        'LOCATION':       (0, 1, None),
        'ORGANIZER':      (0, 1, None),
        'PERCENT':        (0, 1, None),
        'PRIORITY':       (0, 1, None),
        'DTSTAMP':        (1, 1, None),
        'SEQUENCE':       (0, 1, None),
        'STATUS':         (0, 1, None),
        'SUMMARY':        (0, 1, None),
        'UID':            (0, 1, None),
        'URL':            (0, 1, None),
        'RECURRENCE-ID':  (0, 1, None),
        'DUE':            (0, 1, None),  # NOTE: Only one of Due or
        'DURATION':       (0, 1, None),  # Duration can appear
        'ATTACH':         (0, None, None),
        'ATTENDEE':       (0, None, None),
        'CATEGORIES':     (0, None, None),
        'COMMENT':        (0, None, None),
        'CONTACT':        (0, None, None),
        'EXDATE':         (0, None, None),
        'EXRULE':         (0, None, None),
        'REQUEST-STATUS': (0, None, None),
        'RELATED-TO':     (0, None, None),
        'RESOURCES':      (0, None, None),
        'RDATE':          (0, None, None),
        'RRULE':          (0, None, None),
        'VALARM':         (0, None, None)
        }
        """
        if self._ical:
            return self._ical
        cal = vobject.iCalendar()
        v = vobject.newFromBehavior("vtodo")
        creation_date = (
            self.creation_date
            if self.creation_date
            else datetime.now().strftime("%Y-%m-%d")
        )
        v.add("dtstart").value = datetime.strptime(creation_date, "%Y-%m-%d")
        v.add("dtstamp").value = datetime.strptime(creation_date, "%Y-%m-%d")
        # unused : self.completed
        if self.completion_date:
            v.add("completed").value = datetime.strptime(
                self.completion_date, "%Y-%m-%d"
            )
        elif self.completed:
            v.add("completed").value = datetime.now()
        v.add("categories").value = ",".join(self.contexts)
        v.add("priority").value = self.priority or ""
        # unused : self.projects
        # unused : self.tags, except for "due"
        if "due" in self.tags:
            v.add("due").value = datetime.strptime(self.tags.due, "%Y-%m-%d")
        v.add("summary").value = self.text or ""
        v.add("description").value = json.dumps(self.to_dict())

        cal.add(v)
        self._ical = cal
        return cal
