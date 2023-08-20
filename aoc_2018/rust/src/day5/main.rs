use std::collections::HashSet;
use std::env;
use utils::config;

fn initiate_polymer_reaction(polymers: &str) -> Vec<char> {
    let mut reaction_stack = Vec::<char>::new();

    polymers
        .chars()
        .for_each(|poly_in| match reaction_stack.last() {
            Some(poly_top) => match poly_in != *poly_top
                && (poly_in == poly_top.to_ascii_lowercase()
                    || poly_in.to_ascii_lowercase() == *poly_top)
            {
                true => {
                    reaction_stack.pop();
                }
                false => reaction_stack.push(poly_in),
            },
            None => reaction_stack.push(poly_in),
        });

    reaction_stack
}

fn calculate_polymers_remaining_after_reaction(polymers: &str) -> u64 {
    let reaction_stack = initiate_polymer_reaction(polymers);
    u64::try_from(reaction_stack.len()).unwrap()
}

fn improve_polymer_reaction(polymers: &str) -> u64 {
    let mut distinct_polymers = HashSet::<char>::new();

    polymers.chars().for_each(|p| {
        distinct_polymers.insert(p.to_ascii_lowercase());
    });

    let (p_removed, min_length) = distinct_polymers
        .iter()
        .map(|p| {
            let new_polymer = polymers
                .chars()
                .filter(|c| *p != c.to_ascii_lowercase())
                .collect::<String>();
            let reaction_stack = initiate_polymer_reaction(&new_polymer);
            (*p, u64::try_from(reaction_stack.len()).unwrap())
        })
        .min_by_key(|(_p_rem, p_len)| *p_len)
        .unwrap();

    println!("Polymer {p_removed} when removed, yields least length of {min_length}");
    min_length
}

fn main() {
    let cli_args: Vec<String> = env::args().collect();
    let conf = config::get_config(&cli_args);
    let input_text = conf.get_input_text();
    println!(
        "Day-5, Part-1: {}",
        calculate_polymers_remaining_after_reaction(&input_text)
    );
    println!("Day-5, Part-2: {}", improve_polymer_reaction(&input_text));
}

#[cfg(test)]
mod tests {

    use super::{calculate_polymers_remaining_after_reaction, improve_polymer_reaction};

    #[test]
    fn test_calculate_polymers_remaining_after_reaction() {
        let input_text = "dabAcCaCBAcCcaDA";
        assert!(calculate_polymers_remaining_after_reaction(input_text) == 10);
    }

    #[test]
    fn test_improve_polymer_reaction() {
        let input_text = "dabAcCaCBAcCcaDA";
        assert!(improve_polymer_reaction(input_text) == 4);
    }
}
