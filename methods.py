from rp5_portal import settings
from datetime import datetime, timedelta
from django.utils import timezone
from PIL import Image, UnidentifiedImageError
from .models import User, File
import os

def get_files_with_metadata(dir='media'):
    storage_root = settings.STORAGE_ROOT
    dir_path = os.path.join(storage_root, dir)
    file_list = os.listdir(dir_path)
    
    file_metadata = []
    
    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            file_metadata.append([file_name, format_size(os.path.getsize(file_path))])
    
    return file_metadata

def format_size(size):
    units = {0: ' B', 1: ' KB', 2: ' MB', 3: ' GB'}
    count = 0

    while size >= 1024:
        size = size/1024
        count += 1

    size = str(round(size, 3))

    return size + units[count]

def get_all_content_size():
    dirs = os.listdir(settings.STORAGE_ROOT)
    total_size = 0

    for dir in dirs:
        for file in os.listdir(os.path.join(settings.STORAGE_ROOT, dir)):
            file = os.path.join(settings.STORAGE_ROOT, dir, file)
            total_size += os.path.getsize(file)

    return total_size

def clean_temp_folder():
    try:
        temp_folder_path = os.path.join(settings.STORAGE_ROOT, 'temp')
        for filename in os.listdir(temp_folder_path):
            file = File.objects.get(name=filename)
            filepath = os.path.join(temp_folder_path, filename)
            thumbnail_filepath = os.path.join(settings.STORAGE_ROOT, 'thumbnails', filename)
            if file.upload_date < timezone.now() - timedelta(days=7):
                os.remove(filepath)
                file.delete()
                if os.path.isfile(thumbnail_filepath):
                    os.remove(thumbnail_filepath)
    except:
        print('Error occured cleaning the temp folder.')

def create_thumbnail(input_path, output_path, size=(48, 48)):
    try:
        with Image.open(input_path) as img:
            img.thumbnail(size)
            img.save(output_path)
    except UnidentifiedImageError:
        print("Unsupported image type for thumbnail generation.")