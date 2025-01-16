/**
 * Creates push notification jobs in the given queue.
 * @param {Array} jobs - Array of job objects containing phoneNumber and message.
 * @param {Object} queue - Kue queue instance.
 * @throws {Error} If jobs is not an array.
 */
function createPushNotificationsJobs(jobs, queue) {
  // Check if jobs is an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // Create a job for each item in the jobs array
  jobs.forEach(jobData => {
    const job = queue.create('push_notification_code_3', jobData).save(err => {
      if (err) {
        console.log(`Notification job failed: ${err}`);
      } else {
        console.log(`Notification job created: ${job.id}`);
      }
    });

    // Track job progress
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    job.on('failed', errorMessage => {
      console.log(`Notification job ${job.id} failed: ${errorMessage}`);
    });

    job.on('progress', (progress, total) => {
      const percent = (progress / total) * 100;
      console.log(
        `Notification job ${job.id} ${Math.round(percent)}% complete`
      );
    });
  });
}

export default createPushNotificationsJobs;
