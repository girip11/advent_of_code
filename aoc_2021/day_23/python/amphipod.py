import sys
from copy import deepcopy
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Iterator, List, Set


@dataclass(frozen=True)
class Amphipod:
    type_: str
    energy: int

    def __str__(self) -> str:
        return self.type_


EMPTYPOD = Amphipod(".", -1)


@dataclass
class Hallway:
    ALL: ClassVar[List[int]] = list(range(1, 12))
    RESERVED: ClassVar[Set[int]] = {3, 5, 7, 9}
    occupied: Dict[int, Amphipod] = field(default_factory=dict, init=False)

    def __contains__(self, amphipod: Amphipod) -> bool:
        return amphipod in self.occupied.values()

    def get_amphipod_slots(self, amphipod: Amphipod) -> List[int]:
        return [slot for slot, amph in self.occupied.items() if amphipod == amph]

    def move_from_hallway(self, pos: int) -> None:
        if pos in self.occupied:
            self.occupied.pop(pos)

    def move_to_hallway(self, amphipod: Amphipod, pos: int) -> None:
        self.occupied[pos] = amphipod

    def __str__(self) -> str:
        return "".join(self.occupied.get(slot, EMPTYPOD).type_ for slot in Hallway.ALL)


@dataclass
class SideRoom:
    idx: int
    alloted_for: Amphipod
    hallway_slot: int
    room_size: int
    amphipods: List[Amphipod] = field(default_factory=list, init=False)

    @property
    def empty(self) -> bool:
        return len(self.amphipods) == 0

    @property
    def arranged(self) -> bool:
        return len(self.amphipods) == self.room_size and all(
            amphipod == self.alloted_for for amphipod in self.amphipods
        )

    @property
    def disarranged(self) -> bool:
        return not self.empty and any(amphipod != self.alloted_for for amphipod in self.amphipods)

    @property
    def vacant_slots(self) -> int:
        return self.room_size - len(self.amphipods)

    def __getitem__(self, pos: int) -> Amphipod:
        return self.amphipods[pos] if pos < len(self.amphipods) else EMPTYPOD


@dataclass
class Configuration:
    hallway: Hallway
    siderooms: List[SideRoom]
    energy_spent: int = field(default=0)
    # steps: List[str] = field(default_factory=list, init=False)

    def copy(self) -> "Configuration":
        return deepcopy(self)

    def vacant_siderooms(self) -> Iterator[SideRoom]:
        yield from (sideroom for sideroom in self.siderooms if sideroom.vacant_slots)

    def unarranged_siderooms(self) -> Iterator[SideRoom]:
        yield from (sideroom for sideroom in self.siderooms if not sideroom.arranged)

    @property
    def arranged(self) -> bool:
        return all(sideroom.arranged for sideroom in self.siderooms)

    def __str__(self) -> str:
        content: List[str] = ["#############", f"#{self.hallway}#"]
        start = self.siderooms[0].room_size - 1
        for i in range(start, -1, -1):
            s = "#".join(f"{sideroom[i]}" for sideroom in self.siderooms)
            if i == start:
                s = f"###{s}###"
            else:
                s = f"  #{s}#"
            content.append(s)

        content.append("  #########")
        content.append(f"Energy : {self.energy_spent}")

        return "\n".join(content)


def try_filling_from_siderooms(config: Configuration, room_to_fill: SideRoom) -> bool:
    hallway: Hallway = config.hallway
    amphipod_to_fill: Amphipod = room_to_fill.alloted_for
    before_filling: int = len(room_to_fill.amphipods)

    for other_sideroom in config.siderooms:
        if (
            not room_to_fill.arranged
            and not other_sideroom.empty
            and other_sideroom.idx != room_to_fill.idx
            and other_sideroom.amphipods[-1] == amphipod_to_fill
        ):
            dir_to_move: int = 1 if room_to_fill.hallway_slot < other_sideroom.hallway_slot else -1
            hallway_steps = range(
                room_to_fill.hallway_slot,
                other_sideroom.hallway_slot + dir_to_move,
                dir_to_move,
            )

            if all(pos not in hallway.occupied for pos in hallway_steps):
                for amph in other_sideroom.amphipods[::-1]:
                    # if the hallway path is clear, then fill the sideroom
                    if amph == amphipod_to_fill and room_to_fill.vacant_slots > 0:
                        # config.steps.append(
                        #     (
                        #         f"{amphipod_to_fill.type_}, "
                        #         f"S{other_sideroom.idx+1}_{len(other_sideroom.amphipods)} -> "
                        #         f"S{room_to_fill.idx+1}_{len(room_to_fill.amphipods)+1}"
                        #     )
                        # )
                        config.energy_spent += (
                            other_sideroom.vacant_slots
                            + len(hallway_steps)
                            + room_to_fill.vacant_slots
                        ) * amphipod_to_fill.energy
                        room_to_fill.amphipods.append(other_sideroom.amphipods.pop())

    return len(room_to_fill.amphipods) != before_filling


def try_filling_from_hallway(config: Configuration, room_to_fill: SideRoom) -> None:
    hallway: Hallway = config.hallway
    amphipod_to_fill: Amphipod = room_to_fill.alloted_for

    for amphipod_pos in sorted(
        hallway.get_amphipod_slots(amphipod_to_fill),
        key=lambda pos: abs(room_to_fill.hallway_slot - pos),
    ):
        # if we have the corresponding type in the hallway, try moving it to the sideroom
        dir_to_move: int = 1 if amphipod_pos < room_to_fill.hallway_slot else -1
        hallway_steps = range(
            amphipod_pos + dir_to_move, room_to_fill.hallway_slot + dir_to_move, dir_to_move
        )

        # if the position to the sideroom path is clear, then fill the sideroom
        if all(pos not in hallway.occupied for pos in hallway_steps):
            config.energy_spent += (
                len(hallway_steps) + room_to_fill.vacant_slots
            ) * amphipod_to_fill.energy
            # config.steps.append(
            #     (
            #         f"{amphipod_to_fill.type_}, "
            #         f"H{amphipod_pos} -> S{room_to_fill.idx+1}_{len(room_to_fill.amphipods)+1}"
            #     )
            # )
            hallway.move_from_hallway(amphipod_pos)
            room_to_fill.amphipods.append(amphipod_to_fill)


def try_filling_siderooms(config: Configuration) -> None:
    dirty: bool = True
    while dirty:
        dirty = False
        for sideroom in config.vacant_siderooms():
            if sideroom.empty or not sideroom.disarranged:
                # try to fill all the vacant spots of the current room
                # from amphipods either in the hallway or other siderooms
                try_filling_from_hallway(config, sideroom)
                if not sideroom.arranged:
                    dirty = try_filling_from_siderooms(config, sideroom) or dirty


# new configurations to explore
def generate_configurations(configuration: Configuration) -> List[Configuration]:
    configs: List[Configuration] = []

    def create_configs(
        config: Configuration, sideroom_idx: int, search_range: range
    ) -> List[Configuration]:
        configs: List[Configuration] = []
        available_slots: Set[int] = set(Hallway.ALL) - Hallway.RESERVED

        for slot in search_range:
            if slot in config.hallway.occupied:
                break
            if slot in available_slots:
                new_config = config.copy()
                # remove from sideroom and move to the hallway
                sideroom: SideRoom = new_config.siderooms[sideroom_idx]
                # compute the steps moved
                # new_config.steps.append(
                #     (
                #         f"{sideroom.amphipods[-1].type_}, ",
                #         f"S{sideroom.idx+1}_{len(sideroom.amphipods)} -> H{slot}",
                #     )
                # )
                new_config.energy_spent += (
                    sideroom.vacant_slots + abs(slot - sideroom.hallway_slot) + 1
                ) * sideroom.amphipods[-1].energy

                new_config.hallway.move_to_hallway(sideroom.amphipods.pop(), slot)
                configs.append(new_config)

        return configs

    for sideroom in configuration.unarranged_siderooms():
        if sideroom.disarranged:
            # check if pods can be placed to the left in the hallway
            configs.extend(
                create_configs(configuration, sideroom.idx, range(sideroom.hallway_slot - 1, 0, -1))
            )
            # check if pods can be placed to the right in the hallway
            configs.extend(
                create_configs(
                    configuration,
                    sideroom.idx,
                    range(sideroom.hallway_slot + 1, Hallway.ALL[-1] + 1),
                )
            )

    return configs


# Brute force approach with slight optimization by pruning paths
def rearrange_amphipods(configuration: Configuration) -> Configuration:
    best_configuration: Configuration = configuration.copy()
    best_configuration.energy_spent = sys.maxsize
    configs: List[Configuration] = generate_configurations(configuration)

    while configs:
        print(f"New configurations:{len(configs)}")
        current_config = configs.pop()

        if current_config.energy_spent >= best_configuration.energy_spent:
            continue

        try_filling_siderooms(current_config)

        if (
            current_config.arranged
            and current_config.energy_spent < best_configuration.energy_spent
        ):
            best_configuration = current_config
        else:
            configs.extend(
                filter(
                    lambda c: c.energy_spent < best_configuration.energy_spent,
                    generate_configurations(current_config),
                )
            )

    return best_configuration


def parse_input(lines: List[str]) -> Configuration:
    amphipods: Dict[str, Amphipod] = {
        "A": Amphipod("A", 1),
        "B": Amphipod("B", 10),
        "C": Amphipod("C", 100),
        "D": Amphipod("D", 1000),
    }
    hallway: Hallway = Hallway()
    sideroom_amphipods: List[str] = lines[len(lines) - 2 : 1 : -1]
    room_size: int = len(sideroom_amphipods)
    siderooms: List[SideRoom] = [
        SideRoom(0, amphipods["A"], 3, room_size),
        SideRoom(1, amphipods["B"], 5, room_size),
        SideRoom(2, amphipods["C"], 7, room_size),
        SideRoom(3, amphipods["D"], 9, room_size),
    ]

    for line in sideroom_amphipods:
        for i, amphipod in enumerate(line.strip().strip("#").split("#")):
            siderooms[i].amphipods.append(amphipods[amphipod])

    return Configuration(hallway, siderooms)


def main(*args: str) -> None:
    input_lines = sys.stdin.readlines()
    configuration: Configuration = parse_input(input_lines)
    print(configuration)

    # part-1 and part-2
    print(f"Least energy to rearrange amphipods: {rearrange_amphipods(configuration)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
