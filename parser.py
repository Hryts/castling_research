import re

WHITE, BLACK, DRAW = (1, 0), (0, 1), (0.5, 0.5)
RESULTS = {"1-0": WHITE, "1/2-1/2": DRAW, "0-1": BLACK}


def parse(input_file, output_file, number_of_games):
    pgn = open(input_file)
    errors_counter = 0

    with open(output_file, 'w') as out_file:
        current_game = 0
        while current_game != number_of_games:
            current_game += 1
            white_rating = black_rating = None
            white_castling = black_castling = 0
            result = None

            try:
                for i in range(20):

                    line = pgn.readline()
                    if i == 5:
                        white_rating = re.search(r'.*"(\d+)"', line).groups('0')[0]
                    if i == 6:
                        black_rating = re.search(r'.*"(\d+)"', line).groups('0')[0]
                    if i == 16:
                        result = RESULTS[re.search(r'.*"([0-9\-/]+)"', line).groups('0')[0]]
                    if i == 18:
                        if re.search(r"\d+\. O-O(-O)?", line):
                            white_castling = 1
                        if re.search(r"\d+\.\s.{2,5}\sO-O(-O)?", line):
                            black_castling = 1
                out_file.write(f"{white_rating}, {white_castling}, {result[0]}\n")
                out_file.write(f"{black_rating}, {black_castling}, {result[1]}\n")
            except (KeyError, AttributeError) as e:
                if pgn.readline() == "" and pgn.readline() == "":
                    print("File is over")
                    break
                errors_counter += 1
                counter = 2
                for _ in range(counter):
                    while (line := pgn.readline().strip()) != "":
                        pass
        print(f"Number of errors: {errors_counter}")
        print(f"Number of games: {current_game}")


if __name__ == '__main__':
   parse('games.pgn', 'january_2019_blitz.csv', -1)
