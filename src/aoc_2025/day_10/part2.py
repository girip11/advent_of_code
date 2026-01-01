from z3 import Int, Optimize, Sum, sat

from aoc_2025.day_10.mypyc_impl import Machine


# I have to think of another way. If I model this as a constraint problem to be satisfied
# I will be using z3 solver package for this. I cannot think of any other way
# Take this example
# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# This is how I will model using Z3 solver
# from z3 import *
# s = Optimize()
# b1 = Int('b1')
# b2 = Int('b2')
# b3 = Int('b3')
# b4 = Int('b4')
# b5 = Int('b5')
# b6 = Int('b6')
# s.add(b6>=0)
# s.add(b5>=0)
# s.add(b4>=0)
# s.add(b4>=0)
# s.add(b3>=0)
# s.add(b2>=0)
# s.add(b1>=0)
# s.add(b1+b2+b4 == 7)
# s.add(b2+b6 == 5)
# s.add(b3+b4+b5 == 4)
# s.add(b5+b6 == 3)
# s.minimize(Sum(v))
# s.check() == sat
# s.model()
def compute_fewest_joltage_button_presses(machines: list[Machine]) -> int:
    total_presses: int = 0

    for machine in machines:
        v = [Int(f"b{i}") for i in range(len(machine.buttons))]
        s = Optimize()
        s.add(*[i >= 0 for i in v])
        for j_pos, j in enumerate(machine.joltages):
            s.add(Sum((v[idx] for idx, btn in enumerate(machine.buttons) if j_pos in btn)) == j)
        s.minimize(Sum(v))

        if s.check() == sat:
            result = s.model()
            fewest_presses = sum(result[i].as_long() for i in v)
            # print(fewest_presses)
            total_presses += fewest_presses

    return total_presses
