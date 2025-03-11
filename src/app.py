from flask import Flask, request, jsonify, send_from_directory
from sqlalchemy import create_engine, insert, String, Text, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
import os
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__, static_folder='../dist', template_folder='../dist')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("OPLINK_DATABASE_URL")
db = SQLAlchemy(app)

CORS(app)

class Job(db.Model):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    company: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    time: Mapped[str] = mapped_column(String(255))
    retrieved: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    job_id: Mapped[str] = mapped_column(String(10))

    def __repr__(self) -> str:
        return f'''Job( 
        id={self.id!r}, company={self.company!r}, title={self.title!r}, 
        location={self.location!r}, time={self.time!r}, retrieved={self.retrieved!r}, 
        link={self.link!r}, description={self.description!r}, job_id={self.job_id!r})'''

with app.app_context():
    db.create_all()

# def get_db_connection():
#     #db_path = os.path.join('/var/data/jobs.db')
#     #db_path = os.path.join(os.path.dirname(__file__), '../linkedin-scraper/jobs.db')
#     connection = sqlite3.connect(db_path)
#     connection.row_factory = sqlite3.Row
#     return connection

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.static_folder), 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(os.path.join(app.static_folder), path)

@app.route('/health')
def health_check():
    return 'OK', 200

@app.route('/recent', methods=['GET'])
def get_recent_job():
     recent_job = Job.query.order_by(Job.retrieved.desc()).first()
     if recent_job:
         return jsonify({"retrieved": recent_job.retrieved[:19]})
     else:
         return jsonify({"retrieved": "UNKNOWN"})


@app.route('/jobs', methods=['GET'])
def get_jobs():
    # connection = get_db_connection()
    # cur = connection.cursor()

    sort = request.args.get('sort', 'time')
    order = request.args.get('order', 'desc')
    company = request.args.get('company', '', type=str).lower()
    title = request.args.get('title', '', type=str).lower()
    location = request.args.get('location', '', type=str).lower()
    state = request.args.get('state', '', type=str)

    #query = '''SELECT company, title, location, time, link FROM job WHERE 1=1'''
    query = Job.query

    if company:
        #query += f" AND (LOWER(company) LIKE '%{company}%')"
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if title:
        #query += f" AND (LOWER(title) LIKE '%{title}%')"
        query = query.filter(Job.title.ilike(f"%{title}%"))
    if location:
        #query += f" AND (LOWER(location) LIKE '%{location}%')"
        query = query.filter(Job.location.ilike(f"%{location}%"))

    # restrict job postings to the last week
    seven_days_ago = datetime.now() - timedelta(days=7, hours=7)
    seven_days_ago_str = seven_days_ago.strftime("%Y-%m-%d %H:%M")
    query = query.filter(Job.time >= seven_days_ago_str)

    state_dictionary = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming"
    }

    if state != '':
        #query += f" AND (location LIKE '%, {state}' OR location LIKE '%{state_dictionary[state]}%')"
        query = query.filter(Job.location.like(f'%, {state}') | Job.location.like(f'%{state_dictionary[state]}%'))
    
    #query += f" ORDER BY {sort} {order.upper()}"
    query = query.order_by(getattr(Job, sort).desc() if order == 'desc' else getattr(Job, sort))

    #print(query)

    #jobs = cur.execute(query).fetchall()
    jobs = query.all()
    jobs_list = [{"company": job.company, "title": job.title, "location": job.location, "time": job.time, "link": job.link} for job in jobs]

    #jobs_list = [dict(job) for job in jobs]

    return jsonify(jobs_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)