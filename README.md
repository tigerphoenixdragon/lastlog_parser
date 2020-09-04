# lastlog_parser

usage: last_log_parser.py [-h] -f FILE [-u UTMP] [-p PASSWD] [-uls LINESIZE] [-uhs HOSTSIZE] [-uts TIMESIZE]

Parse a Linux lastlog database.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The lastlog database file to be parsed.
  -u UTMP, --utmp UTMP  The bits/utmp.h file that contains the record description definitions.
  -p PASSWD, --passwd PASSWD
                        The passwd file for converting UID to username, if desired.
  -uls LINESIZE, --linesize LINESIZE
                        The lastlog UT_LINESIZE definition. Set this manually if no bits/utmp.h is available.
  -uhs HOSTSIZE, --hostsize HOSTSIZE
                        The lastlog UT_HOSTSIZE definition. Set this manually if no bits/utmp.h is available.
  -uts TIMESIZE, --timesize TIMESIZE
                        The lastlog TIME size. Default is 4 bytes, but this flag allows changing this if the target lastlog struct uses a different size.

Either use -u, or use -uls and -uhs.  The -uts can be used with either combination.
If -p is given, the username to UID mappings are given after the lastlog data.
This is because it is not impossible for duplicate UIDs to exist in the passwd file.
