import re
import os


filename = os.path.join(os.path.dirname(__file__), 'day1/input.txt')

def fetch_first_and_last_digit_regex(line: str):
    first_match = re.search(r'\d', line)
    first_digit = first_match.group(0) if first_match else 0
    last_match = re.search(r'\d(?![\s\S]*\d)', line)
    last_digit = last_match.group(0) if last_match else 0
    return str(first_digit) + str(last_digit)


def day1_part1():
    numbers = []
    with open(filename) as f:
        for line in f.readlines():
            calibrated = fetch_first_and_last_digit_regex(line)
            print(calibrated)
            numbers.append(int(calibrated))
    return sum(numbers)


digit_mapping = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def map_words_to_numbers(digits: list[str]) -> list[str]:
    print(f"in: {digits}")
    mapped_digits = []
    for digit in digits:
        mapped_digits.append(digit_mapping.get(digit, digit))
    print(f"out: {mapped_digits}")
    return mapped_digits


def find_all_digits(subject: str) -> list[str]:
    return re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', subject, re.IGNORECASE)


def get_calibrated_int(digits: list[str]) -> int:
    first = digits[0]
    digits.reverse()
    last = digits[0]
    calibrated = str(first) + str(last)
    return int(calibrated)


def day1_part2() -> int:
    numbers = []
    with open(filename) as f:
        for line in f.readlines():
            print(line)
            matched_digits = find_all_digits(line)
            mapped_digits = map_words_to_numbers(matched_digits)
            calibrated_int = get_calibrated_int(mapped_digits)
            print(f"result: {calibrated_int}")
            numbers.append(calibrated_int)
    return sum(numbers)


def main():
    part1_result = day1_part1()
    part2_result = day1_part2()
    print(part1_result)
    print(part2_result)


if __name__ == '__main__':
    main()
