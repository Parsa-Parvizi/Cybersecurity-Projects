import pandas as pd
import matplotlib.pyplot as plt

# Assume the data is stored in the file keylog.csv.
df = pd.read_csv('keylog.csv')

# Data cleaning (example)
df['time'] = pd.to_datetime(df['time'])  # Convert time column to datetime type
df.dropna(inplace=True)  # Delete rows with missing values

# Analysis
key_counts = df['key'].value_counts()  # Counting the number of times each key is pressed
print(key_counts)

# Visualization - Number of times each key is pressed
plt.figure(figsize=(10, 6))
key_counts.plot(kind='bar')
plt.title('Number of times each key is pressed')
plt.xlabel('Key')
plt.ylabel('Number')
plt.show()

# Additional Analysis (Examples)

# Analysis by Time
df['hour'] = df['time'].dt.hour
hourly_keystrokes = df.groupby('hour')['key'].count()

# Visualization - Keystrokes per Hour
plt.figure(figsize=(10, 6))
hourly_keystrokes.plot(kind='bar')
plt.title('Number of Keystrokes per Hour')
plt.xlabel('Hour')
plt.ylabel('Number of Keystrokes')
plt.show()

# Analysis by Window
window_counts = df['window_title'].value_counts()

# Visualization - Keystrokes per Window
plt.figure(figsize=(10, 6))
window_counts.plot(kind='bar')
plt.title('Number of Keystrokes per Window')
plt.xlabel('Window Title')
plt.ylabel('Number of Keystrokes')
plt.xticks(rotation=45, ha='right')  # Rotate long window titles for better readability
plt.show()

# You can add more analysis sections here based on your needs
# For example, analyze hold times, key combinations, etc.