from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .wrapper import Wrapper, WrapperException, bcolors

import re

def index(request):
    return render(request, 'spannerlog/index.html', {})

@csrf_exempt
def run(request):

    try:
        wrapper = Wrapper()

        files = request.FILES.getlist('edb')
        for f in files:
            wrapper.add_input_file(f)
        
        wrapper.write_program(request.POST['program'])

        data = wrapper.run()
    except WrapperException as e:
        ansi_escape = re.compile(r'\x1b[^m]*m')
        print(bcolors.FAIL + "WrapperException occured!" + bcolors.ENDC)
        print(str(e))
        print(ansi_escape.sub('', str(e)))
        return HttpResponse(ansi_escape.sub('', str(e)), status=500)
  
    return HttpResponse(data, content_type='application/json')
