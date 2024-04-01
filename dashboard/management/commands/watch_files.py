import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.core.management.base import BaseCommand
from dashboard.data_parsing import certificate_data_extraction_from_pdf
from dashboard.models import Configurations

logger = logging.getLogger(__name__)


class FileHandler(FileSystemEventHandler):

    def on_created(self, event):
        logger.info("File created event detected.")
        file_path = event.src_path
        logger.debug("File path: %s", file_path)
        if file_path.endswith(".pdf"):
            logger.info("---------Holding file for 2 sec------------")
            time.sleep(2)
            logger.info("Processing PDF file: %s", file_path)
            res = certificate_data_extraction_from_pdf(file_path)
            logger.info("Result: %s", res)


class Command(BaseCommand):
    help = "Watch directories for file changes and parse"

    def handle(self, *args, **kwargs):
        directory_paths = self.get_directory_paths_from_table()
        for directory_path in directory_paths:
            if os.path.isdir(directory_path):
                self.watch_directory(directory_path)
            else:
                try:
                    # os.makedirs(directory_path)
                    # logger.info("Create directory: %s", directory_path)
                    logger.error("Directory '%s' does not exist.", directory_path)
                    self.watch_directory(directory_path)
                except OSError as e:
                    logger.error("Failed to create directory '%s': %s", directory_path)

    def get_directory_paths_from_table(self):
        directory_paths = []
        configurations = Configurations.objects.filter(
            data_key="certificateDestinationPath"
        )
        for configuration in configurations:
            directory_paths.append(configuration.data_value)
        return directory_paths

    def watch_directory(self, directory):
        logger.info("Watching directory: %s", directory)
        observer = Observer()
        event_handler = FileHandler()
        observer.schedule(event_handler, directory, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logger.info("File watcher stopped.")

        observer.join()
