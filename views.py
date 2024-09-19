from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import FileResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from .models import User, File
from .methods import *
from rp5_portal import settings
import os


def index(request, dir='files'):
    clean_temp_folder()
    message = ''
    if dir not in os.listdir('storage'):
        return HttpResponse('Folder not available.')

    # handle uploaded files on POST
    if request.method == 'POST' and request.user.is_authenticated:
        if 'file-input' in request.FILES:
            file = request.FILES['file-input']

            if File.objects.filter(name=file).exists():
                return HttpResponse('Cannot upload duplicate name. Rename file to upload.')

            # Save the uploaded file
            save_path = os.path.join(settings.STORAGE_ROOT, request.POST['dir'], file.name)
            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # record file model
            file_record = File()
            file_record.name = file.name
            file_record.uploaded_by = request.user
            file_record.save()
            create_thumbnail(save_path, os.path.join(settings.STORAGE_ROOT, 'thumbnails', file.name))
            message = 'File uploaded successfully.'
        else:
            message = 'No file uploaded.'

    return render(request, "fileshare/index.html", {
        "app": 'fileshare',
        "dir": dir,
        "files": get_files_with_metadata(dir),
        "thumbnails": os.listdir(os.path.join(settings.STORAGE_ROOT, 'thumbnails')),
        "model_data": File.objects.all(),
        "storage": format_size(get_all_content_size()),
        "message": message
    })

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "fileshare/login.html", {
                "app": 'fileshare',
                "message": "Invalid email and/or password."
                })
    else:
        return render(request, "fileshare/login.html", {
            "app": 'fileshare'
        })
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        
        # get user info
        username = request.POST["username"]
        email = request.POST["email"]

        # ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "fileshare/register.html", {
                "message": "Passwords must match."
            })
        
        # create new user, display error if necessary
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "fileshare/register.html", {
                "app": 'fileshare',
                "message": "Email or username already taken."
            })
        except ValueError as e:
            print(e) # create dropdown to view error details?
            return render(request, "fileshare/register.html", {
                "app": 'fileshare',
                "message": "Invalid form submission."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "fileshare/register.html", {
            "app": 'fileshare'
        })
    
@login_required
def download(request, file_name, dir):
    try:
        user_file_objs = File.objects.filter(uploaded_by=request.user)
        user_file_names = [file.name for file in user_file_objs]
        filepath = os.path.join(settings.STORAGE_ROOT, dir, file_name)
        response = FileResponse(open(filepath, 'rb'), as_attachment=True, filename=file_name)

        if file_name in user_file_names:
            return response
        else:
            return HttpResponse('Invalid permissions.')
    except File.DoesNotExist:
        return HttpResponse('File does not exist.')
    
@login_required 
def delete(request, file_name, dir):
    try:
        # uploaded file
        user_file_objs = File.objects.filter(uploaded_by=request.user)
        user_file_names = [file.name for file in user_file_objs]
        filepath = os.path.join(settings.STORAGE_ROOT, dir, file_name)

        if file_name not in user_file_names:
            return HttpResponse('Invalid permissions.')

        # handle associated thumbnail
        thumbnail_filepath = os.path.join(settings.STORAGE_ROOT, 'thumbnails', file_name)
        if os.path.isfile(thumbnail_filepath):
            os.remove(thumbnail_filepath)

        os.remove(filepath)
        file_record = File.objects.get(name=file_name)
        file_record.delete()
        return HttpResponse("File deleted.")
    except File.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))