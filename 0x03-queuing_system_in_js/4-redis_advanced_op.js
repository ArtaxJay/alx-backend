import { createClient, print } from 'redis';

const client = createClient();

// Event listener for successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Event listener for connection errors
client.on('error', err => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Create Hash
const hashKey = 'ALX';
const hashValues = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const [field, value] of Object.entries(hashValues)) {
  client.hset(hashKey, field, value, print); // redis.print logs confirmation
}

// Display Hash
client.hgetall(hashKey, (err, object) => {
  if (err) {
    console.error(`Error fetching hash ${hashKey}:`, err);
  } else {
    console.log(object);
  }
});
