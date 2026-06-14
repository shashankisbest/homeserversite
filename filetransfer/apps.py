from django.apps import AppConfig
import os
import time


class FiletransferConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filetransfer'

    def ready(self):

        temp_dir = "temp_zips"

        if not os.path.exists(temp_dir):
            return

        for filename in os.listdir(temp_dir):

            filepath = os.path.join(temp_dir, filename)

            if os.path.isfile(filepath):
                os.remove(filepath)
