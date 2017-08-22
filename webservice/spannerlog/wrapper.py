import os
import json
import subprocess
import platform
import psycopg2


class Wrapper(object):

  def __init__(self):
    self.app = "myapp"
    self.working_dir = "spannerlog/temp/" + self.app + "/"
    self.db = self.app + "_db"
    self.init_app() 


  def get_schema(self):
    conn = psycopg2.connect("dbname='%s' user='yoavn' host='localhost' password='1234'" % (self.db,))
    cur = conn.cursor()
    cur.execute("""
      SELECT table_name
      FROM information_schema.tables
      WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN
              ('pg_catalog', 'information_schema');
      """) # source: https://stackoverflow.com/questions/582657/how-do-i-discover-the-structure-of-a-postgresql-database
    rows = cur.fetchall()
    rows = [rec[0] for rec in rows]
    data = json.dumps(rows)

    conn.close()
    return data

  def get_table(self, table_name):
    conn = psycopg2.connect("dbname='%s' user='yoavn' host='localhost' password='1234'" % (self.db,))
    cur = conn.cursor()
    cur.execute("""
      SELECT column_name
          FROM information_schema.columns
      WHERE table_name = %s;
      """, (table_name,)) 
    rows = cur.fetchall()
    header = [rec[0] for rec in rows]

    table = [header]

    data = json.dumps(table)

    conn.close()
    return data


  def run(self):
    print("running %s..." % (self.app,))
    try:
      if platform.system() == "Linux":
        cmd = "cd %s; spl compile; spl run" % (self.working_dir,)

        df = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = df.communicate()

        out = out.decode('utf-8')
        err = err.decode('utf-8')

        print(out)

        if err:
          if "error" in err.lower():
              raise WrapperException(err)
          print(err)          
    except subprocess.CalledProcessError as e:
      print("CalledProcessError occured!")
      raise WrapperException(e.output)


  def write_program(self, text):
    print("writing to " + self.working_dir + "app.spl")
    with open(self.working_dir + "app.spl", 'w') as file:
      file.write(text)


  def add_input_file(self, file):
    path = self.working_dir + "edb/" + file.name.lower()
    with open(path, 'wb+') as destination:
      for chunk in file.chunks():
        destination.write(chunk)


  def init_app(self):
    if not os.path.exists(self.working_dir):
      os.makedirs(self.working_dir)

    """creates an empty spannerlog app"""
    if not os.path.exists(self.working_dir):
      os.makedirs(self.working_dir)

    if not os.path.exists(self.working_dir + "edb"):
      os.makedirs(self.working_dir + "edb")

    if not os.path.exists(self.working_dir + "edb/dummy.csv"):
      with open(self.working_dir + "edb/dummy.csv", 'w') as f:
        f.write("\"a\"\n\"b\"\n")

    if not os.path.exists(self.working_dir + "db.url"):
      with open(self.working_dir + "db.url", 'w') as f:
        f.write("postgresql://yoavn:1234@localhost:5432/" + self.db)
            
    if not os.path.exists(self.working_dir + "app.spl"):
      with open(self.working_dir + "app.spl", 'w') as f:
        f.write("")


class WrapperException(Exception):
  pass

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
