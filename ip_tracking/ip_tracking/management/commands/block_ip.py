from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP


class Command(BaseCommand):
    help = "Block an IP address"

    def add_arguments(self, parser):
        parser.add_argument("ip", type=str, help="The IP address to block")

    def handle(self, *args, **options):
        ip = options["ip"]
        BlockedIP.objects.get_or_create(ip_address=ip)
        self.stdout.write(self.style.SUCCESS(f"IP {ip} has been blocked."))
