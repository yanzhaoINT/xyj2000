#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import *
from ..common import Tintin
from ..common import logger


def check_room(conn, zone, room, desc, exits):
    room = fixup_room(room)
    if room in room_alias:
        return room_alias[room], None

    # sql = "select roomno,abbr from mud_room where roomname = '%s'" % (room)
    # rows = conn.execute(sql).fetchall()
    # if len(rows) == 1:
    #     return rows[0][0], rows[0][1]

    # sql = "select roomno,abbr from mud_room where roomname = '%s' and zone = '%s'" % (
    #     room, zone)
    # rows = conn.execute(sql).fetchall()
    # if len(rows) == 1:
    #     return rows[0][0], rows[0][1]

    # sql = "select roomno,abbr from mud_room where roomname = '%s' and description = '%s'" % (
    #     room, desc)
    # rows = conn.execute(sql).fetchall()
    # if len(rows) == 1:
    #     return rows[0][0], rows[0][1]

    # sql = "select roomno,abbr from mud_room where roomname = '%s' and description = '%s' and exits = '%s'" % (
    #     room, desc, exits)
    # rows = conn.execute(sql).fetchall()
    # if len(rows) == 1:
    #     return rows[0][0], rows[0][1]

    sql = "select max(roomno),abbr from mud_room where zone = '%s' and roomname = '%s' and description = '%s' and exits = '%s'" % (
        zone, room, desc, exits)

    row = conn.execute(sql).fetchone()
    if row and row[0]:
        return row[0], row[1]

    return -1, -1


if __name__ == "__main__":
    conn = open_database()
    roomno, abbr = check_room(conn, sys.argv[1], sys.argv[2], sys.argv[3],
                              normalize_exits(sys.argv[4]))

    tt = Tintin()
    tt.write("#var gps.roomno %d;" % (roomno))
    tt.write("#var gps.abbr %s;" % (abbr))
