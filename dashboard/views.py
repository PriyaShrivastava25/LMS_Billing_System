from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from enrollments.models import Enrollment
from billing.models import Invoice
from resources.models import Course

# HOME
def home(request):
    return render(request, 'home.html')

# LOGIN 
def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")

        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "login.html")

# SIGNUP
def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        name_parts = name.strip().split()
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "signup.html")


# STUDENT DASHBOARD
@login_required
def student_dashboard(request):

    if request.user.is_staff or request.user.is_superuser:
        return redirect("admin_dashboard")

    student = request.user
    enrollments = Enrollment.objects.filter(student=student).select_related('course')

    enrollment_data = []
    total_spent = 0

    for e in enrollments:
        gst = (e.course.price * 18) / 100
        total = e.course.price + gst
        total_spent += total

        invoice = Invoice.objects.filter(enrollment=e).first()

        enrollment_data.append({
            'course_title': e.course.title,
            'price': e.course.price,
            'gst': gst,
            'total': total,
            'payment_status': e.payment_status,
            'enrolled_on': e.enrollment_date,
            'invoice_id': invoice.id if invoice else None
        })

    context = {
        'student_name': student.first_name,
        'enrollments': enrollment_data,
        'total_courses': enrollments.count(),
        'total_spent': total_spent
    }

    return render(request, 'student_dashboard.html', context)


# COURSE LIST
@login_required
def course_list(request):

    if request.user.is_staff or request.user.is_superuser:
        return redirect("admin_dashboard")

    courses = Course.objects.all()
    return render(request, "course_list.html", {"courses": courses})


# INVOICE
@login_required
def view_invoice(request, invoice_id):

    if request.user.is_staff or request.user.is_superuser:
        return redirect("admin_dashboard")

    try:
        invoice = Invoice.objects.get(
            id=invoice_id,
            enrollment__student=request.user
        )
    except Invoice.DoesNotExist:
        return render(request, 'invoice_not_found.html')

    return render(request, 'invoice_view.html', {'invoice': invoice})

#LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")
