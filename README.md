# real-estate-indicator

A simple Flask web application that profiles users based on their investment
preferences and suggests real estate projects in Dubai. After filling out a
questionnaire, users receive a PDF report with a recommended investor/end-user
percentage and example projects.

## Requirements
- Python 3.11+
- Flask
- fpdf

Install dependencies with:
```
pip install Flask fpdf
```

## Running
```
python app.py
```
The server starts on `http://localhost:5000/`.

User submissions are stored in `data/users.csv` and sample projects can be edited
in `data/projects.json`.
