import os
from datetime import datetime


def truncate_text(text, max_length=200):
    return text[:max_length] + "..." if len(text) > max_length else text


def get_folder_modification_time(folder_path):
    return max(os.path.getmtime(os.path.join(root, file))
               for root, _, files in os.walk(folder_path)
               for file in files)


def folder_needs_update(folder_path, last_updated):
    last_updated_time = datetime.fromisoformat(last_updated)
    folder_mod_time = datetime.fromtimestamp(get_folder_modification_time(folder_path))
    return folder_mod_time > last_updated_time
