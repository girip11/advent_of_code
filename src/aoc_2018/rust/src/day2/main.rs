use std::env;

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
        let mut count_tracker = [0_u8; 26];

        box_id.chars().for_each(|letter| {
            count_tracker[letter as usize - 'a' as usize] += 1;
        });

        let (double, triple) = count_tracker
            .iter()
            .map(|c| (*c == 2, *c == 3))
            .fold((false, false), |(d_acc, t_acc), (double, triple)| {
                (d_acc || double, t_acc || triple)
            });

        double.then(|| double_counts += 1);
        triple.then(|| triple_counts += 1);
    });

    double_counts
        .checked_mul(triple_counts)
        .expect("Checksum overflow!")
}

fn find_common_letters(box_ids: &[String]) -> String {
    let mut box_iter = box_ids.iter().enumerate();

    // I did use loop, so that I can terminate the iteration when the
    // solution is found.
    loop {
        if let Some(correct_box_id) = box_iter.next().and_then(|(i, box_id)| {
            box_ids.iter().skip(i + 1).find_map(|other_box_id| {
                (box_id.len() == other_box_id.len())
                    .then(|| {
                        let common = box_id
                            .chars()
                            .zip(other_box_id.chars())
                            .filter_map(|(c1, c2)| (c1 == c2).then_some(c1))
                            .collect::<String>();
                        (box_id.len() - common.len() == 1).then_some(common)
                    })
                    .flatten()
            })
        }) {
            break correct_box_id;
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
    println!("Day 2, Part-2: {}", common_letters);
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
        assert!(find_common_letters(&box_ids) == "fgij");
    }
}
