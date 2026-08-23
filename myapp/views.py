from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponse
from .models import Server

# HOME
def home(request):
    return render(request, 'home.html')



# LOGIN
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)
        print("Password:", password)

        user = authenticate(request, username=username, password=password)
        print("Authenticated User:", user)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")

        return render(request, "signin.html", {"error": "Invalid username or password"})

    return render(request, "signin.html")


# REGISTER PAGE
def register(request):
    return render(request, 'register.html')


# REGISTER PROCESS
def registration(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email already exists"})

        User.objects.create_user(username=username, email=email, password=password)

        return redirect("user_dashboard")

    return render(request, "register.html")


# DASHBOARD SELECTION
def dashboard_selection(request):
    return render(request, "dashboard_selection.html")


# ADMIN DASHBOARD
@staff_member_required
def admin_dashboard(request):

    search = request.GET.get("search")

    if search:
        servers = Server.objects.filter(server_name__icontains=search)
    else:
        servers = Server.objects.all()

    total_users = User.objects.count()
    total_servers = Server.objects.count()
    online_servers = Server.objects.filter(status="Online").count()
    offline_servers = Server.objects.filter(status="Offline").count()
    critical_servers = Server.objects.filter(overall_health="Critical").count()

    context = {
        "servers": servers,
        "total_users": total_users,
        "total_servers": total_servers,
        "online_servers": online_servers,
        "offline_servers": offline_servers,
        "critical_servers": critical_servers,
    }

    return render(request, "admin_dashboard.html", context)


# USER DASHBOARD
@login_required
def user_dashboard(request):
    servers = Server.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'servers': servers})


# ADD SERVER
@login_required
def addserver(request):
    if request.method == "POST":
        server_name = request.POST["server_name"]
        ip_address = request.POST["ip_address"]
        operating_system = request.POST["operating_system"]
        cpu_usage = int(request.POST["cpu_usage"])
        ram_usage = int(request.POST["ram_usage"])
        disk_usage = int(request.POST["disk_usage"])
        status = request.POST["status"]

        if cpu_usage < 50 and ram_usage < 50:
            overall_health = "Good"
        elif cpu_usage < 80 or ram_usage < 80:
            overall_health = "Average"
        else:
            overall_health = "Critical"

        if not Server.objects.filter(
            user=request.user,
            server_name=server_name,
            ip_address=ip_address
        ).exists():

            Server.objects.create(
                user=request.user,
                server_name=server_name,
                ip_address=ip_address,
                operating_system=operating_system,
                cpu_usage=cpu_usage,
                ram_usage=ram_usage,
                disk_usage=disk_usage,
                status=status,
                overall_health=overall_health
            )

        return redirect("user_dashboard")

    return render(request, "addserver.html")

# DELETE SERVER
@login_required 
def delete_server(request,id):
    server=get_object_or_404(Server,id=id)
    server.delete()
    return redirect("admin_dashboard")

# EDIT SERVER
@login_required
def edit_server(request, id):
    server = get_object_or_404(Server, id=id)

    if request.method == "POST":
        server.server_name = request.POST["server_name"]
        server.ip_address = request.POST["ip_address"]
        server.operating_system = request.POST["operating_system"]
        server.cpu_usage = int(request.POST["cpu_usage"])
        server.ram_usage = int(request.POST["ram_usage"])
        server.disk_usage = int(request.POST["disk_usage"])
        server.status = request.POST["status"]

        if server.cpu_usage < 50 and server.ram_usage < 50:
            server.overall_health = "Good"
        elif server.cpu_usage < 80 or server.ram_usage < 80:
            server.overall_health = "Average"
        else:
            server.overall_health = "Critical"

        server.save()
        return redirect("admin_dashboard")

    return render(request, "edit_server.html", {"server": server})

# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('signin')
