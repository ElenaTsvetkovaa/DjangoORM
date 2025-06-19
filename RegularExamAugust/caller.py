import os
import django
from django.db.models import Q, Count, Sum, F, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.choices import MissionStatusChoices

# Import your models here
from main_app.models import Astronaut, Spacecraft, Mission

def get_astronauts(search_string=None):

    try:
        astronauts = Astronaut.objects.filter(
            Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
        ).order_by('name')

        return '\n'.join(
            f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {'Active' if a.is_active else 'Inactive'}"
            for a in astronauts
        )  if astronauts else ''

    except ValueError:
        return ''


def get_top_astronaut():

    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()
    if top_astronaut:
        return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions."

    return "No data."

def get_top_commander():

    top_commander = (Astronaut.objects.prefetch_related('commanded_missions')
                     .annotate(count_missions=Count('commanded_missions'))
                     .order_by('-count_missions', 'phone_number').first())

    if top_commander and top_commander.count_missions > 0:
        return f"Top Commander: {top_commander.name} with {top_commander.count_missions} commanded missions."
    return "No data."

def get_last_completed_mission():

    last_completed_mission = (Mission.objects
                              .filter(status=MissionStatusChoices.COMPLETED)
                              .select_related('spacecraft', 'commander')
                              .prefetch_related('astronauts')
                              .order_by('-launch_date')
                              .first())

    if not last_completed_mission:
        return "No data."

    astronauts = last_completed_mission.astronauts.all().order_by('name')
    total_spacewalks = astronauts.aggregate(total=Sum('spacewalks'))['total']

    return (f"The last completed mission is: {last_completed_mission.name}. "
            f"Commander: {last_completed_mission.commander.name if last_completed_mission.commander else 'TBA'}. "
            f"Astronauts: {', '.join([a.name for a in astronauts])}. "
            f"Spacecraft: {last_completed_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")



def get_most_used_spacecraft():

    spacecraft = (Spacecraft.objects
                  .prefetch_related('mission_set', 'mission_set__astronauts')
                  .annotate(total_missions=Count('mission',  distinct=True),
                           total_astronauts=Count('mission__astronauts',  distinct=True))
                  .order_by('-total_missions', 'name')
                  .first()
                  )
    if spacecraft and spacecraft.total_missions > 0:
        return (f"The most used spacecraft is: {spacecraft.name}, "
                f"manufactured by {spacecraft.manufacturer}, "
                f"used in {spacecraft.total_missions} missions, "
                f"astronauts on missions: {spacecraft.total_astronauts}.")
    return "No data."

def decrease_spacecrafts_weight():

    spacecrafts = (Spacecraft.objects
                   .prefetch_related('mission_set')
                   .filter(mission__status=MissionStatusChoices.PLANNED,
                           weight__gte=200.0)
                   ).distinct()

    affected_spacecrafts_count = spacecrafts.update(weight=F('weight') - 200.0)
    if affected_spacecrafts_count > 0:
        avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']
        return (f"The weight of {affected_spacecrafts_count} spacecrafts has been decreased. "
                f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")

    return "No changes in weight."


