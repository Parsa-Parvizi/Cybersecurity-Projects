from scapy.all import *
import pandas as pd
import matplotlib.pyplot as plt
# import time
from scapy.layers.inet import IP
import smtplib
from email.mime.text import MIMEText

# Initial settings
interface = "eth0"  # Replace with the name of your network interface.
bpf_filter = "ip"  # Filter to select IP packets
capture_time = 60  # Packet recording time in seconds


# A function to process each packet
def packet_handler(packetArg):
    # Extracting information from the package
    ip_layer = packetArg[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    protocol = ip_layer.proto
    timestamp = packetArg.time
    packet_size = len(packetArg)

    # Storing data in a DataFrame
    data = {'src_ip': src_ip, 'dst_ip': dst_ip, 'protocol': protocol, 'timestamp': timestamp}
    global df
    df = df.append(data, ignore_index=True)


def send_alert(message):
    # Alert sending function
    msg = MIMEText(message)
    msg['Subject'] = 'Alert: Suspicious Activity Detected'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)


def detect_port_scan(df, threshold_port_count=10, threshold_unique_ips=5, window_size=60):
    """
    Port scan detection function

    Arguments:
    df: DataFrame containing traffic data
    threshold_port_count: Threshold number of requests to a port per time window
    threshold_unique_ips: Threshold number of unique IP addresses connecting to a port
    window_size: Time window size in seconds

    Output:
    A list of indices of rows that are likely to contain port scans
    """

    # Create a new column to count the number of requests to each port in each time window
    df['port_count'] = df.groupby(['destination_port', pd.Grouper(key='timestamp', freq=f'{window_size}S')]).size()

    # Create a new column to count the number of unique IP addresses for each port in each time window
    df['unique_ips'] = df.groupby(['destination_port', pd.Grouper(key='timestamp', freq=f'{window_size}S')])[
        'source_ip'].nunique()

    # Identify rows with a number of requests or unique IP addresses exceeding a threshold
    suspicious_indices = df[(df['port_count'] > threshold_port_count) | (df['unique_ips'] > threshold_unique_ips)].index

    return suspicious_indices


def detect_ddos(df, threshold_packets=1000, threshold_bytes=1000000, window_size=60):
    """
    DDoS Attack Detection Function

    Arguments:
    df: DataFrame containing traffic data
    threshold_packets: Threshold number of packets per time window
    threshold_bytes: Threshold traffic volume per time window
    window_size: Time window size in seconds

    Output:
    A list of indices of rows that are likely to contain a DDoS attack
    """

    # Create a new column to count the number of packets in each time window
    df['count'] = df.groupby(pd.Grouper(key='timestamp', freq=f'{window_size}S')).size()

    # Create a new column to calculate traffic volume in each time window
    df['bytes'] = df.groupby(pd.Grouper(key='timestamp', freq=f'{window_size}S')).size() * df['packet_size'].mean()

    # Identify rows whose traffic volume packets exceed the threshold
    suspicious_indices = df[(df['count'] > threshold_packets) | (df['bytes'] > threshold_bytes)].index

    return suspicious_indices


def analyze_http_traffic(df):
    """
    HTTP Traffic Analysis Function

    Arguments:
    df: DataFrame containing traffic data

    Output:
    New DataFrame containing information extracted from HTTP traffic
    """

    # HTTP packet filtering
    http_df = df[df['protocol'] == 'tcp']  # Suppose the HTTP protocol is transmitted over TCP.
    http_df = http_df[http_df['http']]  # Checking for the presence of the HTTP layer in the packet

    # Extracting information from the HTTP layer
    http_df['method'] = http_df.http.method
    http_df['url'] = http_df.http.Host + http_df.http.Path
    http_df['status_code'] = http_df.http.response.status_code
    http_df['content_type'] = http_df.http.response.Content_Type

    # Further analysis (example)
    # Number of GET requests
    get_requests = http_df[http_df['method'] == 'GET'].shape[0]
    print("Number of GET requests :", get_requests)

    # Most used URLs
    top_urls = http_df['url'].value_counts().head(10)
    print("Most commonly used URLs:")
    print(top_urls)

    # More analysis based on need

    return http_df


# Create an empty DataFrame to store data
df = pd.DataFrame(columns=['src_ip', 'dst_ip', 'protocol', 'timestamp'])

print("Starting to register packages...")
sniff(prn=packet_handler, filter=bpf_filter, iface=interface, timeout=capture_time)

# Port Scan Detection
port_scan_indices = detect_port_scan(df)
if not port_scan_indices.empty:
    send_alert("Port scan detected!")

# DDoS Attack Detection
ddos_indices = detect_ddos(df)
if not ddos_indices.empty:
    send_alert("DDoS attack detected!")

# HTTP traffic analysis
http_df = analyze_http_traffic(df)

# Data analysis
print("Data analysis...")
print(df.describe())

# Calculating basic statistics
print("basic statistics:")
print(df.describe())

# Identifying high-traffic IP addresses
top_ips = df['src_ip'].value_counts().head(10)
print("high-traffic IP addresses:")
print(top_ips)

# Drawing a protocol distribution diagram
plt.figure(figsize=(10, 5))
df['protocol'].value_counts().plot(kind='bar')
plt.title('Distribution of protocols')
plt.xlabel('protocols')
plt.ylabel('Number')
plt.show()

# Save data to CSV file
df.to_csv('traffic_data.csv', index=False)

# Traffic analysis based on time
time_series = df.set_index('timestamp').resample('1T').count()  # Analysis by the minute
plt.figure(figsize=(10, 5))
time_series['src_ip'].plot()
plt.title('Traffic by time')
plt.xlabel('Time')
plt.ylabel('Number of packages')
plt.show()


# Add the ability to load data from a CSV file
def load_data(file_path):
    return pd.read_csv(file_path)


# Add the ability to identify suspicious packages
def detect_suspicious_packets(df, suspicious_threshold=100):
    suspicious_packets = df[df['packet_size'] > suspicious_threshold]
    return suspicious_packets.index


suspicious_indices = detect_suspicious_packets(df)
if not suspicious_indices.empty:
    send_alert("Suspicious packets detected!")

# Save suspicious data to CSV file
if not suspicious_indices.empty:
    df.loc[suspicious_indices].to_csv('suspicious_packets.csv', index=False)

# Displaying suspicious data
print("suspicious data:")
print(df.loc[suspicious_indices])


# Adding traffic analysis capability based on protocol
def analyze_protocol_traffic(df):
    protocol_analysis = df.groupby('protocol').size()
    return protocol_analysis


protocol_traffic = analyze_protocol_traffic(df)
print("Traffic analysis based on protocol:")
print(protocol_traffic)

# Traffic analysis graph based on protocol
plt.figure(figsize=(10, 5))
protocol_traffic.plot(kind='pie', autopct='%1.1f%%')
plt.title('Traffic analysis based on protocol')
plt.ylabel('')
plt.show()
