import re
def check_password_strength(password):
    score = 0
    feedback = []
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make it at least 8 characters long.")
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include at least one number.")
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Include at least one special character.")
    strength = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong", "Excellent"]
    return strength[score], feedback
pwd = input("Enter your password: ")
rating, fb = check_password_strength(pwd)
print("Strength:", rating)
print("Suggestions:")
for item in fb:
    print("-", item)