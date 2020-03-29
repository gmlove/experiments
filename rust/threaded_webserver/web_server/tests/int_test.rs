use rand;
use rand::Rng;
use std::{thread, time};
use web_server;
use reqwest;
use futures::join;
use futures::executor::block_on;
use tokio::runtime::Runtime;

#[test]
fn start_web_server() {
    let port = rand::thread_rng().gen_range(50000, 60000);
    let mut server = web_server::WebServer::new(port);

    server.start();
    thread::sleep(time::Duration::from_secs(1));

    let client = reqwest::Client::builder()
        .no_proxy().build().unwrap();

    let test_gets = futures::future::join_all(
        (0..10).map(|_|
            futures::future::FutureExt::boxed(async {
                let resp = client.get(&format!("http://localhost:{}/health", port)).send().await.unwrap().text().await.unwrap();
                println!("got result: {}", resp);
                resp
            })
        ));

    Runtime::new().unwrap().block_on(test_gets);

    println!("int test end");
}