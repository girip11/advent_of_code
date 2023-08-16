use std::collections::HashSet;
use std::env;

use utils::config;

fn get_frequences(freq_text: &str) -> Vec<i64> {
    freq_text
        .split('\n')
        .map(|v| v.trim().parse::<i64>().unwrap())
        .collect()
}

fn compute_total_frequency(frequencies: &[i64]) -> i64 {
    frequencies.iter().sum()
}

fn find_first_repeating_frequency(frequencies: &[i64]) -> i64 {
    let mut frequencies_seen = HashSet::<i64>::new();
    let mut freqs = frequencies.iter().cycle();
    let mut total_frequency = 0;
    loop {
        let freq = freqs.next().unwrap();
        total_frequency += freq;
        if frequencies_seen.contains(&total_frequency) {
            break total_frequency;
        }
        frequencies_seen.insert(total_frequency);
    }
}

fn main() {
    let cli_conf = config::get_config(&env::args().collect::<Vec<String>>());
    let input_text = cli_conf.get_input_text();
    let frequencies = get_frequences(&input_text);

    // part-1
    let total_frequency = compute_total_frequency(&frequencies);
    println!("Total frequency: {total_frequency}");

    // part-2
    let repeating_frequency = find_first_repeating_frequency(&frequencies);
    println!("First repeating frequency: {repeating_frequency}");
}
