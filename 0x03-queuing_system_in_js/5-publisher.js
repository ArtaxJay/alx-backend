import { createClient } from 'redis';

const publisher = createClient();

// Event listener for successful connection
publisher.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for connection errors
publisher.on('error', err => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

const publishMessage = (message, time) => {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    publisher.publish('ALXchannel', message);
  }, time);
};

// Publish messages
publishMessage('ALX Student #1 starts course', 100);
publishMessage('ALX Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('ALX Student #3 starts course', 400);
