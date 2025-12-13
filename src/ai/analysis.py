import pandas as pd
import matplotlib.pyplot as plt
import os
import glob


def load_latest_session():
    # Find latest session in data/sessions
    sessions = glob.glob("data/sessions/*")
    if not sessions:
        print("No sessions found.")
        return None
    latest_session = max(sessions, key=os.path.getctime)
    log_file = os.path.join(latest_session, "events.csv")
    if not os.path.exists(log_file):
        return None
    return pd.read_csv(log_file)


def plot_performance(df):
    if df is None or df.empty:
        print("No data to plot.")
        return

    # Filter for HIT events
    hits = df[df["event_type"] == "HIT"]
    misses = df[df["event_type"] == "MISS"]

    plt.figure(figsize=(10, 6))

    # Plot spatial distribution
    plt.subplot(1, 2, 1)
    if not hits.empty:
        plt.scatter(hits["x"], hits["y"], c="green", label="Hits", alpha=0.6)
    if not misses.empty:
        plt.scatter(misses["x"], misses["y"], c="red", label="Misses", alpha=0.6)
    plt.xlim(0, 1280)
    plt.ylim(720, 0)  # Invert Y for screen coordinates
    plt.title("Hit/Miss Distribution")
    plt.legend()
    plt.grid(True)

    # Plot reaction times if available
    # We need to extract reaction time from 'details' column which is "time=123ms"
    # This is a bit hacky, but works for the current format
    plt.subplot(1, 2, 2)
    reaction_times = []
    if not hits.empty:
        for detail in hits["details"]:
            try:
                # detail format: "time=123ms"
                t_str = detail.split("=")[1].replace("ms", "")
                reaction_times.append(float(t_str))
            except:
                pass

    if reaction_times:
        plt.hist(reaction_times, bins=10, color="blue", alpha=0.7)
        plt.title("Reaction Time Distribution (ms)")
        plt.xlabel("Time (ms)")
        plt.ylabel("Count")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    df = load_latest_session()
    plot_performance(df)
