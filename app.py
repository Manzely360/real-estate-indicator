from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import json
import csv
import os

app = Flask(__name__)

DATA_FILE = os.path.join('data', 'users.csv')
PROJECT_FILE = os.path.join('data', 'projects.json')

# Ensure data directory exists
os.makedirs('data', exist_ok=True)


def load_projects():
    with open(PROJECT_FILE, 'r') as f:
        return json.load(f)


def save_user(info):
    exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=info.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(info)


def calculate_profile(answers):
    # Basic scoring for demonstration
    investment_score = 0
    enduser_score = 0

    income = float(answers.get('income', 0))
    purchase_power = float(answers.get('purchase_power', 0))
    invest_per_month = float(answers.get('invest_per_month', 0))

    if answers.get('intent') == 'invest':
        investment_score += 2
    else:
        enduser_score += 2

    investment_score += income / 10000 + invest_per_month / 1000
    enduser_score += purchase_power / 100000

    total = investment_score + enduser_score
    if total == 0:
        return 50, 50
    inv_pct = int(100 * investment_score / total)
    end_pct = 100 - inv_pct
    return inv_pct, end_pct


def suggest_projects(area):
    projects = load_projects()
    return [p for p in projects if p['area'].lower() == area.lower()]


def create_pdf(name, investment_pct, enduser_pct, projects):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Real Estate Recommendation', ln=1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Client: {name}', ln=1)
    pdf.cell(0, 10, f'Profile: {investment_pct}% Investor / {enduser_pct}% End-user', ln=1)
    pdf.ln(10)
    for project in projects:
        pdf.cell(0, 10, f"Project: {project['name']} - {project['price']} USD", ln=1)
    report_path = os.path.join('data', 'report.pdf')
    pdf.output(report_path)
    return report_path


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        info = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'income': request.form.get('income'),
            'purchase_power': request.form.get('purchase_power'),
            'invest_per_month': request.form.get('invest_per_month'),
            'intent': request.form.get('intent'),
            'area': request.form.get('area'),
        }
        save_user(info)
        investment_pct, enduser_pct = calculate_profile(info)
        projects = suggest_projects(info['area'])
        report_path = create_pdf(info['name'], investment_pct, enduser_pct, projects)
        return send_file(report_path, as_attachment=True)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
