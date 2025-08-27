from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Test database connection and show basic info'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Test connection with a simple query
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                self.stdout.write(f"✅ Database connection successful!")
                self.stdout.write(f"MySQL Version: {version}")
                
                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()[0]
                self.stdout.write(f"Current Database: {db_name}")
                
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                self.stdout.write(f"Tables: {', '.join([table[0] for table in tables])}")
                
        except Exception as e:
            self.stderr.write(f"❌ Database connection failed: {e}")
