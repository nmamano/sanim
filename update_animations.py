#!/usr/bin/env python3
import re

# Read the sanim.py file
with open('sanim.py', 'r') as file:
    content = file.read()

# Replace Write with CustomWrite
updated_content = content.replace('Write(self.text)', 'CustomWrite(self.text)')
updated_content = updated_content.replace('Write(self.term)', 'CustomWrite(self.term)')
updated_content = updated_content.replace('Write(self.defi)', 'CustomWrite(self.defi)')

# Write the updated content back to sanim.py
with open('sanim.py', 'w') as file:
    file.write(updated_content)

print("Updated sanim.py with CustomWrite animations")