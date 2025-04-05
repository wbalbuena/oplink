import unittest
import json
from datetime import datetime, timedelta
from app import app, db, Job

class TestMethods(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client() # test client for Flask

        with app.app_context():
            db.create_all()

            test_jobs = [
                Job(
                    company="Test Company 1",
                    title="Software Engineer",
                    location="San Francisco, CA",
                    time=datetime.now().strftime("%Y-%m-%d %H:%M"),
                    retrieved=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    link="https://example.com/job1",
                    description="Test job description 1",
                    job_id="JOB123"
                ),
                Job(
                    company="Test Company 2",
                    title="Data Scientist",
                    location="New York, NY",
                    time=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
                    retrieved=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
                    link="https://example.com/job2",
                    description="Test job description 2",
                    job_id="JOB456"
                )
            ]
            db.session.add_all(test_jobs)
            db.session.commit()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    # checks if the most recent job is returned
    def test_recent_job(self):
        response = self.client.get('/recent')
        data = json.loads(response.data)
        self.assertIn('retrieved', data)
        self.assertTrue(len(data['retrieved']) > 0)

    # checks if both test jobs are shown
    def test_get_jobs_no_filters(self):
        response = self.client.get('/jobs')
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
    
    # checks company search functionality
    def test_get_jobs_company_filter(self):
        response = self.client.get('/jobs?company=Test Company 1')
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['company'], 'Test Company 1')
    
    # checks title search functionality
    def test_get_jobs_title_filter(self):
        response = self.client.get('/jobs?title=data')
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Data Scientist')
    
    # checks state filter
    def test_get_jobs_state_filter(self):
        response = self.client.get('/jobs?state=CA')
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['location'], 'San Francisco, CA')
    
    # tests sorting by time desc and asc
    def test_get_jobs_sorting(self):
        # descending order
        response = self.client.get('/jobs?sort=time')
        data = json.loads(response.data)
        self.assertEqual(data[0]['company'], 'Test Company 1')  # Most recent first
        
        # ascending order
        response = self.client.get('/jobs?sort=time&order=asc')
        data = json.loads(response.data)
        self.assertEqual(data[0]['company'], 'Test Company 2')  # Oldest first

if __name__ == '__main__':
    unittest.main()