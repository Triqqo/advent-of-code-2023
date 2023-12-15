import re
from dataclasses import dataclass


@dataclass
class PotentialPart:
    number: int
    first_position: int = 0
    first_adj_position: int = 0
    last_position: int = 0
    last_adj_position: int = 0


def mapped_numbers_and_positions(numbers: list[str], line: str):
    parts: list[PotentialPart] = []
    unique_numbers: list[str] = []
    duplicates: list[str] = []
    for number_str in numbers:
        if number_str in unique_numbers:
            duplicates.append(number_str)
        else:
            unique_numbers.append(number_str)

        line_length = len(line)
        part = PotentialPart(number=int(number_str))

        part_matches = list(re.finditer(rf'(?<!\d)({number_str})(?!\d)', line))

        part.first_position = part_matches[1].start(0) if number_str in duplicates else part_matches[0].start(0)
        part.first_adj_position = max([part.first_position - 1, 0])

        part.last_position = part.first_position + (len(number_str) - 1)
        part.last_adj_position = min([part.last_position + 1, line_length - 1])

        parts.append(part)
    return parts


def highlight_string_index(string, index):
    return string[:index] + '\x1b[6;30;47m' + string[index] + '\x1b[0m' + string[index + 1:]


def check_adjacency(parts: list[PotentialPart], previous_line: str, current_line: str, next_line: str):
    adjacent_parts = []
    for part in parts:

        positions_to_check = list(range(part.first_adj_position, part.last_adj_position + 1))
        positions_to_skip = list(range(part.first_position, part.last_position + 1))

        print(f"part: \x1b[6;30;44m{part.number}\x1b[0m")
        print(f"line: \x1b[6;30;44m {current_line}\x1b[0m")
        for i in positions_to_check:
            # if previous_line != '' and not previous_line[i].isspace():
            if previous_line != '':
                print("prev: " + highlight_string_index(previous_line, i))
                if not previous_line[i].isspace() and not previous_line[i].isdigit():
                    print(f"\x1b[6;30;42mfound symbol: {previous_line[i]}\x1b[0m")
                    adjacent_parts.append(part.number)
                    break
            # if i not in positions_to_skip and not current_line[i].isspace():
            if i not in positions_to_skip:
                print("this: " + highlight_string_index(current_line, i))
                if not current_line[i].isspace():
                    print(f"\x1b[6;30;42mfound symbol: {current_line[i]}\x1b[0m")
                    adjacent_parts.append(part.number)
                    break
            # if next_line != '' and not next_line[i].isspace():
            if next_line != '':
                print("next: " + highlight_string_index(next_line, i))
                if not next_line[i].isspace():
                    print(f"\x1b[6;30;42mfound symbol: {next_line[i]}\x1b[0m")
                    adjacent_parts.append(part.number)
                    break
        else:
            print("\x1b[6;30;41mno symbol found\x1b[0m")
    print(f"Adjacent parts: {adjacent_parts}")
    return adjacent_parts


def check_duplicates(numbers: list[str]):
    unique_numbers: list[str] = []
    duplicates: list[str] = []
    for number in numbers:
        if number in unique_numbers:
            duplicates.append(number)
            continue
        unique_numbers.append(number)
    print(f"unique: {unique_numbers}")
    print(f"duplicates: {duplicates}")
    return duplicates


def part1(file_path: str):
    with open(file_path) as f:
        line_index = 0
        lines = f.readlines()
        adjacent_parts: list[int] = []
        duplicates = []
        for line in lines:
            print(f"line index: {line_index}")
            print(f"unformatted: {line}")
            previous_line = (lines[line_index - 1] if line_index > 0 else '').strip('\n').replace('.', ' ')
            current_line = line.strip('\n').replace('.', ' ')
            next_line = (lines[line_index + 1] if line_index < len(lines) - 1 else '').strip('\n').replace('.', ' ')
            print(f"prev line: {previous_line}")
            print(f"this line: {current_line}")
            print(f"next line: {next_line}")

            numbers = re.findall(r'(\d+)', current_line)
            duplicates += check_duplicates(numbers)
            parts = mapped_numbers_and_positions(numbers, current_line)
            print(parts)

            adjacent_parts += check_adjacency(parts, previous_line=previous_line,
                                              current_line=current_line, next_line=next_line)
            line_index += 1
        print(f"total: {sum(adjacent_parts)}")
        print(f"all parts: {adjacent_parts}")
        print(f"all duplicates: {duplicates}")


def main():
    part1('day3/input.txt')
    # part1('day3/example.txt')


if __name__ == '__main__':
    main()
