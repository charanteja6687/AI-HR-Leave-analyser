from datetime import datetime, timedelta

# Public holidays (customize based on your region)
PUBLIC_HOLIDAYS = [
    '2025-01-01',  # New Year's Day
    '2025-01-26',  # Republic Day (India)
    '2025-03-14',  # Holi
    '2025-04-18',  # Good Friday
    '2025-08-15',  # Independence Day
    '2025-10-02',  # Gandhi Jayanti
    '2025-10-24',  # Diwali
    '2025-12-25',  # Christmas
    
    # Add 2026 holidays for future requests
    '2026-01-01',  # New Year's Day
    '2026-01-26',  # Republic Day
    '2026-12-25',  # Christmas
]

def analyze_leave_request(reason, start_date, end_date, department, previous_leaves_count=0):
    """
    Analyzes a leave request based on multiple rules.
    
    Args:
        reason (str): Reason for leave request
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        department (str): Employee's department
        previous_leaves_count (int): Number of leaves already taken this month
    
    Returns:
        dict: {
            'status': 'Approved' or 'Flagged',
            'reasons': list of reasons if flagged or approval message,
            'duration': number of days,
            'rules_triggered': list of rule numbers triggered
        }
    """
    flags = []
    rules_triggered = []
    
    # Convert dates
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        duration = (end - start).days + 1
    except ValueError:
        return {
            'status': 'Flagged',
            'reasons': ['Invalid date format - please use YYYY-MM-DD'],
            'duration': 0,
            'rules_triggered': ['validation_error']
        }
    
    # Validate duration is positive
    if duration <= 0:
        return {
            'status': 'Flagged',
            'reasons': ['End date must be on or after start date'],
            'duration': 0,
            'rules_triggered': ['validation_error']
        }
    
    # Rule 1: Duration more than 7 days
    if duration > 7:
        flags.append(f'Leave duration ({duration} days) exceeds 7 days')
        rules_triggered.append(1)
    
    # Rule 2: Keywords like vacation, travel, holiday, trip
    vacation_keywords = ['vacation', 'travel', 'holiday', 'trip']
    reason_lower = reason.lower()
    found_keywords = [kw for kw in vacation_keywords if kw in reason_lower]
    if found_keywords:
        flags.append(f'Leave reason contains vacation-related keywords: {", ".join(found_keywords)}')
        rules_triggered.append(2)
    
    # Rule 3: Already taken 3 or more leaves in the same month
    if previous_leaves_count >= 3:
        flags.append(f'Employee has already taken {previous_leaves_count} leaves this month (limit: 3)')
        rules_triggered.append(3)
    
    # Rule 4a: Starts on Friday
    if start.weekday() == 4:  # Friday = 4
        flags.append('Leave starts on Friday (potential long weekend extension)')
        rules_triggered.append('4a')
    
    # Rule 4b: Ends on Monday
    if end.weekday() == 0:  # Monday = 0
        flags.append('Leave ends on Monday (potential long weekend extension)')
        rules_triggered.append('4b')
    
    # Rule 5: Contains "sick" but reason is too short (less than 10 characters)
    if 'sick' in reason_lower and len(reason) < 10:
        flags.append(f'Sick leave reason is too brief ({len(reason)} characters, minimum: 10)')
        rules_triggered.append(5)
    
    # Rule 6: IT Support department with leave > 2 days
    if department == 'IT Support' and duration > 2:
        flags.append(f'IT Support department leave exceeds 2 days (requested: {duration} days, limit: 2)')
        rules_triggered.append(6)
    
    # Rule 7: Leave is just before or after a public holiday
    holiday_flags = check_holiday_proximity(start, end, duration)
    if holiday_flags:
        flags.extend(holiday_flags)
        rules_triggered.append(7)
    
    # Determine status
    status = 'Flagged' if flags else 'Approved'
    
    # Prepare response
    if status == 'Approved':
        response_reasons = [
            'All validation rules passed successfully',
            'No policy violations detected',
            'Request meets all approval criteria'
        ]
    else:
        response_reasons = flags
    
    return {
        'status': status,
        'reasons': response_reasons,
        'duration': duration,
        'rules_triggered': rules_triggered,
        'start_day': start.strftime('%A'),
        'end_day': end.strftime('%A')
    }

def check_holiday_proximity(start, end, duration):
    """
    Check if leave is adjacent to or includes public holidays
    
    Args:
        start (datetime): Start date
        end (datetime): End date
        duration (int): Leave duration in days
    
    Returns:
        list: List of holiday-related flags
    """
    flags = []
    
    for holiday_str in PUBLIC_HOLIDAYS:
        try:
            holiday = datetime.strptime(holiday_str, '%Y-%m-%d')
            holiday_name = get_holiday_name(holiday_str)
            
            # Check if leave starts immediately after holiday
            if start == holiday + timedelta(days=1):
                flags.append(f'Leave starts immediately after {holiday_name} ({holiday.strftime("%Y-%m-%d")})')
            
            # Check if leave ends immediately before holiday
            if end == holiday - timedelta(days=1):
                flags.append(f'Leave ends immediately before {holiday_name} ({holiday.strftime("%Y-%m-%d")})')
            
            # Check if holiday falls during the leave period
            if start <= holiday <= end:
                flags.append(f'Leave period includes {holiday_name} ({holiday.strftime("%Y-%m-%d")})')
        except ValueError:
            continue
    
    return flags

def get_holiday_name(date_str):
    """Get holiday name based on date"""
    holiday_names = {
        '01-01': 'New Year\'s Day',
        '01-26': 'Republic Day',
        '03-14': 'Holi',
        '04-18': 'Good Friday',
        '08-15': 'Independence Day',
        '10-02': 'Gandhi Jayanti',
        '10-24': 'Diwali',
        '12-25': 'Christmas'
    }
    
    month_day = date_str[5:]  # Extract MM-DD
    return holiday_names.get(month_day, 'Public Holiday')

def get_all_rules_info():
    """
    Returns information about all rules for documentation/display
    """
    return {
        'rule_1': {
            'name': 'Long Duration',
            'description': 'Leave duration exceeds 7 days',
            'threshold': '7 days'
        },
        'rule_2': {
            'name': 'Vacation Keywords',
            'description': 'Reason contains vacation-related keywords',
            'keywords': ['vacation', 'travel', 'holiday', 'trip']
        },
        'rule_3': {
            'name': 'Frequent Leaves',
            'description': 'Employee has taken 3 or more leaves in the same month',
            'threshold': '3 leaves per month'
        },
        'rule_4a': {
            'name': 'Friday Start',
            'description': 'Leave starts on Friday (potential long weekend)',
            'day': 'Friday'
        },
        'rule_4b': {
            'name': 'Monday End',
            'description': 'Leave ends on Monday (potential long weekend)',
            'day': 'Monday'
        },
        'rule_5': {
            'name': 'Brief Sick Reason',
            'description': 'Sick leave with insufficient details',
            'threshold': '10 characters minimum'
        },
        'rule_6': {
            'name': 'IT Support Duration',
            'description': 'IT Support department leave exceeds limit',
            'threshold': '2 days for IT Support'
        },
        'rule_7': {
            'name': 'Holiday Proximity',
            'description': 'Leave is adjacent to or includes public holidays',
            'check': 'Before, after, or during holidays'
        }
    }