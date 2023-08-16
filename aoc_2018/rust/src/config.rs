use std::fs;
use std::path;

pub struct Config {
    input_filepath: String,
}

impl Config {
    pub fn new(filepath: &str) -> Self {
        match path::Path::new(filepath).try_exists() {
            Ok(true) => Config {
                input_filepath: filepath.to_string(),
            },
            Ok(false) => panic!("Given input file {filepath} doesnot exist"),
            Err(e) => panic!("Error {e} when checking if {filepath} exists"),
        }
    }

    pub fn get_input_text(&self) -> String {
        fs::read_to_string(&self.input_filepath)
            .expect("Unable to read the input file {self.input_filepath}")
            .trim()
            .to_string()
    }
}

pub fn get_config(cli_args: &[String]) -> Config {
    let filepath = cli_args
        .iter()
        .skip(1)
        .last()
        .expect("Expected to provide the input file for processing.");
    Config::new(filepath)
}
