from django.core.management.base import BaseCommand
from book.models import UBStudent
from django.contrib.auth.models import User
from book.models import UBStudent
from django.db.utils import IntegrityError

class Command(BaseCommand):
    args = '<file>'
    help = 'takes one argument <file>'

    def handle(self, *args, **kwargs):
        if not args:
            return None
        with open(args[0], 'r') as f:
            for line in f:
                if line[0] == '#':
                    continue
                ubnumber, ubitname, email = line.split()
                ubnumber = int(ubnumber)
                try:
                    u = User.objects.create(username=ubitname, email=email, is_active=False)
                    UBStudent.objects.create(user=u, ubnumber=ubnumber)
                    print('creating record for %s' % ubitname)
                except IntegrityError:
                    print('%s skipped' % ubitname)
                    continue
        print('completed!')
