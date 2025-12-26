# Algorithm

Brute force approach with pruning of certain branches in the decision tree.

- Stack - to maintain states of the amphipod position in the hallways and the siderooms.
- pop from the stack a state and do the following
- Try filling all the open side rooms.
- When we have arrived at the point where we don't have open side rooms or the side rooms can't be filled, then from the siderooms that arent yet filled yet one amphipod is chosen with all available spots for it to move in the hallway.
- All such amphipod and available hallway spots are added to the stack to try.
- We terminate exploring the decision tree when
  - we can't move any amphipod further or no hallway slots available and we haven't properly arranged.
    or
  - all the pods are correctly arranged. In this case keep track of the energy spent. Keep track of the minimum.
