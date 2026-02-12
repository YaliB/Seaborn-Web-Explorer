# Seaborn Web Explorer

An interactive system for data display and visualization with dynamic filtering, based on FastAPI, Pandas, and Seaborn.

## Requirements
- Python 3.10+
- See requirement.txt for all dependencies

## Local Run Instructions
1. Install dependencies:
   ```
   pip install -r requirement.txt
   ```
2. Start the server:
   ```
   uvicorn main:app --reload
   ```
3. Open your browser at:
   http://localhost:8000

## Project Structure
- main.py — Main entry point
- routers/ — Routers for data, pages, and questions
- services/ — Data processing and analysis services
- static/ — Styling files and plots
- templates/ — HTML templates

## Notes
- Make sure the .gitignore file includes all files that should not be committed to git (system files, environments, plots, etc.).
- It is recommended to add more documentation as needed.
