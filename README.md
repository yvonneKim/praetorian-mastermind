# praetorian-mastermind
A program that solves the Mastermind puzzle game challenge from Praetorian.

https://www.praetorian.com/challenges/mastermind

https://en.wikipedia.org/wiki/Mastermind_(board_game)


SOLVED! -Y.H.Kim

https://www.praetorian.com/hall-of-fame


## Features
- Automatically proceeds through the levels
- Option to reset the whole challenge


## Issues
- Sometimes, the potential guess list is reduced to zero- there is a flaw in the reduction logic
- Network timeouts and hangs


## Install and Run
```pip install```

```python praetorian-mastermind.py```

If it hangs or runs into an error, CTRL-C and run it again- it will automatically resume at the current level.


## How does this work?
First, it creates a seed of random initial guesses to quickly cut down potential solutions. This step does not choose the optimal guesses that would shrink the number of solutions the most.


Once the seed guesses have been used, it will switch to solve by guessing in a way that eliminates the most possible solutions in a guess. This is computationally extensive and will time out if there are too many potential solutions to start with. The seed is supposed to make sure this doesn't happen, although it's far from perfect and will repeat the rounds persistently until it passes. 

This program has a high but not complete chance of passing a level. The attempts do pretty well and can usually win the level after a few tries. The final level is an exception- be patient passing it. 

