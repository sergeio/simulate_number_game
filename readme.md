Number game simulation
======================

I played a fun card-game the other day, where cards of numbers 1-100 are
shuffled into a deck, and players take turns playing them from their hands onto
one of four piles: two starting at 100, with each card played needing to be
lower than the previous, and two starting at 1, ascending.

There is an additional rule that allows jumping a pile in the opposite
direction it requires if you have the card exactly 10 away from its current
value (in the direction you want to go).

The game allows limited communication between players.

This description isn't very good, but if you've played the game before, it's
probably enough to jog your memory.

What is this code?
------------------

This bad not good code is me simulating this game to figure out how likely you
are to win with very basic strategies.

The learnings:

If you play ONLY playing the least bad cards each turn with no communication, a
game with 2 people will succeed 1.7% of the time.

If you allow players to also jump at the ends of their turns (since the game
only has a minimum requirement for cards played per turn), the rate of success
goes up to 3%.

If you allow players to also make good plays at the ends of their turns, and
not just jumps, the rate improves to 5%.

If you allow basic communication of calling "dibs" on a pile because you
have something good you want to do with it, we can get up to 9%.

Adding a minor dibs (as in I have a good card to play here, but it's not a full
on jump-card) gets us to 10%.

And tweaking the algorithm to penalize a player ignoring another's dibs: 12%.
