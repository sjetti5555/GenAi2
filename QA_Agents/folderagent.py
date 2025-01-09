import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderMonitorAgent(FileSystemEventHandler):
    """
    Agent to monitor a folder and process files when they are added.
    """
    def __init__(self, folder_to_monitor, process_file_callback):
        self.folder_to_monitor = folder_to_monitor
        self.process_file_callback = process_file_callback
        self.last_file_added_time = time.time()

    def on_created(self, event):
        """
        Triggered when a new file is created in the monitored folder.
        """
        if not event.is_directory:  # Ignore folder creation events
            file_path = event.src_path
            print(f"New file detected: {file_path}")
            self.last_file_added_time = time.time()  # Update the last file added time
            self.process_file_callback(file_path)

def start_folder_monitoring(folder_to_monitor, process_file_callback):
    """
    Start monitoring the specified folder using FolderMonitorAgent.
    """
    if not os.path.exists(folder_to_monitor):
        os.makedirs(folder_to_monitor)
        print(f"Created folder: {folder_to_monitor}")

    # Initialize the event handler and observer
    event_handler = FolderMonitorAgent(folder_to_monitor, process_file_callback)
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=True)

    # Start the observer
    print(f"Monitoring folder: {folder_to_monitor}")
    observer.start()
    try:
        while True:
            time.sleep(10)  # Check every 10 seconds
            time_since_last_file = time.time() - event_handler.last_file_added_time
            if time_since_last_file > 30:  # No files added in the last 30 seconds
                print("No files added in the last 30 seconds. Monitoring is active...")
                event_handler.last_file_added_time = time.time()  # Reset the timer to avoid repeated prints
    except KeyboardInterrupt:
        print("Stopping folder monitoring...")
        observer.stop()
    observer.join()

# Example Callback Function
def process_file(file_path):
    """
    Example callback function to process a file when added.
    """
    print(f"Processing file: {file_path}")
    # Add your file processing logic here

# Main Script
if __name__ == "__main__":
    folder_to_monitor = "C:/Users/srira/Desktop/GenAi2/QARAGAgents/qa_files"
    start_folder_monitoring(folder_to_monitor, process_file)
