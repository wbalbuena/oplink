# oplink
## Description
https://opl.ink

__oplink__ was made to help computer science graduates connect with relevant entry-level jobs by filtering out hundreds of fluff from other job boards.

This repo is for the web application without the scraping script.

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