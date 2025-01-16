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

/**
 * Sets a new key-value pair in Redis
 * @param {string} schoolName - The key
 * @param {string} value - The value
 */
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print); // redis.print logs a confirmation message
}

/**
 * Gets the value of a key from Redis
 * @param {string} schoolName - The key
 */
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.error(`Error fetching value for key ${schoolName}:`, err);
    } else {
      console.log(reply);
    }
  });
}

// Calling the functions
displaySchoolValue('ALX');
setNewSchool('ALXSanFrancisco', '100');
displaySchoolValue('ALXSanFrancisco');
