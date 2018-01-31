#! /user/bin/python3
import multiprocessing

import implementation

def main():
    with multiprocessing.Pool(4) as pool:
        results = pool.map(implementation.play_game, range(4000))
    print(sum(results) / len(results))
    # for _ in range(10):
    #     implementation.play_game()
    # implementation.play_game()


if __name__ == '__main__':
    main()
