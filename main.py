from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/multa', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date_str = request.form['start_date']
        line_value = float(request.form['line_value'])
        num_lines = int(request.form['num_lines'])
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = start_date + timedelta(days=730)  # 24 meses
        
        today = datetime.today()
        remaining_months = (end_date.year - today.year) * 12 + end_date.month - today.month
        
        if end_date.day < today.day:
            remaining_months -= 1
        
        total_fine = remaining_months * line_value * num_lines

        end_date_formatted = end_date.strftime('%d/%m/%Y')

        # Verifica se o contrato já venceu
        if today > end_date:
            return render_template('index.html', message="Contrato vencido", end_date=end_date_formatted)

        return render_template('index.html', end_date=end_date_formatted, remaining_months=remaining_months, total_fine=total_fine)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
