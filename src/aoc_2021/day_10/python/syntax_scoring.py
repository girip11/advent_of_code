import sys
from typing import List, Mapping, Optional, Set, Tuple

LEGAL_PAIRS: Mapping[str, str] = {"{": "}", "[": "]", "(": ")", "<": ">"}

CHUNK_TYPES: Set[str] = {"{", "[", "(", "<"}

SYNTAX_ERROR_SCORING_TABLE: Mapping[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}

AUTOCOMPLETE_SCORING_TABLE: Mapping[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}


def is_corrupted_line(line: str) -> Tuple[bool, Optional[str]]:
    chunk_tracker: List[str] = []
    is_corrupted: bool = False
    corrupted_chunk: Optional[str] = None

    for chunk in line:
        # opening chunks
        if chunk in CHUNK_TYPES:
            chunk_tracker.append(chunk)
        else:
            # one of the closing chunks
            if LEGAL_PAIRS[chunk_tracker[-1]] == chunk:
                chunk_tracker.pop()
            else:
                is_corrupted = True
                corrupted_chunk = chunk
                break

    return (is_corrupted, corrupted_chunk)


def compute_syntax_score(lines: List[str]) -> int:
    score = 0
    for line in lines:
        is_corrupted, corrupted_chunk = is_corrupted_line(line)
        if is_corrupted:
            score += SYNTAX_ERROR_SCORING_TABLE[corrupted_chunk or ""]
            print(f"Corrupted line: {line} by chunk {corrupted_chunk}")

    return score


def fix_incomplete_line(line: str) -> str:
    chunk_tracker: List[str] = []
    autocompleted_chunks: List[str] = []

    for chunk in line:
        # opening chunks
        if chunk in CHUNK_TYPES:
            chunk_tracker.append(chunk)
        else:
            # one of the closing chunks
            if LEGAL_PAIRS[chunk_tracker[-1]] == chunk:
                chunk_tracker.pop()
            else:
                print("Error the line is incomplete.")
                break

    for chunk in reversed(chunk_tracker):
        autocompleted_chunks.append(LEGAL_PAIRS[chunk])

    return "".join(autocompleted_chunks)


def compute_autocompletion_score(lines: List[str]) -> int:
    autocomplete_line_scores: List[int] = []

    for line in lines:
        if is_corrupted_line(line)[0]:
            continue  # skip the corrupted lines.

        score: int = 0
        autocompleted_chunk = fix_incomplete_line(line)
        for chunk in autocompleted_chunk:
            score = score * 5 + AUTOCOMPLETE_SCORING_TABLE[chunk]

        print(f"AutocompleteLine: {line} autocompleted chunk {autocompleted_chunk} score {score}")
        autocomplete_line_scores.append(score)

    # return the middle score
    autocomplete_line_scores.sort()
    return autocomplete_line_scores[len(autocomplete_line_scores) // 2]


def main(*_: str) -> None:
    lines: List[str] = [line.strip() for line in sys.stdin.readlines()]

    print(lines)
    # part-1
    print(compute_syntax_score(lines))

    # part-2
    print(compute_autocompletion_score(lines))


if __name__ == "__main__":
    main(*sys.argv[1:])
