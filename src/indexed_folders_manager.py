import json
import os
from datetime import datetime


class IndexedFoldersManager:
    def __init__(self, file_path='indexed_folders.json'):
        self.file_path = file_path
        self.indexed_folders = self.load_indexed_folders()

    def load_indexed_folders(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def save_indexed_folders(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.indexed_folders, f, indent=2)

    def add_indexed_folder(self, folder_path):
        self.indexed_folders[folder_path] = {
            'last_indexed': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        self.save_indexed_folders()

    def update_indexed_folder(self, folder_path):
        if folder_path in self.indexed_folders:
            self.indexed_folders[folder_path]['last_updated'] = datetime.now().isoformat()
            self.save_indexed_folders()

    def get_indexed_folders(self):
        return self.indexed_folders
