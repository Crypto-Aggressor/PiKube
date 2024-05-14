import os
from py_tool_kit import py_tool_kit as ptk

hostname = os.getenv('GATEWAY_HOSTNAME')
username = os.getenv('GATEWAY_USERNAME')
private_key_path = os.getenv('GATEWAY_SECRET_FILE')

# hostname = "192.168.8.10"
# username = "pi"
# private_key_path = "~/.ssh/gateway-pi"

## Get the full path of the currently running script
current_script_path = os.path.abspath(__file__)

# Extract just the filename without the extension
current_script_filename_without_extension = os.path.splitext(os.path.basename(current_script_path))[0]

log_file_path = f'logs/{current_script_filename_without_extension}.log'

# Initialize the logger
logger = ptk.init_logger(log_file_path)

# Create an instance of PiClusterManager
cluster_manager = ptk.PiClusterManager(
    hostname,
    username,
    private_key_path,
    logger=logger,
)

try:
    # Call the setup_dns method to configure DNS
    cluster_manager.setup_dns()
except Exception as e:
    # Handle any exceptions or errors that may occur during DNS setup
    print(f"DNS setup failed: {str(e)}")
