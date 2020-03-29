
#[macro_export]
macro_rules! info {
    ($($arg:tt)*) => {{
        extern crate chrono;
        use chrono::prelude::{Local, DateTime};
        let now: DateTime<Local> = Local::now();
        std::println!("[INFO ] [{}] [{}:{}] - {}", now.format("%Y-%m-%d %H:%M:%S").to_string(), std::file!(), std::line!(), std::format!($($arg)*));
    }};
}

#[macro_export]
macro_rules! debug {
    ($($arg:tt)*) => {{
        extern crate chrono;
        use chrono::prelude::{Local, DateTime};
        let now: DateTime<Local> = Local::now();
        std::println!("[DEBUG] [{}] [{}:{}] - {}", now.format("%Y-%m-%d %H:%M:%S").to_string(), std::file!(), std::line!(), std::format!($($arg)*));
    }};
}


#[macro_export]
macro_rules! error {
    ($($arg:tt)*) => {{
        extern crate chrono;
        use chrono::prelude::{Local, DateTime};
        let now: DateTime<Local> = Local::now();
        std::println!("[ERROR] [{}] [{}:{}] - {}", now.format("%Y-%m-%d %H:%M:%S").to_string(), std::file!(), std::line!(), std::format!($($arg)*));
    }};
}
