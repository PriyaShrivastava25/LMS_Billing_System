
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from resources.models import Course
from enrollments.models import Enrollment
from billing.models import Invoice
from django.db.models import Sum, Count
from django.contrib import messages


def admin_dashboard(request):

    total_users = User.objects.filter(is_superuser=False, is_staff=False).count()

    total_courses = Course.objects.count()

    total_enrollments = Enrollment.objects.count()

    total_revenue = Invoice.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    top_courses = Course.objects.annotate(
        enroll_count=Count('enrollment')
    ).order_by('-enroll_count')[:5]

    recent_enrollments = Enrollment.objects.select_related('student', 'course').order_by('-id')[:5]

    context = {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "total_revenue": total_revenue,
        "top_courses": top_courses,
        "recent_enrollments": recent_enrollments,
    }

    return render(request, "AdminPanel/admin_dashboard.html", context)

# Course List
def manage_courses(request):
    courses = Course.objects.all()

    return render(request, "adminpanel/manage_courses.html", {"courses": courses})

# Add Course
def add_course(request):

    if request.method == "POST":
        title = request.POST.get('title')
        price = request.POST.get('price')
        total_seats = request.POST.get('total_seats')
        category = request.POST.get('category')

        Course.objects.create(
            title=title,
            price=price,
            total_seats=total_seats,
            available_seats=total_seats,
            category=category
        )

        messages.success(request, "Course added successfully!")
        return redirect("admin_courses")

    return render(request, "adminpanel/add_course.html")
    
# Edit Course
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.price = request.POST.get("price")
        course.total_seats = request.POST.get("total_seats")
        course.category = request.POST.get("category")
        course.save()

        return redirect("manage_courses")

    return render(request, "adminpanel/edit_course.html", {"course": course})


# Delete Course
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect("manage_courses")


# Manage Enrollments
def manage_enrollments(request):

    enrollments = Enrollment.objects.select_related('student', 'course')

    student = request.GET.get('student')
    if student:
        enrollments = enrollments.filter(student__username__icontains=student)

    course = request.GET.get('course')
    if course:
        enrollments = enrollments.filter(course__title__icontains=course)

    return render(request, "AdminPanel/manage_enrollments.html", {
        "enrollments": enrollments
    })


# Manage Invoice
def manage_invoices(request):

    invoices = Invoice.objects.select_related('enrollment__student', 'enrollment__course')

    status = request.GET.get('status')
    if status:
        invoices = invoices.filter(enrollment__payment_status=status)

    return render(request, "AdminPanel/manage_invoices.html",
        {"invoices": invoices
    })