#! /user/bin/python3
import multiprocessing

import implementation

def main():
    with multiprocessing.Pool(4) as pool:
        results = pool.map(implementation.play_game, range(4000))
        print(sum(results) / len(results))

    # results = [implementation.play_game() for _ in range(10)]
    # print(sum(results) / len(results))

    # implementation.play_game()


if __name__ == '__main__':
    main()
