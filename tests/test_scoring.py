from playus_scoreboard.playus.models import Player, PlayerScore, Team, TeamBonus
from playus_scoreboard.scoring.engine import (
    build_player_leaderboard,
    build_team_leaderboard,
    calculate_player_totals,
    calculate_team_totals,
)


def make_players() -> list[Player]:
    return [
        Player(user_id="player-a", display_name="Player A", team_id="team-a"),
        Player(user_id="player-b", display_name="Player B", team_id="team-a"),
        Player(user_id="player-c", display_name="Player C", team_id="team-b"),
    ]


def make_teams() -> list[Team]:
    players = make_players()

    return [
        Team(
            team_id="team-a",
            name="Team A",
            players=players[:2],
        ),
        Team(
            team_id="team-b",
            name="Team B",
            players=players[2:],
        ),
    ]


def make_scores() -> list[PlayerScore]:
    return [
        PlayerScore(
            score_id="score-1",
            user_id="player-a",
            group_id="group-1",
            group_game_id="group-game-1",
            score=40,
        ),
        PlayerScore(
            score_id="score-2",
            user_id="player-b",
            group_id="group-1",
            group_game_id="group-game-1",
            score=30,
        ),
        PlayerScore(
            score_id="score-3",
            user_id="player-c",
            group_id="group-1",
            group_game_id="group-game-1",
            score=50,
        ),
    ]


def test_player_totals():
    totals = calculate_player_totals(
        players=make_players(),
        scores=make_scores(),
    )

    assert totals == {
        "player-a": 40,
        "player-b": 30,
        "player-c": 50,
    }


def test_team_total_with_double_bonus():
    bonuses = [
        TeamBonus(
            team_id="team-a",
            bonus_type="double",
            points=50,
            reason="Double",
        )
    ]

    totals = calculate_team_totals(
        teams=make_teams(),
        players=make_players(),
        scores=make_scores(),
        bonuses=bonuses,
    )

    assert totals["team-a"] == 120
    assert totals["team-b"] == 50


def test_player_leaderboard():
    leaderboard = build_player_leaderboard(
        players=make_players(),
        scores=make_scores(),
    )

    assert [entry.identifier for entry in leaderboard] == [
        "player-c",
        "player-a",
        "player-b",
    ]

    assert [entry.score for entry in leaderboard] == [50, 40, 30]
    assert [entry.rank for entry in leaderboard] == [1, 2, 3]


def test_team_leaderboard():
    bonuses = [
        TeamBonus(
            team_id="team-a",
            bonus_type="double",
            points=50,
            reason="Double",
        )
    ]

    leaderboard = build_team_leaderboard(
        teams=make_teams(),
        players=make_players(),
        scores=make_scores(),
        bonuses=bonuses,
    )

    assert leaderboard[0].identifier == "team-a"
    assert leaderboard[0].score == 120
    assert leaderboard[0].rank == 1

    assert leaderboard[1].identifier == "team-b"
    assert leaderboard[1].score == 50
    assert leaderboard[1].rank == 2
