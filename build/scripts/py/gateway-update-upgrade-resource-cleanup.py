import os
from py_tool_kit import py_tool_kit as ptk

hostname = os.getenv('GATEWAY_HOSTNAME')
username = os.getenv('GATEWAY_USERNAME')
private_key_path = os.getenv('GATEWAY_SECRET_FILE')

# Get the full path of the currently running script
current_script_path = os.path.abspath(__file__)

# Extract just the filename without the extension
current_script_filename_without_extension = os.path.splitext(os.path.basename(current_script_path))[0]

log_file_path = f'logs/{current_script_filename_without_extension}.log'  # Specify your custom log file path

# Initialize the logger
logger = ptk.init_logger(log_file_path)

# Create an instance of PiClusterManager
cluster_manager = ptk.PiClusterManager(
    hostname,
    username,
    private_key_path,
    logger=logger,
    timeout_minutes=3
)

# Update and upgrade packages on the gateway
if cluster_manager.update_and_upgrade_if_needed():
    print("Updates were applied. Gateway may reboot.")

# Reboot the gateway if updates were applied, and check and record logs during reboot
cluster_manager.reboot_if_updates_applied()

# Free up resources after updates and upgrades
cluster_manager.free_resources()
