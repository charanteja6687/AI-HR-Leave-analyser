# AI-HR Leave Request Analyzer
A Flask-based web application that automates the analysis of employee leave requests using rule-based decision making. The system evaluates leave requests against multiple criteria and provides instant feedback on whether the request is approved or flagged for manager review.
```bash
# Solution: Run on a different port
flask run --port 5001
```
**Issue: Module not found error**
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```
**Issue: CSV file not being created**
- Check write permissions in the project directory
- The `dataset/` folder will be created automatically on first run
**Issue: Templates not loading**
- Verify the `templates/` and `static/` folders are in the same directory as `app.py`
- Check folder names are exactly `templates` and `static` (lowercase)
## 🔐 Security Considerations
This is a demonstration application. For production use, consider:
- Adding user authentication and authorization
- Implementing CSRF protection
- Validating and sanitizing all user inputs
- Using a proper database (PostgreSQL, MySQL) instead of CSV
- Adding rate limiting to prevent abuse
- Implementing secure session management
- Using HTTPS for all communications
## 🚀 Future Enhancements
Potential features to add:
- **Machine Learning Integration**: Train a model to predict approval likelihood
- **Email Notifications**: Automatic emails to employees and managers
- **Manager Dashboard**: Interface for managers to review flagged requests
- **Calendar Integration**: Sync with Google Calendar or Outlook
- **Leave Balance Tracking**: Monitor remaining leave days per employee
- **Analytics Dashboard**: Visualize leave patterns and trends
- **Multi-language Support**: Internationalization for global teams
- **Mobile App**: Native iOS/Android applications
## 📝 API Documentation
### Endpoints
**GET /**
- Description: Renders the leave request form
- Returns: HTML form page
**POST /submit**
- Description: Processes leave request submission
- Parameters (form data):
  - `employee_name`: string (required)
  - `employee_id`: string (required)
  - `department`: string (required)
  - `reason`: string (required)
  - `start_date`: date in YYYY-MM-DD format (required)
  - `end_date`: date in YYYY-MM-DD format (required)
- Returns: HTML result page with analysis
## 📄 File Descriptions
### Core Application Files
- **app.py**: Main Flask application, handles routing and request processing
- **leave_analyzer.py**: Contains the rule-based logic for analyzing leave requests
- **requirements.txt**: Python package dependencies
### Templates
- **templates/index.html**: Leave request submission form with validation
- **templates/result.html**: Displays analysis results (Approved/Flagged)
### Static Assets
- **static/style.css**: Professional corporate styling with responsive design
### Data Storage
- **dataset/leave_requests.csv**: Auto-generated CSV file storing all submissions
## 🧪 Testing
### Manual Testing Checklist
- [ ] Submit a valid leave request (1-2 days, mid-week, generic reason)
- [ ] Test long duration (>7 days)
- [ ] Test vacation keywords (vacation, travel, holiday, trip)
- [ ] Test Friday start date
- [ ] Test Monday end date
- [ ] Test short sick leave reason (<10 chars)
- [ ] Test IT Support department with >2 days
- [ ] Test leave around public holidays
- [ ] Submit multiple requests from same employee in one month
- [ ] Test form validation (end date before start date)
- [ ] Test responsive design on mobile device
### Example Test Scenarios
```python
# Test 1: Multiple Flags
Employee: John Doe (EMP-001)
Department: IT Support
Start: 2025-10-01 (Friday)
End: 2025-10-12 (Monday, 12 days)
Reason: "Planning a vacation trip"
Expected: Flagged (4+ reasons)
# Test 2: Clean Approval
Employee: Jane Smith (EMP-002)
Department: Engineering
Start: 2025-10-15 (Wednesday)
End: 2025-10-16 (Thursday, 2 days)
Reason: "Medical appointment and recovery"
Expected: Approved
# Test 3: Holiday Proximity
Employee: Bob Johnson (EMP-003)
Department: Finance
Start: 2025-12-24 (Day before Christmas)
End: 2025-12-24 (1 day)
Reason: "Personal work"
Expected: Flagged (before public holiday)
```
## 🤝 Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
## 📞 Support
For issues, questions, or suggestions:
- Create an issue in the repository
- Check existing issues for solutions
- Review the troubleshooting section above
## 📜 License
This project is open source and available under the MIT License.
## 👏 Acknowledgments
- Built with Flask web framework
- Designed for HR departments and employee management systems
- Inspired by real-world leave approval workflows
## 📊 Project Statistics
- **Lines of Code**: ~800
- **Languages**: Python, HTML, CSS, JavaScript
- **Dependencies**: Flask, Werkzeug
- **Estimated Setup Time**: 5 minutes
- **Complexity**: Beginner to Intermediate
---
**Version**: 1.0.0  
**Last Updated**: September 2025  
**Status**: Production Ready (Demo)
## 🎯 Quick Start Commands
```bash
# Complete setup in 4 commands
git clone <repository-url>
cd AI-HR-Leave-Request-Analyzer
pip install -r requirements.txt
python app.py
```
Then open `http://localhost:5000` in your browser!
---
**Made with ❤️ for efficient HR management**🌟 Features
- **Automated Leave Analysis**: Real-time evaluation of leave requests based on 8 comprehensive rules
- **Professional HR Interface**: Clean, modern UI designed for corporate environments
- **Request History Tracking**: All submissions are stored in CSV format for record-keeping
- **Multiple Department Support**: Handles different departments with specific rules (e.g., IT Support)
- **Public Holiday Detection**: Identifies leaves adjacent to public holidays
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
## 📋 Analysis Rules
The system flags leave requests based on the following criteria:
1. **Duration Limit**: Leave duration exceeds 7 days
2. **Vacation Keywords**: Reason contains "vacation", "travel", "holiday", or "trip"
3. **Frequency Check**: Employee has taken 3+ leaves in the same month
4. **Weekend Extension**: Leave starts on Friday or ends on Monday
5. **Sick Leave Validation**: "Sick" reason with less than 10 characters
6. **Department-Specific**: IT Support department with leave > 2 days
7. **Holiday Proximity**: Leave is immediately before/after a public holiday
8. **Holiday Inclusion**: Leave period includes a public holiday
## 🚀 Installation & Setup
### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
### Step-by-Step Installation
1. **Clone or Download the Project**
   ```bash
   cd AI-HR-Leave-Request-Analyzer
   ```
2. **Create a Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Verify Project Structure**
   ```
   AI-HR-Leave-Request-Analyzer/
   ├── app.py
   ├── leave_analyzer.py
   ├── requirements.txt
   ├── README.md
   ├── templates/
   │   ├── index.html
   │   └── result.html
   ├── static/
   │   └── style.css
   └── dataset/
       └── leave_requests.csv (auto-created)
   ```
5. **Run the Application**
   ```bash
   python app.py
   ```
6. **Access the Application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`
   - You should see the Leave Request submission form
## 💻 Usage
### Submitting a Leave Request
1. Fill in the employee information:
   - Full Name
   - Employee ID
   - Department
2. Provide leave details:
   - Start Date
   - End Date
   - Detailed reason (min 10 characters recommended)
3. Click "Submit Request"
4. View the analysis result:
   - **Approved**: Leave is automatically approved
   - **Flagged**: Leave requires manager review with specific reasons listed
### Sample Test Cases
**Test Case 1: Approved Leave**
- Employee ID: EMP-001
- Department: Engineering
- Start Date: Any Wednesday
- End Date: Same Wednesday (1 day)
- Reason: "Personal appointment scheduled"
**Test Case 2: Flagged - Long Duration**
- Employee ID: EMP-002
- Department: Marketing
- Start Date: Any Monday
- End Date: 10 days later
- Reason: "Family vacation trip abroad"
(Flags: Duration > 7 days, vacation keywords, ends on Friday)
**Test Case 3: Flagged - IT Support**
- Employee ID: EMP-003
- Department: IT Support
- Start Date: Any Monday
- End Date: Friday (5 days)
- Reason: "Medical treatment required"
(Flags: IT Support > 2 days, ends on Friday)
## 📊 Data Storage
All leave requests are automatically saved to `dataset/leave_requests.csv` with the following fields:
- Timestamp
- Employee Name
- Employee ID
- Department
- Reason
- Start Date
- End Date
- Duration
- Status (Approved/Flagged)
- Flags (reasons if flagged)
## 🔧 Customization
### Modifying Public Holidays
Edit the `PUBLIC_HOLIDAYS` list in `leave_analyzer.py`:
```python
PUBLIC_HOLIDAYS = [
    '2025-01-01',  # New Year's Day
    '2025-12-25',  # Christmas
    # Add more holidays as needed
]
```
### Adding New Departments
Update the dropdown in `templates/index.html`:
```html
<option value="Your Department">Your Department</option>
```
### Adjusting Rules
Modify the logic in `leave_analyzer.py` to change thresholds or add new rules.
##