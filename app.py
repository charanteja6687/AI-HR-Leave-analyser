from flask import Flask, render_template, request, redirect, url_for, jsonify
from leave_analyzer import analyze_leave_request
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Ensure dataset directory exists
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# Initialize CSV file with headers if it doesn't exist
csv_file = 'dataset/leave_requests.csv'
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Employee Name', 'Employee ID', 'Department', 
                        'Reason', 'Start Date', 'End Date', 'Duration', 'Status', 'Flags'])

def get_employee_leave_history(employee_id, start_date):
    """
    Get the number of leaves taken by employee in the same month
    Returns 0 if employee is new or hasn't taken leaves this month
    """
    if not os.path.exists(csv_file):
        return 0
    
    try:
        start_month = datetime.strptime(start_date, '%Y-%m-%d').month
        start_year = datetime.strptime(start_date, '%Y-%m-%d').year
        
        leave_count = 0
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Employee ID'] == employee_id:
                    try:
                        leave_date = datetime.strptime(row['Start Date'], '%Y-%m-%d')
                        if leave_date.month == start_month and leave_date.year == start_year:
                            leave_count += 1
                    except ValueError:
                        continue
        return leave_count
    except Exception as e:
        print(f"Error reading leave history: {e}")
        return 0

def get_employee_info(employee_id):
    """
    Get employee information if exists in dataset
    Returns None if employee is new
    """
    if not os.path.exists(csv_file):
        return None
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Employee ID'] == employee_id:
                    return {
                        'name': row['Employee Name'],
                        'department': row['Department'],
                        'total_leaves': 1
                    }
    except Exception as e:
        print(f"Error reading employee info: {e}")
    return None

def validate_dates(start_date, end_date):
    """Validate that dates are in correct format and end >= start"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if end < start:
            return False, "End date cannot be before start date"
        return True, None
    except ValueError:
        return False, "Invalid date format"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_leave():
    # Get form data
    employee_name = request.form.get('employee_name', '').strip()
    employee_id = request.form.get('employee_id', '').strip()
    department = request.form.get('department', '').strip()
    reason = request.form.get('reason', '').strip()
    start_date = request.form.get('start_date', '').strip()
    end_date = request.form.get('end_date', '').strip()
    
    # Validate required fields
    if not all([employee_name, employee_id, department, reason, start_date, end_date]):
        return render_template('error.html', 
                             message="All fields are required. Please fill out the complete form.")
    
    # Validate dates
    valid, error_msg = validate_dates(start_date, end_date)
    if not valid:
        return render_template('error.html', message=error_msg)
    
    # Check if employee exists in system
    existing_employee = get_employee_info(employee_id)
    is_new_employee = existing_employee is None
    
    # Get employee's leave history for Rule 3
    previous_leaves = get_employee_leave_history(employee_id, start_date)
    
    # Analyze the leave request
    result = analyze_leave_request(
        reason=reason,
        start_date=start_date,
        end_date=end_date,
        department=department,
        previous_leaves_count=previous_leaves
    )
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                employee_name,
                employee_id,
                department,
                reason,
                start_date,
                end_date,
                result['duration'],
                result['status'],
                '; '.join(result['reasons'])
            ])
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return render_template('error.html', 
                             message="Error saving request. Please try again.")
    
    # Render result page with additional info
    return render_template('result.html', 
                         employee_name=employee_name,
                         employee_id=employee_id,
                         is_new_employee=is_new_employee,
                         previous_leaves_count=previous_leaves,
                         result=result)

@app.route('/stats')
def statistics():
    """Display system statistics"""
    if not os.path.exists(csv_file):
        return render_template('stats.html', stats=None)
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            
            total_requests = len(reader)
            approved = sum(1 for r in reader if r['Status'] == 'Approved')
            flagged = sum(1 for r in reader if r['Status'] == 'Flagged')
            
            # Get unique employees
            unique_employees = len(set(r['Employee ID'] for r in reader))
            
            # Department breakdown
            dept_stats = {}
            for row in reader:
                dept = row['Department']
                dept_stats[dept] = dept_stats.get(dept, 0) + 1
            
            stats = {
                'total_requests': total_requests,
                'approved': approved,
                'flagged': flagged,
                'approval_rate': round((approved / total_requests * 100), 1) if total_requests > 0 else 0,
                'unique_employees': unique_employees,
                'departments': dept_stats
            }
            
            return render_template('stats.html', stats=stats)
    except Exception as e:
        print(f"Error generating stats: {e}")
        return render_template('stats.html', stats=None)

@app.route('/api/check-employee/<employee_id>')
def check_employee(employee_id):
    """API endpoint to check if employee exists"""
    info = get_employee_info(employee_id)
    if info:
        return jsonify({'exists': True, 'info': info})
    return jsonify({'exists': False})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', message="Internal server error"), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 AI-HR Leave Request Analyzer")
    print("=" * 50)
    print(f"📁 Dataset location: {csv_file}")
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            line_count = sum(1 for _ in f) - 1  # Exclude header
            print(f"📊 Existing records: {line_count}")
    else:
        print("📊 No existing records (new system)")
    print("=" * 50)
    print("🌐 Starting server...")
    print("🔗 Open: http://localhost:5000")
    print("📈 Stats: http://localhost:5000/stats")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)