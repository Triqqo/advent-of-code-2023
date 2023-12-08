import dataclasses
import re
from dataclasses import dataclass


@dataclass
class GameSet:
    blue: int = 0
    green: int = 0
    red: int = 0


@dataclass
class Game:
    id: int
    game_results_str: str
    sets: list[GameSet] = None
    is_possible: bool = False
    fewest_needed_cubes: GameSet = None
    power: int = 0


class Constants:
    MAX_RED_CUBES = 12
    MAX_GREEN_CUBES = 13
    MAX_BLUE_CUBES = 14


def parse_game_dict(game_str: str) -> Game:
    match = re.search(r'^Game (?P<game_id>\d+): (?P<game_results_str>[a-zA-Z0-9;, ]*)$', game_str)

    return Game(id=int(match.group('game_id')), game_results_str=match.group('game_results_str'))


def parse_game_sets(game: Game) -> Game:
    game_sets_str = game.game_results_str.split(';')
    game.sets = []
    for game_set_str in game_sets_str:
        reds = re.search(r'(\d*) red', game_set_str)
        greens = re.search(r'(\d*) green', game_set_str)
        blues = re.search(r'(\d*) blue', game_set_str)

        game_set = GameSet(
            red=int(reds.group(1)) if reds else 0,
            green=int(greens.group(1)) if greens else 0,
            blue=int(blues.group(1)) if blues else 0
        )
        game.sets.append(game_set)
    print(game.sets)
    return game


def check_possibility(game: Game) -> Game:
    if all(game_set.red <= Constants.MAX_RED_CUBES
           and game_set.green <= Constants.MAX_GREEN_CUBES
           and game_set.blue <= Constants.MAX_BLUE_CUBES for game_set in game.sets):
        game.is_possible = True
    print(f"Possibility: {game.is_possible}")
    return game


def part1():
    games: list[Game] = []
    possible_game_ids: list[int] = []
    # with open('day2/part1_test.txt') as f:
    with open('day2/input.txt') as f:
        for line in f.readlines():
            print('\n' + line.strip('\n'))
            game = parse_game_dict(line)
            game = parse_game_sets(game)
            game = check_possibility(game)
            games.append(game)
            if game.is_possible:
                possible_game_ids.append(game.id)
    print('\n' + str(sum(possible_game_ids)))
    return games


def get_fewest_needed_cubes(game: Game):
    reds = []
    greens = []
    blues = []
    game.fewest_needed_cubes = GameSet()
    for game_set in game.sets:
        reds.append(game_set.red)
        greens.append(game_set.green)
        blues.append(game_set.blue)
    game.fewest_needed_cubes.red = max(reds)
    game.fewest_needed_cubes.green = max(greens)
    game.fewest_needed_cubes.blue = max(blues)
    return game


def get_power(game: Game):
    game.power = game.fewest_needed_cubes.red * game.fewest_needed_cubes.green * game.fewest_needed_cubes.blue
    return game


def part2(games: list[Game]):
    powers = []
    for game in games:
        game = get_fewest_needed_cubes(game)
        print(game.fewest_needed_cubes)
        game = get_power(game)
        print(game.power)
        powers.append(game.power)
    print(sum(powers))


def main():
    games = part1()
    part2(games)


if __name__ == '__main__':
    main()
