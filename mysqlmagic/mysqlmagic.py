# encoding: utf-8

import IPython
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from IPython.display import display, HTML
from IPython import get_ipython

import pymysql
import json
from pandas.core.frame import DataFrame


# NAME_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]*$")


@magics_class
class MySQLMagic(Magics):

    def __init__(self, shell, db=None, cursor=None):
        super(MySQLMagic, self).__init__(shell=shell)
        self.db = db
        self.cursor = cursor

    @cell_magic
    def configs(self, line, cell):
        """
            Example:
            Input:
                %%configs
                {
                    "user": "root",
                    "password": "admin",
                    "host": "127.0.0.1",
                    "port": 13306
                }
            Output:
                Database version : 8.0.26
        """
        args = json.loads(cell)
        db = pymysql.connect(
            user=args['user'], 
            password=args['password'], 
            host=args['host'],
            port=args['port']
        )
        self.db = db
        self.cursor = db.cursor()
        self.cursor.execute("SELECT VERSION()")
        version = self.cursor.fetchone()
        print("Connect to the database successfully! The database version is %s" % version)

    @cell_magic
    @magic_arguments()
    @argument('-v', '--dest_var', type=str, help='Destination variable name which stores the query results.')
    @argument('-f', '--dest_file', type=str, help='Path of csv file to save query results.')
    def mysql(self, line, cell):
        """
            Example:
            Input:
                %%mysql -v query_results -f query_results.csv
                SELECT *
                FROM EMPLOYEE;
            Output:
                The query results will be saved at python variable query_results, and be saved as a file query_results.csv.
        """
        args = parse_argstring(self.mysql, line)
        sqls = cell.strip().split(';')
        sqls = [sql.strip() for sql in sqls if len(sql)>0]
        for i, sql in enumerate(sqls):
            sql_type = sql.split()[0].upper()
            try:
                msg = self.cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
            else:
                if i<len(sqls)-1:
                    continue
                if sql_type == 'SELECT':
                    cols = [tp[0] for tp in self.cursor.description]
                    records = self.cursor.fetchall()
                    df = DataFrame(records)
                    df.columns = cols
                    if args.dest_var:
                        IPython.get_ipython().push({args.dest_var: df})
                    if args.dest_file:
                        df.to_csv(args.dest_file, index=False)
                    display(HTML(df.to_html()))
                else:
                    print(msg)