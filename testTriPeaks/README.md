# Solver of Tri Peaks
This is one solver of Tri Peaks game.

# Algorithm
Each state of tri-peaks game is mapped into one number, and we use remaining-card number as utility function.
1. initial-state: full card on table, first card of stock, stock remains 23 card.
2. push initial-state into queue
3. while queue is not empty:
   - 3.1 pop state from queue with lowest remaining-card-number
   - 3.2 if current state clears the board, break the loop
   - 3.3 get all possible states with given state
   - 3.4 enqueue all possible states
4. print the result.

# Version log
- v0.1: initial version, try to enum all versions, cannot solve overnight.
- v0.2: use fixed array to pre-allocate all resources, and try to enum all. (2mins)
- v0.3: use priority queue to reduce solving time. (9 sec)
- v0.4: re-write IO parts.
- v0.5: remove pre-allocated resources. (6 sec)