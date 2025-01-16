import express from 'express';
import redis from 'redis';
import util from 'util';
import kue from 'kue';

// Set up Redis client and promisify the methods
const client = redis.createClient();
client.get = util.promisify(client.get);
client.set = util.promisify(client.set);

// Create an Express server
const app = express();
const port = 1245;

// Set up Kue queue
const queue = kue.createQueue();

// Initialize reservationEnabled and available seats
let reservationEnabled = true;
const initialSeats = 50;
let availableSeats = initialSeats;

// Function to reserve a seat in Redis
const reserveSeat = async number => {
  await client.set('available_seats', number);
};

// Function to get current available seats from Redis
const getCurrentAvailableSeats = async () => {
  const seats = await client.get('available_seats');
  return seats ? parseInt(seats, 10) : 0;
};

// Route to check available seats
app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats.toString() });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat', {}).save(err => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', result => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', err => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

// Route to process the queue and update seat availability
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  const job = await queue.process('reserve_seat', async (job, done) => {
    const seats = await getCurrentAvailableSeats();
    if (seats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    const updatedSeats = seats - 1;
    await reserveSeat(updatedSeats);

    if (updatedSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Start the Express server and initialize the number of available seats
app.listen(port, async () => {
  await reserveSeat(initialSeats); // Set initial available seats to 50
  console.log(`Server running at http://localhost:${port}`);
});
