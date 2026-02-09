from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Delete all data
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        # Clear members from all teams before deleting teams (for Djongo compatibility)
        for team in Team.objects.all():
            team.members = []
            team.save()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users (super heroes)
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'username': 'superman', 'email': 'superman@dc.com', 'first_name': 'Clark', 'last_name': 'Kent'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]
        marvel_users = [User.objects.create(**hero) for hero in marvel_heroes]
        dc_users = [User.objects.create(**hero) for hero in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Team Marvel')
        marvel_team.members = marvel_users
        marvel_team.save()
        dc_team = Team.objects.create(name='Team DC')
        dc_team.members = dc_users
        dc_team.save()

        # Create activities
        for user in marvel_users + dc_users:
            Activity.objects.create(user=user, activity_type='Running', duration=30, calories_burned=300, date=date.today())
            Activity.objects.create(user=user, activity_type='Cycling', duration=45, calories_burned=400, date=date.today())

        # Create workouts
        for user in marvel_users + dc_users:
            Workout.objects.create(user=user, workout_type='HIIT', suggested_by='Coach', date=date.today())
            Workout.objects.create(user=user, workout_type='Yoga', suggested_by='Coach', date=date.today())

        # Create leaderboard
        Leaderboard.objects.create(team=marvel_team, points=200, rank=1)
        Leaderboard.objects.create(team=dc_team, points=180, rank=2)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
