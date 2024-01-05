import random
from datetime import timedelta

from django.db.transaction import atomic
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker
from apps.contests.models import ContestModel, SolveModel, DisciplineModel, ScrambleModel, RoundSessionModel
from apps.accounts.models import User
from scripts.scramble import generate_scramble

DISCIPLINE_NAMES = ['3by3']
CONTEST_QTY = 20


class Command(BaseCommand):
    help = 'Generate fake data for contests app'

    def handle(self, *args, **kwargs):
        self.fake = Faker()

        self.disciplines()
        self.contests()
        self.ongoing_contest()
        self.scrambles()
        self.contest_crambles_sessions_solves()
        self.solve()

    def disciplines(self):
        for discipline in DISCIPLINE_NAMES:
            DisciplineModel.objects.create(
                name=discipline
            )

    def contests(self):
        pass

    def ongoing_contest(self):
        pass

    def scrambles(self):
        pass

    def round_sessions_and_solves(self):
        pass

    def solve(self):
        pass

    @atomic
    def contest_crambles_sessions_solves(self):
        last_contest = ContestModel.objects.last()
        contest_number = 1
        if last_contest:
            contest_number = last_contest.contest_number + 1
            last_contest.ongoing=False
            last_contest.save()
        else:
            start_time = timezone.now()

        end_time = start_time + timedelta(days=7)
        contest = ContestModel.objects.create(
            contest_number=contest_number,
            start=start_time,
            end=end_time
        )

        discipline = DisciplineModel.objects.get(name='3by3')
        for scramble_position in range(1, 6):
            generated_scramble = generate_scramble()
            scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                     extra=False, contest=contest, discipline=discipline)
            scramble.save()
        for scramble_position in range(1, 3):
            scramble_position = f"E{scramble_position}"
            generated_scramble = generate_scramble()
            scramble = ScrambleModel(position=scramble_position, scramble=generated_scramble,
                                     extra=True, contest=contest, discipline=discipline)
            scramble.save()

        users = User.objects.all()

        for user in users:
            discipline = DisciplineModel.objects.get(name='3by3')
            round_session = RoundSessionModel.objects.create(
                contest=contest,
                discipline=discipline,
                user=user,
                submitted=True
            )
            random_time = random.uniform(8, 100)

            scrambles = ScrambleModel.objects.filter(contest=contest, discipline=discipline, extra=False)
            for scramble in scrambles:
                solve = SolveModel.objects.create(
                    time_ms=round(random.uniform(random_time*random.uniform(0.7, 1.3), random_time*random.uniform(0.7, 1.3)), 3)*1000,
                    dnf=False,
                    state='submitted',
                    scramble=scramble,
                    user=user,
                    discipline=discipline,
                    round_session=round_session,
                    contest=contest,
                    reconstruction=scramble
                )
