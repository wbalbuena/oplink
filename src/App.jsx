import { useState, useEffect } from 'react'
import oplinkLogo from './assets/oplink logo.png'
import fluff from './assets/fluff.png'
import './App.css'
import API_BASE_URL from './config';

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [sortField, setSortField] = useState("time");
  const [sortOrder, setSortOrder] = useState("desc");
  const [selectedState, setSelectedState] = useState("");
  const [companySearchTerm, setCompanySearchTerm] = useState("");
  const [titleSearchTerm, setTitleSearchTerm] = useState("");
  const [locationSearchTerm, setLocationSearchTerm] = useState("");
  const [recentJob, setRecentJob] = useState("");
  const [bannerDisplay, setBannerDisplay] = useState(false)

  const fetchJobs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/jobs?sort=${sortField}&order=${sortOrder}&company=${companySearchTerm}&title=${titleSearchTerm}&location=${locationSearchTerm}&state=${selectedState}`)
      const data = await response.json();
      setJobs(data);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [sortField, sortOrder, companySearchTerm, titleSearchTerm, locationSearchTerm, selectedState]);


  const fetchRecentJob = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/recent`);
      const data = await response.json();
      setRecentJob(data);
    } catch (error) {
      console.error('Error fetching recent job: ', error);
    }
  };

  useEffect(() => {
    fetchRecentJob();
  }, []);

  return (
    <>
      <header className="sticky-header">
          <img src={oplinkLogo} className="logo" alt="outlink logo" />
          <a href="https://www.linkedin.com/in/william-balbuena/" target="_blank">Connect With Me!</a>
      </header>
      {bannerDisplay && (
        <div onClick={() => {setBannerDisplay(false)}} className = "moty">
          <p><b>MESSAGE OF THE DAY: 2/25/2025</b></p>
          <p>...</p>
          <p><u>CLICK TO CLOSE</u></p>
        </div>
      )}
      <div className = "blurb">
        <p>oplink was made to help <b>computer science</b> graduates connect with relevant <b>entry-level</b> jobs by filtering out hundreds of fluff from other job boards.</p>
        <p>Jobs shown are from the <b>past week</b> and are refreshed <b>daily</b>!</p>
        <p>Jobs from the following states are available: <b>CA, FL, GA, IL, MA, MD, NY, TX, VA</b></p>
      </div>
      <div className = "ribbon">
        <p><b>LAST UPDATED</b>: {recentJob.retrieved} PST</p>
      </div>
      <div className = "container">
        <Sidebar
          setCompanySearchTerm={setCompanySearchTerm}
          setTitleSearchTerm={setTitleSearchTerm}
          setLocationSearchTerm={setLocationSearchTerm}
          selectedState={selectedState}
          setSelectedState={setSelectedState}
          recentJob={recentJob}
        />
        <div className="cards">
          <div className="card-header">
            <h3 onClick={() => {setSortField("company"); setSortOrder(sortOrder === "desc" ? "asc" : "desc")}}>COMPANY:</h3>
            <h3 onClick={() => {setSortField("title"); setSortOrder(sortOrder === "desc" ? "asc" : "desc")}}>JOB TITLE:</h3>
            <h3 onClick={() => {setSortField("location"); setSortOrder(sortOrder === "desc" ? "asc" : "desc")}}>LOCATION:</h3>
            <h3 onClick={() => {setSortField("time"); setSortOrder(sortOrder === "desc" ? "asc" : "desc")}}>TIME:</h3>
          </div>
          {
            jobs.map((job, index) => (
              <Job
                key = {index}
                company = {job.company}
                title = {job.title}
                location = {job.location}
                time = {job.time}
                link = {job.link}
              />
            ))
          }
        </div>
      </div>
    </>
  )
}

function Sidebar ( { setCompanySearchTerm, setTitleSearchTerm, setLocationSearchTerm, selectedState, setSelectedState, recentJob } ){
  // const states = [
  //   "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
  //   "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
  //   "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
  //   "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
  //   "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
  // ];

  const states = [
    "CA", "FL", "GA", "IL", "MA", "MD", "NY", "TX", "VA"
  ];

  return(
    <>
      <div className = "sidebar">
        <div className = "search">
          <h3>SEARCH</h3>
          <div className = "search-boxes">
            <input type="text" className="search-box" placeholder="COMPANY (e.g. Google)" onChange={(e) => setCompanySearchTerm(e.target.value)}/>
            <input type="text" className="search-box" placeholder="TITLE (e.g. Software Engineer)" onChange={(e) => setTitleSearchTerm(e.target.value)}/>
            <input type="text" className="search-box" placeholder="LOCATION (e.g. Los Angeles)" onChange={(e) => setLocationSearchTerm(e.target.value)}/>
          </div>
        </div>
        <div className = "filters">
          <h3>FILTER</h3>
          <select
            className = "dropdown"
            id="dropdown-box"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
          >
            <option value="" enabled>Select a state...</option>
            {states.map((state, index) => (
              <option key={index} value={state}>
                {state}
              </option>
            ))}
          </select>
        </div>
      </div>
    </>
  )
}

function Job ( { title, company, time, location, link }){
  return (
    <>
      <a href={link} target="_blank">
        <div className="card">
          <h1>{company}</h1>
          <h2>{title}</h2>
          <h3>{location}</h3>
          <h4>{time}</h4>
        </div>
      </a>
    </>
  )
}