import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Count
from main_app.models import TennisPlayer, Tournament, Match


def get_tennis_players(search_name=None, search_country=None):

    players = None
    if search_name and search_country:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name,
                                              country__icontains=search_country)
    elif search_name:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name)
    elif search_country:
        players = TennisPlayer.objects.filter(country__icontains=search_country)

    if players is None:
        return ''

    return '\n'.join([
        f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}"
        for p in players.order_by('ranking')
    ])


def get_top_tennis_player():

    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()
    if top_player is None:
        return ''
    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins_count} wins."


def get_tennis_player_by_matches_count():

    player = TennisPlayer.objects.annotate(
        matches_count=Count('matches')
    ).filter(matches_count__gt=0).order_by('-matches_count', 'ranking').first()

    if player is None:
        return ''
    return f"Tennis Player: {player.full_name} with {player.matches_count} matches played."


def get_tournaments_by_surface_type(surface=None):

    if surface is None:
        return ''

    tournaments = (Tournament.objects.prefetch_related('matches')
                   .annotate(count_matches=Count('matches'))
                   .filter(surface_type__icontains=surface)
                   .order_by('-start_date'))

    return '\n'.join([
        f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.count_matches}"
        for t in tournaments
    ])


def get_latest_match_info():

    last_match = Match.objects.prefetch_related('players').order_by('-date_played').first()
    if last_match is None:
        return ''
    players = [p.full_name for p in last_match.players.order_by('full_name')]

    return (f"Latest match played on: {last_match.date_played}, "
            f"tournament: {last_match.tournament.name}, score: {last_match.score}, "
            f"players: {' vs '.join(players)}, "
            f"winner: {last_match.winner.full_name if last_match.winner else 'TBA'}, "
            f"summary: {last_match.summary}")


def get_matches_by_tournament(tournament_name=None):

    if tournament_name is None:
        return ''

    matches = Match.objects.filter(
        tournament__name=tournament_name
    ).order_by('-date_played')

    return '\n'.join([
        f'Match played on: {m.date_played}, score: {m.score}, '
        f'winner: {m.winner.full_name if m.winner else 'TBA'}'
        for m in matches
    ])

