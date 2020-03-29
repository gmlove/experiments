extern crate libc;

#[link(name = "double")]
extern {
    fn double_input(input: libc::c_int) -> libc::c_int;
}

pub mod double {
    use crate::double_input;

    pub fn double(input: i32) -> i32 {
        unsafe { double_input(input) }
    }

}