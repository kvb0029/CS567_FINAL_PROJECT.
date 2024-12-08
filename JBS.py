from datetime import datetime

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # "employer" or "freelancer"
        self.jobs_posted = []  # Only for employers
        self.bids = []  # Only for freelancers


class Job:
    def __init__(self, title, description, budget, deadline, employer):
        self.title = title
        self.description = description
        self.budget = budget
        self.deadline = deadline
        self.employer = employer
        self.bids = []
        self.selected_bid = None
        self.status = "Open"  # Default status


class Bid:
    def __init__(self, amount, freelancer, message):
        self.amount = amount
        self.freelancer = freelancer
        self.message = message


class JobBiddingSystem:
    def __init__(self):
        self.users = {}
        self.jobs = []
        self.logged_in_user = None

    def register_user(self, username, password, role):
        if username in self.users:
            print("Username already exists. Please choose a different username.")
            return
        if role not in ["employer", "freelancer"]:
            print("Invalid role. Please choose 'employer' or 'freelancer'.")
            return
        self.users[username] = User(username, password, role)
        print(f"User {username} registered successfully as a {role}.")

    def login_user(self, username, password):
        if username not in self.users or self.users[username].password != password:
            print("Invalid username or password.")
            return
        self.logged_in_user = self.users[username]
        print(f"User {username} logged in successfully.")

    def logout_user(self):
        if self.logged_in_user:
            print(f"User {self.logged_in_user.username} logged out.")
            self.logged_in_user = None
        else:
            print("No user is currently logged in.")

    def post_job(self, title, description, budget, deadline):
        if not self.logged_in_user or self.logged_in_user.role != "employer":
            print("Only employers can post jobs.")
            return
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            if deadline_date < datetime.now():
                print("Deadline must be a future date.")
                return
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        job = Job(title, description, budget, deadline, self.logged_in_user)
        self.jobs.append(job)
        self.logged_in_user.jobs_posted.append(job)
        print(f"Job '{title}' posted successfully.")

    def view_jobs(self):
        if not self.jobs:
            print("No jobs available.")
            return
        print("\nAvailable Jobs:")
        for i, job in enumerate(self.jobs, start=1):
            print(f"{i}. {job.title} | Budget: {job.budget} | Deadline: {job.deadline}")
            print(f"   Description: {job.description}")
            print(f"   Employer: {job.employer.username}")
        print()

    def place_bid(self, job_index, amount, message):
        if not self.logged_in_user or self.logged_in_user.role != "freelancer":
            print("Only freelancers can place bids.")
            return
        if job_index < 1 or job_index > len(self.jobs):
            print("Invalid job selection.")
            return
        job = self.jobs[job_index - 1]
        if datetime.strptime(job.deadline, "%Y-%m-%d") < datetime.now():
            print("The job deadline has passed. You cannot bid on this job.")
            return
        bid = Bid(amount, self.logged_in_user, message)
        job.bids.append(bid)
        self.logged_in_user.bids.append(bid)
        print(f"Bid placed successfully on job '{job.title}'.")

    def view_bids(self, job_index):
        if not self.logged_in_user or self.logged_in_user.role != "employer":
            print("Only employers can view bids.")
            return
        if job_index < 1 or job_index > len(self.jobs):
            print("Invalid job selection.")
            return
        job = self.jobs[job_index - 1]
        if job.employer != self.logged_in_user:
            print("You can only view bids on your own jobs.")
            return
        if not job.bids:
            print(f"No bids placed on job '{job.title}'.")
            return
        print(f"Bids for job '{job.title}':")
        for i, bid in enumerate(job.bids, start=1):
            print(f"{i}. {bid.freelancer.username} | Amount: {bid.amount}")
            print(f"   Message: {bid.message}")
        print()

    def select_bid(self, job_index, bid_index):
        if not self.logged_in_user or self.logged_in_user.role != "employer":
            print("Only employers can select bids.")
            return
        if job_index < 1 or job_index > len(self.jobs):
            print("Invalid job selection.")
            return
        job = self.jobs[job_index - 1]
        if job.employer != self.logged_in_user:
            print("You can only select bids for your own jobs.")
            return
        if bid_index < 1 or bid_index > len(job.bids):
            print("Invalid bid selection.")
            return
        job.selected_bid = job.bids[bid_index - 1]
        print(f"Bid selected for job '{job.title}':")
        print(f"Freelancer: {job.selected_bid.freelancer.username}, Amount: {job.selected_bid.amount}")

    def update_job_status(self, job_index, status):
        if not self.logged_in_user or self.logged_in_user.role != "employer":
            print("Only employers can update job status.")
            return
        if job_index < 1 or job_index > len(self.jobs):
            print("Invalid job selection.")
            return
        job = self.jobs[job_index - 1]
        if job.employer != self.logged_in_user:
            print("You can only update the status of your own jobs.")
            return
        if status not in ["Open", "In Progress", "Completed"]:
            print("Invalid status. Choose 'Open', 'In Progress', or 'Completed'.")
            return
        job.status = status
        print(f"Job '{job.title}' status updated to '{status}'.")

    def search_jobs(self, keyword=None, min_budget=None, max_budget=None):
        filtered_jobs = self.jobs
        if keyword:
            filtered_jobs = [job for job in filtered_jobs if keyword.lower() in job.title.lower()]
        if min_budget is not None:
            filtered_jobs = [job for job in filtered_jobs if job.budget >= min_budget]
        if max_budget is not None:
            filtered_jobs = [job for job in filtered_jobs if job.budget <= max_budget]
        if not filtered_jobs:
            print("No jobs found matching your criteria.")
            return []
        print("\nSearch Results:")
        for job in filtered_jobs:
            print(f"{job.title} | Budget: {job.budget} | Deadline: {job.deadline}")
            print(f"   Description: {job.description}")
        return filtered_jobs

    def make_payment(self, job_index, amount):
        if not self.logged_in_user or self.logged_in_user.role != "employer":
            print("Only employers can make payments.")
            return
        if job_index < 1 or job_index > len(self.jobs):
            print("Invalid job selection.")
            return
        job = self.jobs[job_index - 1]
        if job.selected_bid is None or job.employer != self.logged_in_user:
            print("No selected bid found for this job.")
            return
        if amount != job.selected_bid.amount:
            print(f"Payment amount must match the bid amount: {job.selected_bid.amount}.")
            return
        print(f"Payment of {amount} made to freelancer {job.selected_bid.freelancer.username} for job '{job.title}'.")
