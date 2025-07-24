use clap::Parser;
use wasmer::{Instance, Module, Store, Value, imports};

#[derive(Debug, Parser)]
#[command(
    name = "wasmer-cli",
    version = "1.0",
    about = "A simple Wasmer CLI example"
)]
struct WTR {}

fn main() {
    // Create a new store
    let store = Store::default();

    println!("Hello, world!");
}
