#!/usr/bin/python3
from optparse import OptionParser
import sqlite3
import sys
import time
import re

g_version = "0.9"
g_OptParser = OptionParser(version="%%prog %s" % (g_version))

class c_db_finder():
  def __init__(self, options):
    self.options = options
    self.dbname = options.dbfile
    self.tblname = options.table
    self.cursor = None
    self.conn = None
    self.myre = re.compile(options.regex)
    self.prt_after_len = 20
    self.opt_multi = 1
    self.opt_row_only = 0
    if ( options.soption  == "1" ):
      self.opt_multi = 0
    if ( options.soption  == "r" ):
      self.opt_multi = 0
      self.opt_row_only = 1

  def db_close(self):
    self.conn.close()

  def db_connect(self):
    self.conn = sqlite3.connect(self.dbname)
    self.conn.row_factory = sqlite3.Row
    self.conn.text_factory = str
    self.cursor = self.conn.cursor()

  def do_all_table(self, callback_func):
    dbquery="SELECT name FROM sqlite_master WHERE type='table';"
    self.cursor.execute(dbquery)
    tables = self.cursor.fetchall()
    print(">> %d Tables found :" % (len(tables)))
    for table_name in tables:
       table_name = table_name[0]
       callback_func(table_name)

  def check_string(self, col_name, data, prt_keys, start_pos = 0, opt_multi = 0):
     b_matched = 0
     if ( start_pos == 0 ):
        cur_data = data[col_name]
     else:
        cur_data = data[col_name][start_pos:]
     if ( type(cur_data) == type(1) ):
       return
     my_match = (self.myre.search(str(cur_data)))
     key_str = ""
     if my_match != None:
     # Make key with (a-b...)
        if ( prt_keys != None):
           key_str = "(" + ("-".join(list(map(lambda x:str(data[x]), prt_keys.split(","))))) + ")"
        print("Keys[%s] Col[%s] Data[%s]" \
        % (key_str, col_name, cur_data[my_match.start():my_match.end()+self.prt_after_len]))
        if ( opt_multi ):
          return self.check_string(col_name, data, prt_keys, start_pos+my_match.end())
        b_matched = 1
     return b_matched

  def print_table(self, str_tblname):
    dbquery = "SELECT sql FROM sqlite_master WHERE name='%s';" % (str_tblname )
    self.cursor.execute(dbquery)
    CurRow = self.cursor.fetchone()
    print("> Table [%s]" % (str_tblname))
    if ( CurRow != None ):
      scheme_data = CurRow[0].replace("\n","")
      scheme_data = scheme_data.split(",")
      scheme_data[0] = scheme_data[0].split("(")[1]
      scheme_data = list(map(lambda x: (x.strip()).split(" ")[0], scheme_data))
      print (scheme_data)
  def do_one_table(self, str_tblname):
    dbquery = "SELECT * FROM %s;" % ( str_tblname )
    print("> %s" % (str_tblname))
    self.cursor.execute(dbquery)
    line_cnt = 0
    while 1:
      CurRow = self.cursor.fetchone()
      if CurRow == None:
        break
      for cur_col in CurRow.keys():
         b_matched = self.check_string(cur_col, CurRow, self.options.keys, opt_multi = self.opt_multi)
         if ( b_matched and self.opt_row_only ):
            break

  def do_it(self):
    self.db_connect()
    target_table = self.options.table
    if ( self.options.cmd == "list" ):
      cb_func = self.print_table
    else:
      cb_func = self.do_one_table
    if ( target_table == None ):
      self.do_all_table(cb_func)
    else:
      cb_func(target_table)
    self.db_close()

def main():
  requiredOpts = "dbfile regex".split()
  g_OptParser.add_option("-i", "--input", dest="dbfile",
  help="source DB-file", default=None)
  g_OptParser.add_option("-t", "--table", dest="table",
  help="search TableName, if none is all", default=None)
  g_OptParser.add_option("-k", "--keys", dest="keys",
  help="keys ex. head1,head2 ", default=None)
  g_OptParser.add_option("-c", "--cmd", dest="cmd",
  help="commands [ do | list ] default [ do ]", default="do")
  g_OptParser.add_option("-o", "--option", dest="soption",
  help="search option [ 1 | m | r ] m (multi) 1(one-col) r(one-row) default [ m ]", default="m")
  g_OptParser.add_option("-r", "--regex", dest="regex",
  help="search RegEx ex. '&#[0-9]{1,5};'", default=None)
  (options, args) = g_OptParser.parse_args()
  for szOptValName in requiredOpts:
    if options.__dict__[szOptValName] is None:
      g_OptParser.error("parameter %s required" % szOptValName)
  my_obj = c_db_finder (options)
  my_obj.do_it()

if __name__ == "__main__":
  main()
