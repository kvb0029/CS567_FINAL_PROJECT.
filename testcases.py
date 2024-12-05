import unittest
from job_bidding_system import JobBiddingSystem  # Replace with the correct filename

class TestJobBiddingSystem(unittest.TestCase):
    def setUp(self):
        self.system = JobBiddingSystem()
    
    def test_register_user(self):
        self.system.register_user("test_user", "password123", "freelancer")
        self.assertIn("test_user", self.system.users)
        self.assertEqual(self.system.users["test_user"].role, "freelancer")
    
    def test_prevent_duplicate_registration(self):
        self.system.register_user("test_user", "password123", "freelancer")
        self.system.register_user("test_user", "password456", "employer")
        self.assertEqual(len(self.system.users), 1)  # No duplicate allowed
    
    def test_post_job(self):
        self.system.register_user("employer1", "password123", "employer")
        self.system.login_user("employer1", "password123")
        self.system.post_job("Test Job", "This is a test job.", 500, "2024-12-31")
        self.assertEqual(len(self.system.jobs), 1)
        self.assertEqual(self.system.jobs[0].title, "Test Job")
    
    def test_place_bid(self):
        self.system.register_user("employer1", "password123", "employer")
        self.system.register_user("freelancer1", "password456", "freelancer")
        self.system.login_user("employer1", "password123")
        self.system.post_job("Test Job", "This is a test job.", 500, "2024-12-31")
        self.system.logout_user()
        self.system.login_user("freelancer1", "password456")
        self.system.place_bid(1, 450, "I can do this job.")
        self.assertEqual(len(self.system.jobs[0].bids), 1)
        self.assertEqual(self.system.jobs[0].bids[0].amount, 450)
    
    def test_prevent_bid_after_deadline(self):
        self.system.register_user("employer1", "password123", "employer")
        self.system.register_user("freelancer1", "password456", "freelancer")
        self.system.login_user("employer1", "password123")
        self.system.post_job("Test Job", "This is a test job.", 500, "2023-01-01")
        self.system.logout_user()
        self.system.login_user("freelancer1", "password456")
        with self.assertRaises(Exception):  # Custom error handling in your main code
            self.system.place_bid(1, 450, "I can do this job.")

if __name__ == "__main__":
    unittest.main()
