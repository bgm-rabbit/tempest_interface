# grapher.py
import matplotlib.pyplot as plt

def plot_temperature(df, save_path='temp_24h.png'):
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp_local'], df['temp_f'], color='orange', linewidth=2, marker='o', markersize=3, alpha=0.8)
    plt.title('Temperature Over the Last 24 Hours (°F)')
    plt.xlabel('Time (America/Chicago)')
    plt.ylabel('Temperature (°F)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Graph saved as {save_path}")

# Stretch: Add more plots later, e.g., def plot_humidity(df): ...