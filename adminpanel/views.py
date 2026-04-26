from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from resources.models import Course
from enrollments.models import Enrollment
from billing.models import Invoice
from django.db.models import Sum, Count
from django.contrib import messages
from django.db.models.functions import TruncMonth
from datetime import datetime
import json

# Admin dashboard
def admin_dashboard(request):

    total_users = User.objects.filter(is_superuser=False, is_staff=False).count()

    total_courses = Course.objects.count()

    total_enrollments = Enrollment.objects.count()

    total_revenue = Invoice.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    recent_enrollments = Enrollment.objects.select_related('student', 'course').order_by('-id')[:5]

    context = {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "total_revenue": total_revenue,
        "recent_enrollments": recent_enrollments,
    }

    return render(request, "adminpanel/admin_dashboard.html", context)

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
        return redirect("manage_courses")

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

    return render(request, "adminpanel/manage_enrollments.html", {
        "enrollments": enrollments
    })


# Manage Invoice
def manage_invoices(request):

    invoices = Invoice.objects.select_related('enrollment__student', 'enrollment__course')

    status = request.GET.get('status')
    if status:
        invoices = invoices.filter(enrollment__payment_status=status)

    return render(request, "adminpanel/manage_invoices.html",
        {"invoices": invoices
    })


# Analytics Dashboard
def analytics_dashboard(request):

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    invoices = Invoice.objects.all()

    if start_date and end_date:
        invoices = invoices.filter(
            enrollment__enrollment_date__range=[start_date, end_date]
        )

    total_revenue = invoices.aggregate(total=Sum('total_amount'))['total'] or 0

    monthly_data = (
        invoices
        .annotate(month=TruncMonth('enrollment__enrollment_date'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('month')
    )

    months = []
    revenue = []

    for m in monthly_data:
        months.append(m['month'].strftime("%b %Y") if m['month'] else "")
        revenue.append(float(m['total']))

    course_stats = (
        Course.objects
        .annotate(total_enrollments=Count('enrollment'))
        .order_by('-total_enrollments')[:5]
    )

    top_course_labels = [c.title for c in course_stats]
    top_course_data = [c.total_enrollments for c in course_stats]

    course_data = (
        Enrollment.objects
        .values('course__title')
        .annotate(count=Count('id'))
    )

    course_labels = [c['course__title'] for c in course_data]
    course_counts = [c['count'] for c in course_data]

    category_data = (
        invoices
        .values('enrollment__course__category')
        .annotate(total=Sum('total_amount'))
    )

    category_labels = []
    category_revenue = []

    for c in category_data:
        category_labels.append(c['enrollment__course__category'] or "Other")
        category_revenue.append(float(c['total']))

    top_category = category_data.order_by('-total').first()
    top_category_name = top_category['enrollment__course__category'] if top_category else "N/A"

    context = {
        "total_revenue": total_revenue,

        "months": json.dumps(months),
        "revenue": json.dumps(revenue),

        "top_courses": course_stats,

        "course_labels": json.dumps(course_labels),
        "course_counts": json.dumps(course_counts),

        "category_labels": json.dumps(category_labels),
        "category_revenue": json.dumps(category_revenue),

        "top_category": top_category_name,

        "top_course_labels": json.dumps(top_course_labels),
        "top_course_data": json.dumps(top_course_data),

        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "adminpanel/analytics_dashboard.html", context)

