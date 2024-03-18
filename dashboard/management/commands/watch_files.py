import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.core.management.base import BaseCommand

from dashboard.data_parsing import certificate_data_extraction_from_pdf

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        file_path = event.src_path
        if file_path.endswith('.pdf'):
            certificate_data_extraction_from_pdf(event.src_path)
            
        print(f'File {event.src_path} has been created')

class Command(BaseCommand):
    help = 'Watch specified directory for file changes and parse '

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        
        observer = Observer()
        directories = kwargs['directory']
        
        for directory in directories:
            if os.path.isdir(directory):
                event_handler = FileHandler()
                observer.schedule(event_handler, directory, recursive=True)
            else:
                self.stdout.write(self.style.ERROR(f"Directory '{directory}' does not exist."))
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
