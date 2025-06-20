import os
import django
from django.db.models import Q, F
from django.db.models.aggregates import Count, Min, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from helpers import populate_model_with_data
from main_app.models import House, Dragon, Quest

# Import your models here


def get_houses(search_string=None):

    if search_string and search_string.strip() != '':

        houses = House.objects.filter(
            Q(name__istartswith=search_string) | Q(motto__istartswith=search_string)
        ).order_by('-wins', 'name')

        if houses.exists():
            return '\n'.join([
                f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}"
                for h in houses
            ])

    return "No houses match your search."

def get_most_dangerous_house():

    house = House.objects.get_houses_by_dragons_count().first()

    if house is not None:
        return (f"The most dangerous house is the "
                f"House of {house.name} with {house.dragons_count} dragons. "
                f"Currently {'ruling' if house.is_ruling else 'not ruling'} the kingdom.")
    return "No relevant data."

def get_most_powerful_dragon():

    dragon = (Dragon.objects
              .annotate(quests_count=Count('quests'))
              .filter(is_healthy=True)
              .order_by('-power', 'name').first())

    if dragon is not None:

        return (f"The most powerful healthy dragon is {dragon.name} "
                f"with a power level of {dragon.power:.1f}, breath type {dragon.breath}, and {dragon.wins} wins, "
                f"coming from the house of {dragon.house.name}. Currently participating in {dragon.quests_count} quests.")
    return "No relevant data."


def update_dragons_data():
    MIN_POWER_REQUIRED = 1.0
    POWER_DECREASE = 0.1

    num_of_dragons_affected = (Dragon.objects.filter(is_healthy=False,
                                     power__gt=MIN_POWER_REQUIRED)
               .update(power=F('power') - POWER_DECREASE, is_healthy=True))

    if num_of_dragons_affected == 0:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']
    return (f"The data for {num_of_dragons_affected} dragon/s has been changed. "
            f"The minimum power level among all dragons is {min_power:.1f}")


def get_earliest_quest():

    quest = (Quest.objects.prefetch_related('dragons')
             .annotate(dragons_count=Count('dragons'), avg_power=Avg('dragons__power') )
             .filter(dragons_count__gt=0).order_by('start_time').first())

    if quest is None:
        return "No relevant data."

    return (f"The earliest quest is: {quest.name}, code: {quest.code}, "
            f"start date: {quest.start_time.day}.{quest.start_time.month}.{quest.start_time.year}, "
            f"host: {quest.host.name}. "
            f"Dragons: {'*'.join([d.name for d in quest.dragons.order_by('-power', 'name')])}. "
            f"Average dragons power level: {quest.avg_power if quest.dragons.exists() else 0:.2f}")


def announce_quest_winner(quest_code):
    WINS_INCREMENT = 1

    quest = Quest.objects.filter(code=quest_code).first()

    if quest is None:
        return "No such quest."

    dragon_winner = quest.dragons.order_by('-power', 'name').first()
    dragon_winner.wins += WINS_INCREMENT
    dragon_winner.house.wins += WINS_INCREMENT

    dragon_winner.save()
    dragon_winner.house.save()
    quest.delete()

    return (f"The quest: {quest.name} has been won by dragon {dragon_winner.name} "
            f"from house {dragon_winner.house.name}. "
            f"The number of wins has been updated as follows: {dragon_winner.wins} "
            f"total wins for the dragon and {dragon_winner.house.wins} total wins for the house. "
            f"The house was awarded with {quest.reward:.2f} coins.")


