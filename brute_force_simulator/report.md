# Brute-force Login Simulator

## Project Objective
Simulate a brute-force attack to understand credential guessing attacks and develop effective countermeasures.

## Tools & Technologies
- Python 3
- Flask (for dummy login server)
- Requests library (for HTTP client)
- Dictionary file for passwords

## Attack Scenario
- Attacker targets known username: `admin`
- Tries each password from a dictionary file
- Detects success when status code is 200

## Defense Techniques (Implemented)
- Rate limiting: max 5 requests/min

## Screenshots
- Flask server output
- Attacker script terminal output

## Ethical Note
This project is a **safe simulation**, used solely for learning purposes in a controlled environment.

## Learnings
- How brute-force works
- How login systems can be abused
- Importance of defense mechanisms like rate limiting
