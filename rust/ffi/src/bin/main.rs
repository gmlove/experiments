use ffi::double;

fn main() {
    let input = 4;
    let output = double::double(input);
    println!("{} * 2 = {}", input, output);
}
