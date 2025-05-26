<img src="https://github.com/user-attachments/assets/49c23058-0a01-42d9-9ba8-03388a7bfa35" align="right" height="60" />

## oplink
[__oplink__](https://opl.ink) was made to help computer science graduates connect with relevant entry-level jobs by filtering out hundreds of fluff from other job boards.

🔹 **200+** new computer science jobs daily

🔹 Filters out **100+** unrelated job postings daily

🔹 **Search** by job title, company, and location

🔹 Shows only the **newest** job postings from the past week

🔹 **Sort** results by company, title, location, or time posted

This repo contains the source code for the web application and not for the scraping script.

![oplink](https://github.com/user-attachments/assets/c1aa12c1-18ec-41f4-b3f1-9d1313c3f38d)

## What's being filtered?

Currently the filter targets the following:

🔹 **Unrelated job postings**.  Real examples that I've seen include: nurse, psychologist, janitor, doctor, cashier, resort worker.

🔹 **Third-party job boards** that repost old jobs, presenting them as new.

🔹 Companies that **repost the same job posting** in every location when the actual job requires relocation out-of-state.

## How to Install and Run
1. Install the required libraries
```
windows> pip install -r requirements.txt
```
2. Install [Node.js](https://nodejs.org/en/download)
3. Create an .env file in the /src folder and define a database URL
```
OPLINK_DATABASE_URL=...
```
4. Run the Flask server
```
windows> python src/backend/app.py
```
5. Run the Vite development server
```
windows> npm run dev
```
6. Open the website link in the console
```
http://localhost:5173/
```
