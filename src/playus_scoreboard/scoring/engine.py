from collections import defaultdict

from playus_scoreboard.playus.models import (
    LeaderboardEntry,
    Player,
    PlayerScore,
    Team,
    TeamBonus,
)


def calculate_player_totals(
    players: list[Player],
    scores: list[PlayerScore],
) -> dict[str, int]:
    """Calculate each player's total from valid recorded scores."""

    player_ids = {player.user_id for player in players}
    totals: dict[str, int] = defaultdict(int)

    for score in scores:
        if score.user_id in player_ids:
            totals[score.user_id] += score.score

    return dict(totals)


def calculate_team_totals(
    teams: list[Team],
    players: list[Player],
    scores: list[PlayerScore],
    bonuses: list[TeamBonus],
) -> dict[str, int]:
    """Calculate team totals from player scores plus applicable bonuses."""

    player_totals = calculate_player_totals(players, scores)

    player_to_team = {
        player.user_id: player.team_id
        for player in players
    }

    totals: dict[str, int] = defaultdict(int)

    for user_id, player_total in player_totals.items():
        team_id = player_to_team[user_id]
        totals[team_id] += player_total

    valid_team_ids = {team.team_id for team in teams}

    for bonus in bonuses:
        if bonus.team_id in valid_team_ids:
            totals[bonus.team_id] += bonus.points

    return dict(totals)


def build_player_leaderboard(
    players: list[Player],
    scores: list[PlayerScore],
) -> list[LeaderboardEntry]:
    """Build a descending individual leaderboard."""

    totals = calculate_player_totals(players, scores)

    ranked = sorted(
        totals.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return [
        LeaderboardEntry(
            rank=index,
            identifier=user_id,
            score=score,
        )
        for index, (user_id, score) in enumerate(ranked, start=1)
    ]


def build_team_leaderboard(
    teams: list[Team],
    players: list[Player],
    scores: list[PlayerScore],
    bonuses: list[TeamBonus],
) -> list[LeaderboardEntry]:
    """Build a descending team leaderboard."""

    totals = calculate_team_totals(
        teams=teams,
        players=players,
        scores=scores,
        bonuses=bonuses,
    )

    ranked = sorted(
        totals.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return [
        LeaderboardEntry(
            rank=index,
            identifier=team_id,
            score=score,
        )
        for index, (team_id, score) in enumerate(ranked, start=1)
    ]
