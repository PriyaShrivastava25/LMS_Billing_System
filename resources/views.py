from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from enrollments.models import Enrollment
from django.core.paginator import Paginator

@login_required
def course_list(request):

    courses = Course.objects.all()

   
    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(title__icontains=search_query)

   
    category = request.GET.get('category')
    if category:
        courses = courses.filter(category__iexact=category)

  
    price = request.GET.get('price')

    if price == "low":
        courses = courses.filter(price__lt=1000)

    elif price == "mid":
        courses = courses.filter(price__gte=1000, price__lte=5000)

    elif price == "high":
        courses = courses.filter(price__gt=5000)

    paginator = Paginator(courses, 5)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # return render(request, "course_list.html", {"courses": page_obj})

    return render(request, "course_list.html", {
    "courses": page_obj,
    "page_obj": page_obj
})




@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
        return redirect("student_dashboard")

    #  Seat check
    if course.available_seats <= 0:
        messages.error(request, f"Sorry! {course.title} is full.")
        return redirect("course_list")

    Enrollment.objects.create(
        student=request.user,
        course=course
    )

    messages.success(request, f"Successfully enrolled in {course.title}!")
    return redirect("student_dashboard")



