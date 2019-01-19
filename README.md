# praetorian-mastermind
A program that solves the Mastermind puzzle game challenge from Praetorian.

https://www.praetorian.com/challenges/mastermind


SOLVED! -Y.H.Kim

https://www.praetorian.com/hall-of-fame


## Features
- Automatically proceeds through the levels
- Option to reset the whole challenge


## Issues
- Sometimes, the potential guess list is reduced to zero- there is a flaw in the reduction logic.
- Network timeouts.


## Install and Run
```pip install```

```python praetorian-mastermind.py```


## How does this work?
Creates a seed of random initial guesses to quickly cut down potential solutions. This step does not choose the optimal guesses that would shrink the number of solutions the most. At the moment, you can only hope that the seed was strong enough to reduce the solutions to a reasonable size...


Once there are a low number of solutions, switch to solve by guessing in a way that eliminates the most possible solutions in a guess. This is computationally extensive and will time out if there are too many potential solutions to start with. The seed is supposed to make sure this doesn't happen.