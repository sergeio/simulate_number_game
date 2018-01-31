import random

DEBUG = False


class Game:

    def __init__(self, players=None):
        self.num_players = 2 if not players else players
        if self.num_players == 1:
            max_hand_size = 8
        elif self.num_players == 2:
            max_hand_size = 7
        else:
            max_hand_size = 6

        self.players = [Player(game=self, max_hand_size=max_hand_size) for _ in
                        range(self.num_players)]

        self.deck = list(range(2, 100))
        random.shuffle(self.deck)

        self.piles = [Pile(1, direction=1), Pile(1, direction=1),
                      Pile(100, direction=-1), Pile(100, direction=-1)]


    def won(self):
        return not self.deck and all(not p.hand for p in self.players)

    def lost(self):
        if any(p.failed_to_play for p in self.players):
            return True
        return all(p.is_out for p in self.players)


class Pile:

    def __init__(self, start, direction=1):
        self.cards = [start]
        self.direction = direction

    def __lt__(self, other):
        return abs(50 - self.top) < abs(50 - other.top)

    @property
    def top(self):
        return self.cards[-1]

    def __repr__(self):
        return 'Pile <top=%s dir=%s>' % (self.top, self.direction)


class Player:

    def __init__(self, game, max_hand_size):
        self.id = random.randint(0, 10000)
        self.game = game
        self.hand = []
        self.max_hand_size = max_hand_size

        # Player has played all their cards
        self.is_out = False

        # Player lost the game by having no moves
        self.failed_to_play = False

    def __repr__(self):
        return 'Player <id=%s hand=%s>' % (self.id, self.hand)

    def draw_to_full(self):
        while len(self.hand) < self.max_hand_size:
            if not self.game.deck:
                return
            new_card = self.game.deck.pop()
            self.hand.append(new_card)

        if not self.hand:
            self.is_out = True

    def play_round(self):
        if self.is_out:
            return
        required_to_play = 2 if self.game.deck else 1
        for _ in range(required_to_play):
            if not self.hand:
                DEBUG and print('Player %s: No cards to play' % self)
                return
            if self.can_jump():
                DEBUG and print(' jumping')
                card, pile = self.can_jump()
                self.play(card, pile)
            else:
                play = self.find_closest_card_to_play()
                if not play:
                    self.failed_to_play = True
                    DEBUG and print('Player %s lost the game' % self)
                    return
                distance, card, pile = play
                self.play(card, pile)

        while True:
            play = self.have_good_play()
            if play:
                card, pile = play
                self.play(card, pile)
            else:
                break

        self.draw_to_full()

    def have_good_play(self):
        jump = self.can_jump()
        if jump:
            card, pile = jump
            return card, pile

    def can_jump(self):
        for card in self.hand:
            for pile in self.game.piles:
                if card == pile.top - (10 * pile.direction):
                    return card, pile
        return False

    def find_closest_card_to_play(self):
        plays = []
        for card in self.hand:
            for pile in self.game.piles:
                if not self.card_playable_on_pile(card, pile):
                    continue
                distance = abs(card - pile.top)
                plays.append((distance, card, pile))
        if not plays:
            DEBUG and print('Player %s has nothing to play: %s' % (self, self.hand))
            return
        return min(plays)

    @classmethod
    def card_playable_on_pile(cls, card, pile):
        return ((pile.direction > 0 and card > pile.top) or
                (pile.direction < 0 and card < pile.top))

    def play(self, card, pile):
        assert(card in self.hand)
        DEBUG and print('Player %s, playing %s on %s' % (self, card, pile))
        self.hand = [c for c in self.hand if c != card]
        pile.cards.append(card)


def alternate_players(game):
    while True:
        for player in game.players:
            yield player

def play_game(dummy_arg=None):
    game = Game(players=2)
    for player in game.players:
        player.draw_to_full()
        DEBUG and print(('starting', player.hand))

    for player in alternate_players(game):
        if game.lost():
            return False
        player.play_round()

        if game.won():
            return True


    # DEBUG and print('Cards remaining: %s' % len(game.deck))
    # DEBUG and print()
    # for pile in game.piles:
    #     DEBUG and print((pile, pile.cards))

    return False
