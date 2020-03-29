use std::io::{Read, Write};
use std::net::TcpListener;
use std::thread;
use std::time;

use rand;
use rand::Rng;

use logger;

use crate::thread_pool::ThreadPool;

mod thread_pool;

pub struct WebServer {
    port: u32,
    driver: Option<thread::JoinHandle<()>>,
}

impl WebServer {

    pub fn new(port: u32) -> WebServer {
        WebServer { port, driver: None, }
    }

    pub fn start(&mut self) {
        logger::info!("try start server at: {}", self.port);
        let listener = TcpListener::bind(&format!("127.0.0.1:{}", self.port)).unwrap();
        logger::info!("server started at: {}", self.port);

        let driver = thread::spawn(move || {
            let mut executor = ThreadPool::new(3);

            for stream in listener.incoming() {
                executor.submit(move || {
                    let mut buf = [0; 500];
                    let mut stream = stream.unwrap();
                    let n = stream.read(&mut buf).unwrap();

//                    let execution_time = rand::thread_rng().gen_range(0, 500);
//                    thread::sleep(time::Duration::from_millis(execution_time));

                    logger::info!("data got: \n{}", String::from_utf8_lossy(&buf[..n]));
                    stream.write("HTTP/1.1 200 OK\r\n\r\n".as_bytes()).unwrap();
                    stream.flush().unwrap();
                }).unwrap_or_else(|err| {
                    logger::error!("submit task to executor failed: {:?}", err);
                })
            }
        });
        self.driver = Some(driver);
        ()
    }

    pub fn join(&mut self) -> thread::Result<()> {
        if let Some(driver) = self.driver.take() {
            driver.join()?;
        }
        Ok(())
    }

}
