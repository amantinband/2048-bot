# 2048 bot

![Alt Text](https://github.com/mantinband/2048-bot/blob/master/bot.gif)

## Tired of wasting time on each game? waste time no more!

just `clone` and run `2048.py`

#### How does it work?
Each iteration all 4 board options are computed and given a score. The board with the highest score is the direction that is chosen.

#### Wanna try?
Current algorithm is pretty simple and works not bad.  
Think you have a better algorithm to compute the score of the board?  
 `algorithm.py` has the following function:
```python
def compute_board_score(board, key):
    # put your logic here
    return score
```
This function is called 4 times each iteration and gives each board a score

The function receives a `Board` object and a `key`.  
where the `key` can be one of `Keys.ARROW_DOWN`, `Keys.ARROW_UP`, `Keys.ARROW_RIGHT`, `Keys.ARROW_LEFT`.
and the `Board` is the how the current board would look if the `key` was pressed.  
Edit this function as you wish and run the program to see how you did.

