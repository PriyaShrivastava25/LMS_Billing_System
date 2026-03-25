from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from enrollments.models import Enrollment

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "course_list.html", {"courses": courses})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # To check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, f"You are already enrolled in {course.title}.")
        return redirect("student_dashboard")

    # To Check seat availability
    if course.available_seats <= 0:
        messages.error(request, f"Sorry! {course.title} is full.")
        return redirect("course_list")

    Enrollment.objects.create(student=request.user, course=course)

    messages.success(request, f"You have successfully enrolled in {course.title}!")
    return redirect("student_dashboard")


