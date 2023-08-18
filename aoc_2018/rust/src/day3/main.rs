use std::iter;
use std::{collections::HashSet, env, hash::Hash};

use utils::config;

#[derive(PartialEq, Debug, Eq, Hash)]
struct Position {
    x: u64,
    y: u64,
}

#[derive(PartialEq, Debug)]
struct ElfClaim {
    claim_id: u64,
    left_top_vertex: Position,
    width: u64,
    height: u64,
}

impl ElfClaim {
    fn default() -> Self {
        ElfClaim {
            claim_id: 0,
            left_top_vertex: Position { x: 0, y: 0 },
            width: 0,
            height: 0,
        }
    }

    fn from(claim_text: &str) -> Self {
        // Each claim input looks like #1 @ 108,350: 22x29
        claim_text
            .split_whitespace()
            .enumerate()
            .fold(ElfClaim::default(), |claim, (i, part)| match i {
                0 => {
                    let claim_id = part
                        .chars()
                        .skip(1)
                        .collect::<String>()
                        .parse::<u64>()
                        .unwrap();
                    ElfClaim { claim_id, ..claim }
                }
                2 => {
                    let left_top_vertex = part
                        .trim_end_matches(':')
                        .split(',')
                        .map(|c| c.parse::<u64>().unwrap())
                        .collect::<Vec<u64>>();

                    ElfClaim {
                        left_top_vertex: Position {
                            x: left_top_vertex[0],
                            y: left_top_vertex[1],
                        },
                        ..claim
                    }
                }
                3 => {
                    let dimension = part
                        .split('x')
                        .map(|d| d.parse::<u64>().unwrap())
                        .collect::<Vec<u64>>();

                    ElfClaim {
                        width: dimension[0],
                        height: dimension[1],
                        ..claim
                    }
                }
                _ => claim,
            })
    }
}

struct SantaFabric {
    rows: Vec<Vec<HashSet<u64>>>,
}

impl SantaFabric {
    fn from(width: u64, height: u64) -> Self {
        let cols: Vec<HashSet<u64>> = iter::repeat(HashSet::<u64>::new())
            .take(usize::try_from(height).unwrap())
            .collect();

        SantaFabric {
            rows: iter::repeat(cols)
                .take(usize::try_from(width).unwrap())
                .collect(),
        }
    }

    fn fill(&mut self, x_start: u64, x_end: u64, y_start: u64, y_end: u64, claim_id: &u64) {
        (x_start..x_end).for_each(|x| {
            (y_start..y_end).for_each(|y| {
                self.rows[usize::try_from(x).unwrap()][usize::try_from(y).unwrap()]
                    .insert(*claim_id);
            })
        })
    }

    fn count_positions_with_nclaims(&self, n: usize) -> u64 {
        self.rows.iter().fold(0_u64, |acc, row| {
            acc + row.iter().filter(|entry| entry.len() >= n).count() as u64
        })
    }

    fn find_unique_claim(&self, claims: &mut HashSet<u64>) {
        self.rows.iter().for_each(|row| {
            row.iter().for_each(|entry| {
                if entry.len() > 1 {
                    entry.iter().for_each(|claim_id| {
                        claims.remove(claim_id);
                    })
                }
            })
        })
    }
}

fn parse_input(input_text: &str) -> Vec<ElfClaim> {
    input_text
        .split('\n')
        .map(ElfClaim::from)
        .collect::<Vec<ElfClaim>>()
}

fn get_fabric_coverage_from_claims(claims: &[ElfClaim]) -> (u64, u64) {
    (
        claims
            .iter()
            .map(|claim| claim.left_top_vertex.x + claim.width)
            .max()
            .unwrap()
            + 1,
        claims
            .iter()
            .map(|claim| claim.left_top_vertex.y + claim.height)
            .max()
            .unwrap()
            + 1,
    )
}

fn mark_elf_claims_on_fabric(claims: &[ElfClaim]) -> SantaFabric {
    let (x_max, y_max) = get_fabric_coverage_from_claims(claims);
    let mut fabric_cloth = SantaFabric::from(x_max, y_max);
    claims.iter().for_each(|claim| {
        fabric_cloth.fill(
            claim.left_top_vertex.x,
            claim.left_top_vertex.x + claim.width,
            claim.left_top_vertex.y,
            claim.left_top_vertex.y + claim.height,
            &claim.claim_id,
        );
    });

    fabric_cloth
}

fn compute_total_overlapping_positions(santa_fabric: &SantaFabric) -> u64 {
    santa_fabric.count_positions_with_nclaims(2_usize)
}

fn find_unique_elf_claim(claims: &[ElfClaim], santa_fabric: &SantaFabric) -> u64 {
    let mut claim_ids = HashSet::from_iter(claims.iter().map(|claim| claim.claim_id));
    santa_fabric.find_unique_claim(&mut claim_ids);
    claim_ids.iter().last().unwrap().to_owned()
}

fn main() {
    let cli_args: Vec<String> = env::args().collect();
    let conf = config::get_config(&cli_args);
    let input_text = conf.get_input_text();
    let elf_claims = parse_input(&input_text);
    println!("Total claims: {}", elf_claims.len());

    let (x_max, y_max) = get_fabric_coverage_from_claims(&elf_claims);
    println!("Fabric coverage: {x_max}, {y_max}");

    let santa_fabric = mark_elf_claims_on_fabric(&elf_claims);

    // part-1
    let overlapping_positions = compute_total_overlapping_positions(&santa_fabric);
    println!("Day 3, Part-1: {overlapping_positions}");

    // part-2
    let unique_claim_id = find_unique_elf_claim(&elf_claims, &santa_fabric);
    println!("Day 3, Part-2: #{unique_claim_id}");
}

#[cfg(test)]
mod tests {
    use crate::{
        compute_total_overlapping_positions, find_unique_elf_claim, mark_elf_claims_on_fabric,
    };

    use super::{ElfClaim, Position};

    #[test]
    fn test_elfclaim_from() {
        assert!(
            ElfClaim::from("#1 @ 108,350: 22x29")
                == ElfClaim {
                    claim_id: 1,
                    left_top_vertex: Position { x: 108, y: 350 },
                    width: 22,
                    height: 29,
                }
        );
    }

    #[test]
    fn test_compute_total_overlapping_positions() {
        let claims = [
            ElfClaim::from("#1 @ 1,3: 4x4"),
            ElfClaim::from("#2 @ 3,1: 4x4"),
            ElfClaim::from("#3 @ 5,5: 2x2"),
        ];
        let santa_fabric = mark_elf_claims_on_fabric(&claims);
        assert!(compute_total_overlapping_positions(&santa_fabric) == 4);
    }

    #[test]
    fn test_find_unique_elf_claim() {
        let claims = [
            ElfClaim::from("#1 @ 1,3: 4x4"),
            ElfClaim::from("#2 @ 3,1: 4x4"),
            ElfClaim::from("#3 @ 5,5: 2x2"),
        ];
        let santa_fabric = mark_elf_claims_on_fabric(&claims);
        assert!(find_unique_elf_claim(&claims, &santa_fabric) == 3);
    }
}
