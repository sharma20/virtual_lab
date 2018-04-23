from django.shortcuts import render, redirect, HttpResponse
import logging
import ConfigParser
from vital.utils import get_notification_message
from vital.models import Registered_Course, Course, Virtual_Machine, Virtual_Machine_Type
from ..forms import CreateCourseForm, CreateVmsForm
from django.utils.crypto import get_random_string


logger = logging.getLogger(__name__)
config_ini = ConfigParser.ConfigParser()
config_ini.optionxform = str

# TODO change to common config file in shared location
config_ini.read("/home/vital/config.ini")


def index(request):
    return redirect('/authoring/courses/home/')


def course_home(request):
    """
    lists all active courses for faculty
    :param request: http request
    :return: active courses page
    """
    logger.debug("In course home")
    active_courses = Registered_Course.objects.filter(user_id=request.user.id, course__status='ACTIVE')

    # to display common notification messages like system maintenance plans on all pages
    request.session['notification'] = get_notification_message()
    message = ''
    if len(active_courses) == 0:
        message = 'You have no active courses'
    return render(request, 'authoring/course_home.html', {'active_courses': active_courses, 'message':message})


def course_create(request):
    logger.debug("in course create")
    error_message = ''
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            course = Course()
            course.name = form.cleaned_data['course_name']
            course.course_number = form.cleaned_data['course_number']
            course.start_date = form.cleaned_data['start_date']
            course.course_owner = request.user.id
            reg_code = get_random_string(length=8)
            course.registration_code = reg_code
            course.save()
            return render(request, 'authoring/course_add_vms.html', {'form': form})
    else:
        form = CreateCourseForm()
    return render(request, 'authoring/course_create.html', {'form': form, 'error_message':error_message})


def course_add_vms(request):
    logger.debug("in course create")
    error_message = ''
    if request.method == 'POST':
        form = CreateVmsForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(course_owner=user.id)
            vm = Virtual_Machine()
            vm.name = form.cleaned_data['vm_name']
            vm.type = form.cleaned_data['vm_type']
            vm.course = course.id
            vm.save()
            return HttpResponse('You are at the Networking Page')
    else:
        form = CreateCourseForm()
    return render(request, 'authoring/course_add_vms.html', {'form': form, 'error_message': error_message})


def course_vm_setup(request):
    return HttpResponse('you are on the course vm setup page')


def course_destroy(request):
    return HttpResponse('you are on the course remove page')