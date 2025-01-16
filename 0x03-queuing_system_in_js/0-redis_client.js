import { createClient } from 'redis';

const client = createClient();

// Event listener for successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for connection errors
client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});
