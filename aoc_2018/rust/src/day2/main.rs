use std::{collections::HashMap, env};

use utils::config;

fn parse_input(input_text: &str) -> Vec<String> {
    input_text
        .split('\n')
        .map(|s| s.trim().to_string())
        .collect::<Vec<String>>()
}

fn calculate_checksum(box_ids: &[String]) -> u64 {
    let mut double_counts = 0_u64;
    let mut triple_counts = 0_u64;

    box_ids.iter().for_each(|box_id| {
        let mut count_tracker = HashMap::<char, u64>::new();

        box_id.chars().for_each(|letter| {
            count_tracker
                .entry(letter)
                .and_modify(|c| *c += 1)
                .or_insert(1);
        });

        count_tracker
            .values()
            .any(|c| *c == 2)
            .then(|| double_counts += 1);

        count_tracker
            .values()
            .any(|c| *c == 3)
            .then(|| triple_counts += 1);
    });

    double_counts
        .checked_mul(triple_counts)
        .expect("Checksum overflow!")
}

fn find_common_letters(box_ids: &[String]) -> String {
    let mut box_iter = box_ids.iter().enumerate();
    let total_box_ids = box_ids.len();

    loop {
        if let Some((i, box_id)) = box_iter.next() {
            if let Some(matching_box_id) = ((i + 1)..total_box_ids)
                .map(|j| box_ids.get(j).unwrap())
                .find(|other_box_id| {
                    box_id
                        .chars()
                        .zip(other_box_id.chars())
                        .fold(0, |acc, pair| if pair.0 != pair.1 { acc + 1 } else { acc })
                        == 1
                })
            {
                break box_id
                    .chars()
                    .zip(matching_box_id.chars())
                    .filter(|pair| pair.0 == pair.1)
                    .map(|pair| pair.0)
                    .collect::<String>();
            }
        } else {
            // iterator ended
            break String::from("");
        }
    }
}

fn main() {
    let cli_args: Vec<String> = env::args().collect();
    let conf = config::get_config(&cli_args);
    let input_text = conf.get_input_text();
    let box_ids = parse_input(&input_text);

    // part-1: checksum
    let checksum = calculate_checksum(&box_ids);
    println!("Day 2, Part-1: {checksum}");

    let common_letters = find_common_letters(&box_ids);
    println!("Day 2, Part-2: {common_letters}");
}

#[cfg(test)]
mod tests {
    use super::{calculate_checksum, find_common_letters};

    #[test]
    fn test_calculate_checksum() {
        let box_ids = vec![
            "abcdef".to_string(),
            "bababc".to_string(),
            "abbcde".to_string(),
            "abcccd".to_string(),
            "aabcdd".to_string(),
            "abcdee".to_string(),
            "ababab".to_string(),
        ];
        assert!(calculate_checksum(&box_ids) == 12);
    }

    #[test]
    fn test_find_common_letters() {
        let box_ids = vec![
            "abcde".to_string(),
            "fghij".to_string(),
            "klmno".to_string(),
            "pqrst".to_string(),
            "fguij".to_string(),
            "axcye".to_string(),
            "wvxyz".to_string(),
        ];
        assert!(find_common_letters(&box_ids) == *"fgij");
    }
}
