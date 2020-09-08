#!/usr/bin/python3

import sys
import struct
import argparse
import datetime


def parse_lastlog(lastlog_file, users_list, lastlog_ut_linesize, lastlog_ut_hostsize, lastlog_ut_timesize):
    ll_record_size = lastlog_ut_linesize + lastlog_ut_hostsize + lastlog_ut_timesize
    ll_unpack_definition = ""
    if lastlog_ut_timesize ==4:
        ll_unpack_definition = ll_unpack_definition + "I"
    ll_unpack_definition = ll_unpack_definition + str(lastlog_ut_linesize) + "s"
    ll_unpack_definition = ll_unpack_definition + str(lastlog_ut_hostsize) + "s"
    ll_uid_list = []
    with open(lastlog_file, 'rb') as ll_fd:
        ll_test = ll_fd.read()
        ll_rec_count = int(len(ll_test) / ll_record_size)
        ll_fd.seek(0)
        ll_records = ll_fd.read(ll_rec_count * ll_record_size)
        ll_uid = 0
        for ll_epoch_time, ll_line, ll_host in struct.iter_unpack(ll_unpack_definition, ll_records):
            if ll_epoch_time > 0:
                timestamp = datetime.datetime.fromtimestamp(ll_epoch_time)
                ll_time = timestamp.strftime('%a %b %d %H:%M:%S %Y %z')
                ll_uid_list.append(ll_uid)
                print('{} {} {} {}'.format(ll_uid, ll_time, ll_line.decode('utf-8'), ll_host.decode('utf-8')))
            ll_uid = ll_uid + 1
    print('')
    ll_get_usernames(users_list, ll_uid_list)

def ll_get_usernames(users_list, uids_list):
    for user_rec in users_list:
        for uid_rec in uids_list:
            ll_user, ll_uid = user_rec
            if str(uid_rec) == str(ll_uid):
                print(ll_uid, ll_user)

def parse_utmp_h(utmp_file):
    lastlog_ut_linesize = 32
    lastlog_ut_hostsize = 256
    fields = []
    with open(utmp_file, 'r') as ut_fd:
        for line in ut_fd:
            if "#define" in line:
                if "UT_LINESIZE" in line:
                    fields = line.split()
                    lastlog_ut_linesize = int(fields[-1])
                if "UT_HOSTSIZE" in line:
                    fields = line.split()
                    lastlog_ut_hostsize = int(fields[-1])
    return lastlog_ut_linesize, lastlog_ut_hostsize

def parse_passwd(passwd_file):
    users_list = []
    with open(passwd_file, 'r') as pw_fd:
        for line in pw_fd:
            user_pair = []
            username, trash, uid, *trash_list = line.split(':')
            user_pair.append(username)
            user_pair.append(uid)
            users_list.append(user_pair)
    return users_list

parser = argparse.ArgumentParser(
        description='Parse a Linux lastlog database.', 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Either use -u, or use -uls and -uhs.  The -uts can be used with either combination.
If -p is given, the username to UID mappings are given after the lastlog data.
This is because it is not impossible for duplicate UIDs to exist in the passwd file.''')
parser.add_argument('-f', '--file', help='The lastlog database file to be parsed.', action='store', required=True)
parser.add_argument('-u', '--utmp', help='The bits/utmp.h file that contains the record description definitions.', action='store', default="")
parser.add_argument('-p', '--passwd', help='The passwd file for converting UID to username, if desired.', action='store', default="")
parser.add_argument('-uls', '--linesize', help='The lastlog UT_LINESIZE definition.  Set this manually if no bits/utmp.h is available.', action='store', default=32, type=int)
parser.add_argument('-uhs', '--hostsize', help='The lastlog UT_HOSTSIZE definition.  Set this manually if no bits/utmp.h is available.', action='store', default=256, type=int)
parser.add_argument('-uts', '--timesize', help='The lastlog TIME size.  Default is 4 bytes, but this flag allows changing this if the target lastlog struct uses a different size.', action='store', default=4, type=int)

users_list = []

args = parser.parse_args()
if len(sys.argv) == 1:
    args.help

#Set lastlog UT_LINESIZE, UT_HOSTSIZE, and UT_TIMESIZE based on arguments settings.
lastlog_ut_linesize = args.linesize
lastlog_ut_hostsize = args.hostsize
lastlog_ut_timesize = args.timesize

#If we passed in a utmp, use the values from that to override the defaults that may have been passed by previous argument check.
if len(args.utmp) > 0:
    lastlog_ut_linesize, lastlog_ut_hostsize = parse_utmp_h(args.utmp)

#If we want to map the usernames for convenience, this should be set.
if len(args.passwd) > 0:
    users_list = parse_passwd(args.passwd)

parse_lastlog(args.file, users_list, lastlog_ut_linesize, lastlog_ut_hostsize, lastlog_ut_timesize)
