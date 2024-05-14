import os
from py_tool_kit import py_tool_kit as ptk

hostname = os.getenv('GATEWAY_HOSTNAME')
username = os.getenv('GATEWAY_USERNAME')
private_key_path = os.getenv('GATEWAY_SECRET_FILE')

# hostname = "192.168.8.10"
# username = "pi"
# private_key_path = "~/.ssh/gateway-pi"
# abs_path = "/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/scripts/logs"
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
    # Step 1: Enable IP Forwarding
    cluster_manager.enable_ip_forwarding()

    # # Step 2: Configure Firewall
    cluster_manager.configure_firewall()
    
    # Step 3: Validate nftables Configuration
    cluster_manager.validate_nftables_config()

    # Step 4: Check nftables Service Status
    cluster_manager.check_enable_and_start_nftables_service()
except Exception as e:
    # Handle errors gracefully and log them
    print(f"Error: {str(e)}")
