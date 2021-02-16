# todotxt-caldav
Sync todo.txt file and caldav TODO files

## Documentation

This scripts works by parsing todo.txt files with todotxtio and generating `.ics` files
to be copied in the given directory.

You can then sync this directory with an online caldav using [vdirsyncer](https://vdirsyncer.pimutils.org/en/stable/) for example.

## TODO (sic)

Who takes precedence ? how to compare ? do we add ids ? urk

For now just use todo2caldav and caldav2todo when you see fit.
