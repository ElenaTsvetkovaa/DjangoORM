import datetime
import os

import django
from django.db.models import Q, Count, F, Avg

from main_app.choices import DragonBreath

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import House, Dragon, Quest


def get_houses(search_string=None):

    houses = (House.objects
              .filter(Q(name__istartswith=f'{search_string}') | Q(motto__istartswith=f'{search_string}'))
              .order_by('-wins', 'name')
              )
    if not houses or not search_string:
        return  "No houses match your search."

    return '\n'.join([
        f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}" for h in houses
    ])


def get_most_dangerous_house():

    if not House.objects.first() or not Dragon.objects.first():
        return "No relevant data."

    most_dangerous_house = House.objects.get_houses_by_dragons_count().first()

    return (f"The most dangerous house is the "
            f"House of {most_dangerous_house.name} with {most_dangerous_house.dragon_count} dragons. "
            f"Currently {'ruling'if most_dangerous_house.is_ruling else 'not ruling'} the kingdom.")


def get_most_powerful_dragon():

    top_dragon = (Dragon.objects
                  .filter(is_healthy=True)
                  .annotate(quest_count=Count('quest'))
                  .order_by('-power', 'name')
                  .first())

    if not top_dragon:
        return "No relevant data."


    return (f"The most powerful healthy dragon is {top_dragon.name} "
            f"with a power level of {top_dragon.power:.1f}, breath type {top_dragon.breath}, "
            f"and {top_dragon.wins} wins, coming from the house of "
            f"{top_dragon.house.name}. Currently participating in {top_dragon.quest_count} quests.")


def update_dragons_data():

    num_of_dragons_affected = (Dragon.objects.filter(
                                is_healthy=False,
                                power__gt=1.0
                            )
                             .update(
                                power=F('power') - 0.1,
                                is_healthy=True,
                            ))

    if num_of_dragons_affected == 0:
        return "No changes in dragons data."

    return (f"The data for {num_of_dragons_affected} dragon/s has been changed. "
            f"The minimum power level among all dragons is {Dragon.objects.values('power').order_by('power').first()['power']:.1f}")


def get_earliest_quest():

    quest = Quest.objects.order_by('start_time').first()

    if not quest:
        return "No relevant data."

    dragons = quest.dragons.order_by('-power', 'name').values('name')

    return (f"The earliest quest is: {quest.name}, code: {quest.code}, "
            f"start date: {quest.start_time.day}.{quest.start_time.month}.{quest.start_time.year}, "
            f"host: {quest.host.name}. Dragons: {'*'.join([d['name'] for d in dragons])}. "
            f"Average dragons power level: {quest.dragons.aggregate(avg_power=Avg('power'))['avg_power']:.2f}")


def announce_quest_winner(quest_code):
    try:
        quest = Quest.objects.prefetch_related('dragons').get(code=quest_code)
        top_dragon = quest.dragons.order_by('-power', 'name').first()

        top_dragon.wins += 1
        top_dragon.house.wins += 1

        top_dragon.save()
        top_dragon.house.save()
        quest.delete()

        return (f"The quest: {quest.name} has been won by dragon {top_dragon.name} from house {top_dragon.house.name}. "
                f"The number of wins has been updated as follows: {top_dragon.wins} total wins for the dragon "
                f"and {top_dragon.house.wins} total wins for the house. "
                f"The house was awarded with {quest.reward:.2f} coins.")

    except Exception:
        return  "No such quest."


