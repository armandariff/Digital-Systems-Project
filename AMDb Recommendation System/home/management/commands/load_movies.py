import json
import csv
import datetime
from dateutil.parser import parse

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from home.models import Movie, Genre


class Command(BaseCommand):
    help = "Command to Load Movies"

    def add_arguments(self, parser) -> None:
        parser.add_argument('csv_file', nargs=1, type=str)
        return super().add_arguments(parser)
    
    @transaction.atomic()
    def handle(self, *args, **options):
        file_name = options['csv_file'][0]
        with open(file_name, 'r', encoding="utf-8") as file:
            rows = csv.reader(file)
            next(rows)
            for row in rows:
                budget = row[0]
                geners = row[1]
                url = row[2]
                external_id= row[3]
                language = row[5]
                title = row[6]
                overview = row[7]
                popularity = row[8]
                extra = row[9]
                if row[11]:
                    release_date = parse(row[11])
                else:
                    release_date = datetime.datetime.today()
                revenue = row[12]
                runtime = row[13]
                
                try:
                    if not popularity:
                        popularity = 0
                    if not revenue:
                        revenue = 0
                    if not runtime:
                        runtime = 0
                    movie = Movie.objects.create(
                        title=title,
                        external_id=external_id,
                        image=url,
                        overview=overview,
                        language=language,
                        popularity=popularity,
                        release_date=release_date,
                        revenue=revenue,
                        runtime=runtime,
                        extra=extra,
                    )
                    for genre in json.loads(geners):
                        gen = Genre.objects.get_or_create(name=genre.get('name'), external_id=genre.get('id'))
                        movie.genre.add(gen[0])
                        
                except Exception as e:
                    pass