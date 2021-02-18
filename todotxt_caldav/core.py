#!env python
"""Main script.

Usage:
  todo2caldav run <todo_file> <caldav_dest_dir>
"""

from commandopt import Command, commandopt
from docopt import docopt
from pathlib import Path
import todotxtio

from todotxt_caldav import __version__
from todotxt_caldav.adapter import VTodoAdapter


@commandopt(["run", "<todo_file>", "<caldav_dest_dir>"])
def t2c(arguments: dict):
    """Transform todo.txt file in multiple caldav .ics files.
    
    :todo: vtodo uid is not consistent from a run to another, so if this script
           is played more than once it re-creates every vtodo hence doubling
           the number of .ics.
    :todo: find a way to create a persistent uid from Todo to be able to keep
           track of existing mapping Todo <-> vtodo
    """
    todo_file = Path(arguments["<todo_file>"])
    caldav_dest_dir = Path(arguments["<caldav_dest_dir>"])
    if not caldav_dest_dir.exists:
        raise Exception(f"Directory {caldav_dest_dir} must exist.")
    todos = todotxtio.from_file(todo_file)
    for todo in todos:
        todo = VTodoAdapter(todo)
        todo_str = todo.serialize()  # We have to serialize _before_ asking for uid
        vtodo_filename = caldav_dest_dir.joinpath(f"t2c-{todo.uid.value}.ics")
        with open(vtodo_filename, "w") as f:
            f.write(todo_str)


def main():
    arguments = docopt(__doc__, version=__version__)
    Command(arguments, call=True)


if __name__ == "__main__":
    main()
