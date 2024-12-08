import unittest
from datetime import datetime, timedelta
from JBS import JobBiddingSystem, User, Job, Bid

class TestJobBiddingSystem(unittest.TestCase):

    def setUp(self):
        self.system = JobBiddingSystem()
        # Register users
        self.system.register_user("employer1", "password1", "employer")
        self.system.register_user("freelancer1", "password2", "freelancer")

    def test_user_registration(self):
        self.system.register_user("employer2", "password3", "employer")
        self.assertIn("employer2", self.system.users)
        self.assertEqual(self.system.users["employer2"].role, "employer")

    def test_login_logout(self):
        self.system.login_user("employer1", "password1")
        self.assertEqual(self.system.logged_in_user.username, "employer1")
        self.system.logout_user()
        self.assertIsNone(self.system.logged_in_user)

    def test_post_job(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Test Job", "Test Description", 1000.0, future_date)
        self.assertEqual(len(self.system.jobs), 1)
        self.assertEqual(self.system.jobs[0].title, "Test Job")

    def test_view_jobs(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Test Job", "Test Description", 1000.0, future_date)
        self.system.view_jobs()
        self.assertEqual(len(self.system.jobs), 1)

    def test_place_bid(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Test Job", "Test Description", 1000.0, future_date)

        self.system.logout_user()
        self.system.login_user("freelancer1", "password2")
        self.system.place_bid(1, 900.0, "I can complete this job efficiently.")
        self.assertEqual(len(self.system.jobs[0].bids), 1)
        self.assertEqual(self.system.jobs[0].bids[0].freelancer.username, "freelancer1")

    def test_view_bids(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Test Job", "Test Description", 1000.0, future_date)

        self.system.logout_user()
        self.system.login_user("freelancer1", "password2")
        self.system.place_bid(1, 900.0, "I can complete this job efficiently.")

        self.system.logout_user()
        self.system.login_user("employer1", "password1")
        self.system.view_bids(1)
        self.assertEqual(len(self.system.jobs[0].bids), 1)

    def test_select_bid(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Test Job", "Test Description", 1000.0, future_date)

        self.system.logout_user()
        self.system.login_user("freelancer1", "password2")
        self.system.place_bid(1, 900.0, "I can complete this job efficiently.")

        self.system.logout_user()
        self.system.login_user("employer1", "password1")
        self.system.select_bid(1, 1)
        self.assertEqual(self.system.jobs[0].selected_bid.amount, 900.0)

    def test_update_job_status(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Test Job", "Test Description", 1000.0, future_date)
        self.system.update_job_status(1, "In Progress")
        self.assertEqual(self.system.jobs[0].status, "In Progress")

    def test_search_jobs(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Python Developer", "Develop a Python script", 1500.0, future_date)
        self.system.post_job("Web Developer", "Develop a website", 2000.0, future_date)

        self.system.logout_user()
        self.system.login_user("freelancer1", "password2")
        result = self.system.search_jobs(keyword="Python", min_budget=1000)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Python Developer")

    def test_make_payment(self):
        self.system.login_user("employer1", "password1")
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        self.system.post_job("Test Job", "Test Description", 1000.0, future_date)

        self.system.logout_user()
        self.system.login_user("freelancer1", "password2")
        self.system.place_bid(1, 900.0, "I can complete this job efficiently.")

        self.system.logout_user()
        self.system.login_user("employer1", "password1")
        self.system.select_bid(1, 1)
        self.system.make_payment(1, 900.0)
        self.assertEqual(self.system.jobs[0].selected_bid.amount, 900.0)

if __name__ == "__main__":
    unittest.main()
