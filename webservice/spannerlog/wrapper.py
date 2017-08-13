import os
import json
import subprocess
import platform
import time
from pprint import pprint


class Wrapper(object):

    def __init__(self):
        self.app = "myapp"
        self.working_dir = os.path.abspath("spannerlog/temp/" + self.app + "/")
        self.db = self.app + "_db"

        self.init_app()



    def run(self):
        print("running %s..." % (self.app,))

        try:
            if platform.system() == "Linux":
                df = subprocess.Popen("cd %s; spl compile" % (self.working_dir,), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = df.communicate()
                # out = subprocess.check_output("""
                #     cd %s; 
                #     spl compile
                #     """ % (self.working_dir, ), shell=True)

                print("Out:")
                print(out)
                print("Err:")
                print(err)
        except subprocess.CalledProcessError as e:
            print("exception!")
            print(str(e))
            print(str(e.output))
            print(e.output)
            pprint(vars(e))

            raise WrapperException(e.output)


        data = json.dumps({
           'some_var_1': 'foo',
           'some_var_2': 'bar',
        })

        return data


    def write_program(self, text):
        with open(self.working_dir + "app.spl", 'w') as file:
            file.write(text)



    def add_input_file(self, file):
        path = self.working_dir + "input/" + file.name
        if not os.path.exists(path):
            with open(path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)



    def init_app(self):
        """creates an empty spannerlog app"""
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        if not os.path.exists(self.working_dir + "input"):
            os.makedirs(self.working_dir + "input")

        if not os.path.exists(self.working_dir + "db.url"):
            with open(self.working_dir + "db.url", 'w') as f:
                f.write("postgresql://localhost/" + self.db)

        if not os.path.exists(self.working_dir + "app.spl"):
            with open(self.working_dir + "app.spl", 'w') as f:
                f.write("")


class WrapperException(Exception):
    pass
