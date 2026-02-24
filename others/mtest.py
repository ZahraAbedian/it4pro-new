import re

def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    
    if re.match(pattern, password):
        return True
    else:
        return False

# Test the function
passwords = ['Password@1', 'password', 'PASSWORD', 'Pass1', 'PassWord', 'validPass1', 'Valid1', 'TooShort1']

for pwd in passwords:
    print(f'Password: {pwd}, Valid: {validate_password(pwd)}')