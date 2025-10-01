"""
Script to generate a large dataset of leave requests for testing
Run this script to populate dataset/leave_requests.csv with 250+ realistic records

Usage:
    python generate_large_dataset.py
"""

import csv
import random
import os
from datetime import datetime, timedelta
from leave_analyzer import analyze_leave_request

# Ensure dataset directory exists
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# Configuration
employees = [
    ("John Smith", "EMP-001"), ("Sarah Johnson", "EMP-002"), ("Michael Chen", "EMP-003"),
    ("Emily Davis", "EMP-004"), ("Robert Wilson", "EMP-005"), ("Lisa Anderson", "EMP-006"),
    ("David Martinez", "EMP-007"), ("Jennifer Taylor", "EMP-008"), ("Christopher Lee", "EMP-009"),
    ("Amanda White", "EMP-010"), ("James Brown", "EMP-011"), ("Maria Garcia", "EMP-012"),
    ("Daniel Rodriguez", "EMP-013"), ("Jessica Martinez", "EMP-014"), ("Matthew Anderson", "EMP-015"),
    ("Ashley Thomas", "EMP-016"), ("Joshua Jackson", "EMP-017"), ("Stephanie White", "EMP-018"),
    ("Andrew Harris", "EMP-019"), ("Michelle Martin", "EMP-020"), ("Ryan Thompson", "EMP-021"),
    ("Nicole Garcia", "EMP-022"), ("Kevin Rodriguez", "EMP-023"), ("Rachel Lewis", "EMP-024"),
    ("Brandon Lee", "EMP-025"), ("Lauren Walker", "EMP-026"), ("Justin Hall", "EMP-027"),
    ("Samantha Allen", "EMP-028"), ("Nicholas Young", "EMP-029"), ("Kimberly King", "EMP-030"),
    ("Tyler Wright", "EMP-031"), ("Brittany Scott", "EMP-032"), ("Jonathan Green", "EMP-033"),
    ("Megan Adams", "EMP-034"), ("Steven Baker", "EMP-035"), ("Amber Nelson", "EMP-036"),
    ("Jacob Carter", "EMP-037"), ("Danielle Mitchell", "EMP-038"), ("Eric Perez", "EMP-039"),
    ("Hannah Roberts", "EMP-040"), ("Adam Turner", "EMP-041"), ("Victoria Phillips", "EMP-042"),
    ("Nathan Campbell", "EMP-043"), ("Olivia Parker", "EMP-044"), ("Zachary Evans", "EMP-045"),
    ("Grace Edwards", "EMP-046"), ("Samuel Collins", "EMP-047"), ("Sophia Stewart", "EMP-048"),
    ("Benjamin Sanchez", "EMP-049"), ("Emma Morris", "EMP-050")
]

departments = [
    "IT Support", "Engineering", "Human Resources", "Finance", 
    "Marketing", "Sales", "Operations", "Customer Service"
]

# Reason templates for different scenarios
approved_reasons = [
    "Medical appointment scheduled with specialist doctor",
    "Dental procedure and recovery time needed",
    "Child's school event and parent-teacher meeting",
    "Home maintenance emergency repair work scheduled",
    "Personal legal matter requires immediate attention",
    "Family member needs assistance with medical care",
    "Vehicle maintenance and registration renewal",
    "Professional certification exam preparation required",
    "Attending important family gathering celebration",
    "Personal health checkup and wellness visit",
    "Moving to new residence within city limits",
    "Elder care responsibilities for family member",
    "Court appearance for personal legal matter",
    "Educational course enrollment and orientation session",
    "Personal financial planning appointment with advisor",
    "Attending professional development workshop",
    "House closing and mortgage signing appointment",
    "Marriage license appointment at courthouse",
    "Required jury duty service obligation",
    "Property inspection and home appraisal scheduled"
]

vacation_reasons = [
    "Planning vacation trip to beach resort",
    "Holiday travel to visit family abroad",
    "Vacation planned for mountain hiking trip",
    "International travel for leisure and sightseeing",
    "Beach holiday with family members scheduled",
    "Trip to national park for camping adventure",
    "Cruise vacation booked months ago departing soon",
    "European travel tour package with group",
    "Adventure travel and exploration trip overseas",
    "Honeymoon trip after wedding ceremony celebration",
    "Annual family vacation to theme parks",
    "Weekend holiday getaway planned for relaxation",
    "Traveling to attend music festival event",
    "Road trip across multiple states planned",
    "Vacation rental booked for beach house stay"
]

sick_short_reasons = [
    "Sick", "Ill", "Flu", "Cold", "Fever", "Unwell", "Not well", "Health"
]

sick_detailed_reasons = [
    "Severe flu symptoms requiring bed rest and recovery time",
    "Doctor recommended rest for viral infection treatment plan",
    "Medical condition requires immediate attention and bed rest",
    "Recovering from minor surgical procedure successfully",
    "Chronic condition flare-up needs management and rest period",
    "Prescribed medication causing drowsiness and fatigue issues",
    "Physical therapy sessions scheduled for injury recovery",
    "Mental health day for stress management and wellness",
    "Migraine episode requiring dark room and complete rest",
    "Stomach illness with doctor's recommendation to stay home"
]

# Generate random date within 2025
def generate_random_date():
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def generate_leave_record():
    """Generate a single leave record with realistic data"""
    name, emp_id = random.choice(employees)
    dept = random.choice(departments)
    
    # Randomly select scenario type (weighted distribution)
    scenario = random.choice([
        'approved_short',      # 40% - Should pass all rules
        'approved_short',
        'approved_short',
        'approved_short',
        'long_duration',       # 10% - Trigger rule 1
        'vacation_keyword',    # 15% - Trigger rule 2
        'vacation_keyword',
        'friday_start',        # 10% - Trigger rule 4a
        'monday_end',          # 10% - Trigger rule 4b
        'sick_short',          # 5% - Trigger rule 5
        'it_support_long',     # 5% - Trigger rule 6
        'holiday_adjacent'     # 5% - Trigger rule 7
    ])
    
    start = generate_random_date()
    
    # Generate based on scenario
    if scenario == 'approved_short':
        # 1-3 days, mid-week, no vacation keywords
        duration = random.choice([1, 2, 3])
        # Avoid Friday (4) and ensure it doesn't end on Monday
        while start.weekday() == 4:  # Avoid Friday
            start = generate_random_date()
        end = start + timedelta(days=duration - 1)
        # Make sure it doesn't end on Monday
        while end.weekday() == 0:
            start = generate_random_date()
            end = start + timedelta(days=duration - 1)
        reason = random.choice(approved_reasons)
        
    elif scenario == 'long_duration':
        # 8-14 days to trigger rule 1
        duration = random.randint(8, 14)
        end = start + timedelta(days=duration - 1)
        reason = random.choice(approved_reasons + vacation_reasons)
        
    elif scenario == 'vacation_keyword':
        # Include vacation keywords to trigger rule 2
        duration = random.choice([3, 4, 5, 6])
        end = start + timedelta(days=duration - 1)
        reason = random.choice(vacation_reasons)
        
    elif scenario == 'friday_start':
        # Start on Friday to trigger rule 4a
        while start.weekday() != 4:  # Make it Friday
            start = generate_random_date()
        duration = random.choice([1, 2, 3])
        end = start + timedelta(days=duration - 1)
        reason = random.choice(approved_reasons)
        
    elif scenario == 'monday_end':
        # End on Monday to trigger rule 4b
        duration = random.choice([2, 3, 4])
        end = start + timedelta(days=duration - 1)
        attempts = 0
        while end.weekday() != 0 and attempts < 50:  # Make end date Monday
            start = generate_random_date()
            end = start + timedelta(days=duration - 1)
            attempts += 1
        reason = random.choice(approved_reasons)
        
    elif scenario == 'sick_short':
        # Short sick reason to trigger rule 5
        duration = 1
        end = start
        reason = random.choice(sick_short_reasons)
        
    elif scenario == 'it_support_long':
        # IT Support with >2 days to trigger rule 6
        dept = "IT Support"
        duration = random.choice([3, 4, 5])
        end = start + timedelta(days=duration - 1)
        reason = random.choice(approved_reasons)
        
    elif scenario == 'holiday_adjacent':
        # Near public holidays to trigger rule 7
        holidays = [
            datetime(2025, 1, 1),   # New Year
            datetime(2025, 12, 24), # Before Christmas
            datetime(2025, 12, 26), # After Christmas
            datetime(2025, 8, 14),  # Before Independence Day
            datetime(2025, 10, 1),  # Before Gandhi Jayanti
        ]
        start = random.choice(holidays)
        duration = random.choice([1, 2])
        end = start + timedelta(days=duration - 1)
        reason = random.choice(approved_reasons)
    
    # Create timestamp (some time before the leave start date)
    timestamp = start - timedelta(days=random.randint(1, 30))
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'timestamp': timestamp_str,
        'name': name,
        'emp_id': emp_id,
        'dept': dept,
        'reason': reason,
        'start_date': start.strftime('%Y-%m-%d'),
        'end_date': end.strftime('%Y-%m-%d'),
        'duration': (end - start).days + 1
    }

# Main execution
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔄 GENERATING LARGE DATASET FOR LEAVE REQUESTS")
    print("="*60)
    
    # Generate records
    print("\n📝 Generating 250 leave request records...")
    records = []
    
    for i in range(250):
        records.append(generate_leave_record())
        if (i + 1) % 50 == 0:
            print(f"   ✓ Generated {i + 1} records...")
    
    print(f"\n✅ Successfully generated {len(records)} records!")
    
    # Sort by timestamp
    records.sort(key=lambda x: x['timestamp'])
    
    # Analyze each record using the same logic as the app
    print("\n🔍 Analyzing records with rule engine...")
    
    # Count leaves per employee per month for rule 3
    employee_monthly_leaves = {}
    
    analyzed_records = []
    for i, record in enumerate(records):
        # Track monthly leaves
        emp_id = record['emp_id']
        month_key = record['start_date'][:7]  # YYYY-MM
        key = f"{emp_id}_{month_key}"
        previous_count = employee_monthly_leaves.get(key, 0)
        employee_monthly_leaves[key] = previous_count + 1
        
        # Analyze using the actual analyzer
        result = analyze_leave_request(
            reason=record['reason'],
            start_date=record['start_date'],
            end_date=record['end_date'],
            department=record['dept'],
            previous_leaves_count=previous_count
        )
        
        analyzed_records.append({
            **record,
            'status': result['status'],
            'flags': '; '.join(result['reasons'])
        })
        
        if (i + 1) % 50 == 0:
            print(f"   ✓ Analyzed {i + 1} records...")
    
    # Write to CSV
    output_file = 'dataset/leave_requests.csv'
    print(f"\n💾 Writing to {output_file}...")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Employee Name', 'Employee ID', 'Department', 
                        'Reason', 'Start Date', 'End Date', 'Duration', 'Status', 'Flags'])
        
        for rec in analyzed_records:
            writer.writerow([
                rec['timestamp'],
                rec['name'],
                rec['emp_id'],
                rec['dept'],
                rec['reason'],
                rec['start_date'],
                rec['end_date'],
                rec['duration'],
                rec['status'],
                rec['flags']
            ])
    
    # Print statistics
    approved = sum(1 for r in analyzed_records if r['status'] == 'Approved')
    flagged = sum(1 for r in analyzed_records if r['status'] == 'Flagged')
    
    print("\n" + "="*60)
    print("✅ DATASET GENERATION COMPLETED!")
    print("="*60)
    print(f"\n📊 STATISTICS:")
    print(f"   Total Records:     {len(analyzed_records)}")
    print(f"   Approved:          {approved} ({approved/len(analyzed_records)*100:.1f}%)")
    print(f"   Flagged:           {flagged} ({flagged/len(analyzed_records)*100:.1f}%)")
    print(f"\n📁 File Location:     {output_file}")
    print(f"📏 File Size:         {os.path.getsize(output_file) / 1024:.1f} KB")
    
    # Rule breakdown
    rule_counts = {}
    for rec in analyzed_records:
        if rec['status'] == 'Flagged':
            flags = rec['flags'].split('; ')
            for flag in flags:
                if 'exceeds 7 days' in flag:
                    rule_counts['Rule 1 (Duration > 7 days)'] = rule_counts.get('Rule 1 (Duration > 7 days)', 0) + 1
                elif 'vacation-related keywords' in flag:
                    rule_counts['Rule 2 (Vacation keywords)'] = rule_counts.get('Rule 2 (Vacation keywords)', 0) + 1
                elif 'already taken' in flag:
                    rule_counts['Rule 3 (Frequent leaves)'] = rule_counts.get('Rule 3 (Frequent leaves)', 0) + 1
                elif 'Friday' in flag:
                    rule_counts['Rule 4a (Friday start)'] = rule_counts.get('Rule 4a (Friday start)', 0) + 1
                elif 'Monday' in flag:
                    rule_counts['Rule 4b (Monday end)'] = rule_counts.get('Rule 4b (Monday end)', 0) + 1
                elif 'too brief' in flag:
                    rule_counts['Rule 5 (Short sick)'] = rule_counts.get('Rule 5 (Short sick)', 0) + 1
                elif 'IT Support' in flag:
                    rule_counts['Rule 6 (IT Support)'] = rule_counts.get('Rule 6 (IT Support)', 0) + 1
                elif 'holiday' in flag.lower():
                    rule_counts['Rule 7 (Holiday proximity)'] = rule_counts.get('Rule 7 (Holiday proximity)', 0) + 1
    
    if rule_counts:
        print(f"\n🎯 RULE TRIGGERS:")
        for rule, count in sorted(rule_counts.items()):
            print(f"   {rule}: {count}")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS:")
    print("="*60)
    print("   1. Run the Flask app:  python app.py")
    print("   2. Open browser:       http://localhost:5000")
    print("   3. View statistics:    http://localhost:5000/stats")
    print("   4. Submit new requests to see them added to the dataset")
    print("="*60 + "\n")