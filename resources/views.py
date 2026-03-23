
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Course

# @login_required
# def course_list(request):
#     courses = Course.objects.all()
#     return render(request, "course_list.html", {"courses": courses})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from enrollments.models import Enrollment

# Show all courses
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "course_list.html", {"courses": courses})


# Enroll in a course
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if seats are available
    if course.available_seats > 0:
        # Create enrollment record
        Enrollment.objects.create(student=request.user, course=course)

        # Reduce available seats
        course.available_seats -= 1
        course.save()

        # Optional: success message
        success_message = f"You have successfully enrolled in {course.title}!"
        courses = Course.objects.all()
        return render(request, "course_list.html", {"courses": courses, "success": success_message})
    else:
        # Optional: error message if full
        error_message = f"Sorry! {course.title} is full."
        courses = Course.objects.all()
        return render(request, "course_list.html", {"courses": courses, "error": error_message})
