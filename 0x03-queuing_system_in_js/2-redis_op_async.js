import { createClient, print } from 'redis';
import { promisify } from 'util';

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
 * Async function to get the value of a key from Redis
 * @param {string} schoolName - The key
 */
async function displaySchoolValue(schoolName) {
  const getAsync = promisify(client.get).bind(client);
  try {
    const reply = await getAsync(schoolName);
    console.log(reply);
  } catch (err) {
    console.error(`Error fetching value for key ${schoolName}:`, err);
  }
}

// Calling the functions
(async () => {
  await displaySchoolValue('ALX');
  setNewSchool('ALXSanFrancisco', '100');
  await displaySchoolValue('ALXSanFrancisco');
})();
