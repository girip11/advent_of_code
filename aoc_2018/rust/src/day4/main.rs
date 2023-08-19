use std::collections::HashMap;

use std::{env, iter};

use utils::config;

enum GuardState {
    Asleep { minute: u8 },
    Awake { minute: u8 },
}

struct Observation {
    guard_id: u64,
    states: Vec<GuardState>,
}

impl Observation {
    fn get_minutes_slept(&self) -> Vec<u8> {
        let mut time_slept = Vec::<u8>::new();
        let mut last_slept: Option<u8> = None;

        for state in self.states.iter() {
            match state {
                GuardState::Asleep { minute } => last_slept = Some(*minute),
                GuardState::Awake { minute } => {
                    if let Some(prev_minute) = last_slept {
                        time_slept.extend(prev_minute..*minute);
                        last_slept = None;
                    }
                }
            };
        }

        if let Some(prev_minute) = last_slept {
            time_slept.extend(prev_minute..60);
        }

        time_slept
    }
}

fn get_observation_time(record: &str) -> (u8, u8) {
    let mut parts = record[record.find(' ').unwrap() + 1..record.find(']').unwrap()].split(':');
    (
        parts.next().unwrap().parse::<u8>().unwrap(),
        parts.next().unwrap().parse::<u8>().unwrap(),
    )
}

fn parse_input(input_text: &str) -> Vec<Observation> {
    // [1518-11-01 00:00] Guard #10 begins shift
    // [1518-11-01 00:05] falls asleep
    // [1518-11-01 00:25] wakes up
    let mut observations = Vec::<Observation>::new();
    let mut entry_id: usize = 0;
    let mut records = input_text
        .split('\n')
        .map(|r| r.to_string())
        .collect::<Vec<String>>();
    records.sort();

    for record in records.iter() {
        match record.split(']').last().unwrap().trim() {
            shift_start if shift_start.starts_with("Guard") => {
                entry_id += 1;
                let guard_id = shift_start
                    .split_whitespace()
                    .nth(1)
                    .unwrap()
                    .trim_start_matches('#')
                    .parse::<u64>()
                    .unwrap();
                observations.push(Observation {
                    guard_id,
                    states: Vec::<GuardState>::new(),
                });
            }
            asleep if asleep.starts_with("falls") => {
                let (_, minute) = get_observation_time(record);
                observations[entry_id - 1]
                    .states
                    .push(GuardState::Asleep { minute });
            }
            awake if awake.starts_with("wakes") => {
                let (_, minute) = get_observation_time(record);
                observations[entry_id - 1]
                    .states
                    .push(GuardState::Awake { minute });
            }
            _ => (),
        }
    }

    observations
}

fn compute_guard_sleep_chart(observations: &[Observation]) -> HashMap<u64, Vec<u64>> {
    let mut guards_sleep_chart = HashMap::<u64, Vec<u64>>::new();

    observations.iter().for_each(|obs| {
        let minutes_slept = obs.get_minutes_slept();

        let value = guards_sleep_chart
            .entry(obs.guard_id)
            .or_insert(iter::repeat(0_u64).take(60).collect::<Vec<u64>>());

        minutes_slept
            .iter()
            .for_each(|min| value[*min as usize] += 1);
    });

    guards_sleep_chart
}

fn find_most_sleepy_guard(guards_sleep_chart: &HashMap<u64, Vec<u64>>) -> u64 {
    let (guard_id, sleep_times) = guards_sleep_chart
        .iter()
        .max_by(|a, b| a.1.iter().sum::<u64>().cmp(&b.1.iter().sum()))
        .unwrap();

    println!(
        "Most sleepy guard {guard_id}, {}",
        sleep_times.iter().sum::<u64>()
    );

    let most_slept_minute_freq = sleep_times.iter().max().unwrap();
    let most_slept_minute = sleep_times
        .iter()
        .position(|i| *i == *most_slept_minute_freq)
        .unwrap() as u64;

    println!(
        "Most slept minute: {} with frequency: {}",
        most_slept_minute, most_slept_minute_freq
    );

    guard_id.checked_mul(most_slept_minute).unwrap()
}

fn find_most_sleepy_minute(guards_sleep_chart: &HashMap<u64, Vec<u64>>) -> u64 {
    let (guard_id, (minute, freq)) = guards_sleep_chart
        .iter()
        .map(|(guard_id, sleep_times)| {
            (
                guard_id,
                sleep_times
                    .iter()
                    .enumerate()
                    .max_by(|a, b| a.1.cmp(b.1))
                    .unwrap(),
            )
        })
        .max_by(|a, b| a.1 .1.cmp(b.1 .1))
        .unwrap();

    println!("{guard_id} was the most sleepiest on minute {minute} with frequency {freq}");
    guard_id
        .checked_mul(u64::try_from(minute).unwrap())
        .unwrap()
}

fn main() {
    let cli_args: Vec<String> = env::args().collect();
    let conf = config::get_config(&cli_args);
    let input_text = conf.get_input_text();
    let observations = parse_input(&input_text);
    println!("Total observations: {}", observations.len());
    let guards_sleep_times = compute_guard_sleep_chart(&observations);
    println!(
        "Day-4, Part-1: {}",
        find_most_sleepy_guard(&guards_sleep_times)
    );
    println!(
        "Day-4, Part-2: {}",
        find_most_sleepy_minute(&guards_sleep_times)
    );
}

#[cfg(test)]
mod tests {

    use super::{
        compute_guard_sleep_chart, find_most_sleepy_guard, find_most_sleepy_minute, parse_input,
    };

    #[test]
    fn test_find_most_sleepy_guard() {
        let input_text = "[1518-11-01 00:00] Guard #10 begins shift\n
[1518-11-01 00:05] falls asleep\n
[1518-11-01 00:25] wakes up\n
[1518-11-01 00:30] falls asleep\n
[1518-11-01 00:55] wakes up\n
[1518-11-01 23:58] Guard #99 begins shift\n
[1518-11-02 00:40] falls asleep\n
[1518-11-02 00:50] wakes up\n
[1518-11-03 00:05] Guard #10 begins shift\n
[1518-11-03 00:24] falls asleep\n
[1518-11-03 00:29] wakes up\n
[1518-11-04 00:02] Guard #99 begins shift\n
[1518-11-04 00:36] falls asleep\n
[1518-11-04 00:46] wakes up\n
[1518-11-05 00:03] Guard #99 begins shift\n
[1518-11-05 00:45] falls asleep\n
[1518-11-05 00:55] wakes up";
        assert!(
            find_most_sleepy_guard(&compute_guard_sleep_chart(&parse_input(input_text))) == 240
        );
    }

    #[test]
    fn test_find_most_sleepy_minute() {
        let input_text = "[1518-11-01 00:00] Guard #10 begins shift\n
[1518-11-01 00:05] falls asleep\n
[1518-11-01 00:25] wakes up\n
[1518-11-01 00:30] falls asleep\n
[1518-11-01 00:55] wakes up\n
[1518-11-01 23:58] Guard #99 begins shift\n
[1518-11-02 00:40] falls asleep\n
[1518-11-02 00:50] wakes up\n
[1518-11-03 00:05] Guard #10 begins shift\n
[1518-11-03 00:24] falls asleep\n
[1518-11-03 00:29] wakes up\n
[1518-11-04 00:02] Guard #99 begins shift\n
[1518-11-04 00:36] falls asleep\n
[1518-11-04 00:46] wakes up\n
[1518-11-05 00:03] Guard #99 begins shift\n
[1518-11-05 00:45] falls asleep\n
[1518-11-05 00:55] wakes up";
        assert!(
            find_most_sleepy_minute(&compute_guard_sleep_chart(&parse_input(input_text))) == 4455
        );
    }
}
