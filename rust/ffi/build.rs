
fn main() {
    println!("cargo:rustc-link-lib=double");
    println!("cargo:rustc-link-lib=mul");
    println!("cargo:rustc-link-search=native=out_c");
}
