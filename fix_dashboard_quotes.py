"""
Fix dashboard template - replace escaped quotes
"""

# Read the file
with open('templates/student/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all escaped quotes
content = content.replace("\\'", "'")

# Write back
with open('templates/student/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all escaped quotes in dashboard.html")
print(f"✅ File size: {len(content)} characters")
