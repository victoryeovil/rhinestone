from django.core.management.base import BaseCommand, CommandError
import os
from django.db import connection


class Command(BaseCommand):
    help = 'Clear migrations.'

    def handle(self, *args, **options):
        try:
            os.remove("db.sqlite3")
        except:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DROP SCHEMA public CASCADE;")
                    cursor.execute("CREATE SCHEMA public;")
            except: pass
        try:
            os.rmdir("media")
        except:
            pass
        try:
            for i in os.listdir(path=f"app{os.sep}migrations"):
                if i  != "__init__.py":
                    try:
                        os.remove(path=f"app{os.sep}migrations{os.sep}{i}")
                    except:
                        for file in os.listdir(f"app{os.sep}migrations{os.sep}{i}"):
                            os.remove(path=f"app{os.sep}migrations{os.sep}{i}{os.sep}{file}")
                        os.removedirs(f"app{os.sep}migrations{os.sep}{i}")
                    print(f"app{os.sep}migrations{os.sep}{i}")
        except Exception as e:
            raise CommandError(str(e))
        self.stdout.write(self.style.SUCCESS(f"Done with clearing migrations. Please proceed to run makemigrations command!"))