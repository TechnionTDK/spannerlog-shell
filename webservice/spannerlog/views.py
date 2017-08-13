from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .wrapper import Wrapper, WrapperException


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
        print("WrapperException occured!")
        print(str(e))
        return HttpResponse(str(e), status=500)
  
    return HttpResponse(data, content_type='application/json')
