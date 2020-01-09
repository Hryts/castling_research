import re

WHITE, BLACK, DRAW = (1, 0), (0, 1), (0.5, 0.5)
RESULTS = {"1-0": WHITE, "1/2-1/2": DRAW, "0-1": BLACK}


def parse(input_file, output_file, number_of_games):
    pgn = open(input_file)
    errors_counter = 0

    with open(output_file, 'w') as out_file:
        current_game = 0

        # parse the exact number of games or till the end of the file if number_of_games is < 0
        while current_game != number_of_games:
            current_game += 1
            white_rating = black_rating = None
            white_castling = black_castling = 0
            result = None

            try:
                # read all the 20 lines of the game
                for i in range(20):
                    line = pgn.readline()
                    # if it is the line with the rating of "white" player
                    if i == 5:
                        white_rating = re.search(r'.*"(\d+)"', line).groups('0')[0]

                    # if it is the line with the rating of "black" player
                    if i == 6:
                        black_rating = re.search(r'.*"(\d+)"', line).groups('0')[0]

                    # if it is the line of game result
                    if i == 16:
                        result = RESULTS[re.search(r'.*"([0-9\-/]+)"', line).groups('0')[0]]

                    # if it is the lines with moves listed
                    if i == 18:
                        # check if the first player has castled
                        if re.search(r"\d+\. O-O(-O)?", line):
                            white_castling = 1

                        # check if the second player has castled
                        if re.search(r"\d+\.\s.{2,5}\sO-O(-O)?", line):
                            black_castling = 1

                # write results to the .csv file
                out_file.write(f"{white_rating}, {white_castling}, {result[0]}\n")
                out_file.write(f"{black_rating}, {black_castling}, {result[1]}\n")
            except (KeyError, AttributeError) as e:
                # if reached the end of the file (cause .readline() will always return an empty line)
                if pgn.readline() == "" and pgn.readline() == "" and pgn.readline() == "":
                    print("File is over")
                    break
                errors_counter += 1

                # read all the lines to reach the next game (as if an exception occured, all the lines, belonging
                # to the current game have not been read
                for _ in range(2):
                    while (line := pgn.readline().strip()) != "":
                        pass
        print(f"Number of errors: {errors_counter}")
        print(f"Number of games: {current_game}")


if __name__ == '__main__':
    parse('games.pgn', 'january_2019_blitz.csv', -1)
