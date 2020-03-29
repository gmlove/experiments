use std::{mem, thread};
use std::sync::{Arc, mpsc, Mutex};
use std::sync::mpsc::{Receiver, Sender, SendError};
use std::thread::JoinHandle;

use logger;

pub struct ThreadPool {
    thread_channels: Vec<ThreadChannel>,
    message_sender: Sender<Message>,
}

struct ThreadChannel {
    name: String,
    thread: JoinHandle<()>
}


pub enum Message {
    Job(Box<dyn FnOnce() + Send + 'static>),
    Stop
}

impl ThreadPool {
    pub fn new(count: usize) -> ThreadPool {
        let (tx, rx) = mpsc::channel::<Message>();
        let mut threads: Vec<ThreadChannel> = Vec::with_capacity(count);
        let shared_rx = Arc::new(Mutex::new(rx));
        for i in 0..count {
            let thread_name = format!("thread-{}", i + 1);
            let rx = Arc::clone(&shared_rx);
            let thread = thread::spawn(move || {
                ThreadPool::loop_execution(&thread_name, rx);
            });
            let thread = ThreadChannel { name: format!("thread-{}", i + 1), thread };
            threads.push(thread);
        }
        ThreadPool { thread_channels: threads, message_sender: tx }
    }

    fn loop_execution(thread_name: &str, shared_rx: Arc<Mutex<Receiver<Message>>>)
    {
        logger::debug!("thread {} started, waiting for task", thread_name);
        loop {
            let message = shared_rx.lock().unwrap().recv().unwrap();
            match message {
                Message::Job(job) => {
                    logger::debug!("execute job in thread: {}", thread_name);
                    job()
                },
                Message::Stop => {
                    logger::debug!("stop execution for thread: {}", thread_name);
                    break
                },
            }
        }
    }

    pub fn submit<T>(&mut self, f: T) -> Result<(), SendError<Message>>
        where T: FnOnce() + Send + 'static
    {
        logger::debug!("submit task");
        let message = Message::Job(Box::new(f));
        self.message_sender.send(message)
    }

    pub fn stop(&mut self) {
        for _ in 0..self.thread_channels.len() {
            self.message_sender.send(Message::Stop).unwrap_or_else(|err| {
                logger::error!("send stop message to driver failed: {:?}", err);
            })
        }
        for thread_channel in mem::replace(&mut self.thread_channels, vec![]) {
            let thread_name = &thread_channel.name[..];
            thread_channel.thread.join().unwrap_or_else(|err| {
                logger::error!("join thread {} failed: {:?}", thread_name, err)
            });
        }
    }
}

impl Drop for ThreadPool {

    fn drop(&mut self) {
        self.stop();
    }

}


#[cfg(test)]
mod tests {
    use std::time;

    use rand::Rng;

    use super::*;

    #[test]
    fn execute_async_in_thread_pool() {
        let mut thread_pool = ThreadPool::new(5);
        for _ in 0..10 {
            thread_pool.submit(|| {
                logger::debug!("executed here!");
                let some_time = rand::thread_rng().gen_range(0, 500);
                thread::sleep(time::Duration::from_millis(some_time));
            }).unwrap();
        }
        thread::sleep(time::Duration::from_secs(2));
    }
}

