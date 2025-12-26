# Solution to Advent of Code 2025

This year I am trying to solve the advent of code puzzles by writing my solution in the following dialects of python focussed on performance.

- Python and compile to C extension using mypyc.
- Codon JIT - As much as possible.
- Numba JIT - As much as possible.

## Setting up

- `uv pip sync requirements-dev.txt`

## Mypyc

- Compile using mypyc `mypyc <python file path>`
