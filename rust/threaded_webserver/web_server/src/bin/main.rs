use web_server;
use std::thread;

fn main() {
    println!("thread id: {:?}", thread::current().id());
    let mut server = web_server::WebServer::new(28080);
    server.start();
    server.join().unwrap();
}
