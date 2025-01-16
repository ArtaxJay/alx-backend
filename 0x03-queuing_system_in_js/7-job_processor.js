import kue from 'kue';

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

/**
 * Sends a notification
 * @param {string} phoneNumber - Phone number to send the notification
 * @param {string} message - Message to send
 * @param {object} job - The current job object
 * @param {function} done - Callback to indicate job completion or failure
 */
function sendNotification(phoneNumber, message, job, done) {
  // Start job progress at 0%
  job.progress(0, 100);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  // Simulate some work and track progress to 50%
  job.progress(50, 100);
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`
  );

  // Finish the job successfully
  done();
}

// Create a Kue queue
const queue = kue.createQueue();

// Process jobs from the queue "push_notification_code_2" with a concurrency of 2
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
