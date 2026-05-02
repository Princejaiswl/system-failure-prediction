import os

os.system("python scripts/generate_metrics.py")
os.system("python scripts/generate_logs.py")
os.system("python scripts/generate_events.py")
os.system("python scripts/merge_data.py")

print("Pipeline completed")