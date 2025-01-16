import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';
import { expect } from 'chai';

describe('createPushNotificationsJobs', function () {
  let queue;

  beforeEach(() => {
    // Create a Kue queue in test mode
    queue = kue.createQueue({
      testMode: true,
    });
  });

  afterEach(() => {
    // Clear the queue after each test
    queue.testMode = false; // Exit testMode after the test
  });

  it('should display an error message if jobs is not an array', function () {
    try {
      createPushNotificationsJobs('not an array', queue);
    } catch (error) {
      expect(error.message).to.equal('Jobs is not an array');
    }
  });

  it('should create two new jobs to the queue', function (done) {
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account',
      },
    ];

    createPushNotificationsJobs(list, queue);

    // Check that the queue contains two jobs
    setImmediate(() => {
      expect(queue.testMode.jobs.length).to.equal(2); // Ensure 2 jobs were added to the queue

      const job1 = queue.testMode.jobs[0];
      const job2 = queue.testMode.jobs[1];

      // Check job details
      expect(job1.data.phoneNumber).to.equal('4153518780');
      expect(job2.data.phoneNumber).to.equal('4153518781');
      expect(job1.data.message).to.equal(
        'This is the code 1234 to verify your account'
      );
      expect(job2.data.message).to.equal(
        'This is the code 5678 to verify your account'
      );

      done();
    });
  });
});
