import os
from py_tool_kit import py_tool_kit as ptk

hostname = os.getenv('GATEWAY_HOSTNAME')
username = os.getenv('GATEWAY_USERNAME')
private_key_path = os.getenv('GATEWAY_SECRET_FILE')

# Get the full path of the currently running script
current_script_path = os.path.abspath(__file__)

# Extract just the filename without the extension
current_script_filename_without_extension = os.path.splitext(os.path.basename(current_script_path))[0]

log_file_path = f'logs/{current_script_filename_without_extension}.log'

# Initialize the logger
logger = ptk.init_logger(log_file_path)

package_list_path = os.getenv('GATEWAY_PACKAGE_LIST')

# Create an instance of PiClusterManager
cluster_manager = ptk.PiClusterManager(
    hostname,
    username,
    private_key_path,
    logger=logger,
    package_list_path=package_list_path
)

# Install packages on the remote gateway
cluster_manager.install_packages()
