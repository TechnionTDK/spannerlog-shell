from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .wrapper import Wrapper, WrapperException, bcolors

import re

from pprint import pprint


def index(request):
  return render(request, 'spannerlog/index.html', {})


@csrf_exempt
def run(request):
  print(bcolors.OKBLUE + "Incoming: program" + bcolors.ENDC)
  pprint(request.POST)

  try:
    wrapper = Wrapper()
    files = request.FILES.getlist('edb')
    for f in files:
      wrapper.add_input_file(f)
    
    wrapper.write_program(request.POST['program'])
    wrapper.run()

    data = wrapper.get_schema()
    pprint(data)
  except WrapperException as e:
    print(bcolors.FAIL)
    print("WrapperException occured!")
    print(str(e))

    ansi_escape = re.compile(r'\x1b[^m]*m')
    return HttpResponse(ansi_escape.sub('', str(e)), status=500)

  return HttpResponse(data, content_type='application/json')

@csrf_exempt
def get_table(request, table_name):
  print(bcolors.OKBLUE + "Incoming: table name" + bcolors.ENDC)
  pprint(table_name)

  wrapper = Wrapper()
  data = wrapper.get_table(table_name)
  return HttpResponse(data, content_type='application/json')

