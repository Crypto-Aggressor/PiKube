import logging
import socket
import subprocess
import os
import time
from datetime import datetime
import yaml

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        return self.end_time - self.start_time


def init_logger(log_file_path):
    """
    Initialize and configure the logger.

    Args:
        log_file_path (str): The path to the log file.

    Returns:
        Logger: The configured logger.
    """
    # Initialize and configure the logger
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')
    return logging.getLogger()

class PiClusterManager:
    """
    Class for managing a Raspberry Pi cluster.

    Args:
        hostname (str): The hostname or IP address of the Gateway.
        username (str): The SSH username for connecting to the Gateway.
        private_key_path (str): The path to the private SSH key for authentication.
        logger (Logger): The logger to use for logging messages.
        timeout_minutes (int, optional): The timeout duration in minutes for various operations. Default is 5 minutes.
        package_list_path (str, optional): The path to a YAML file containing a list of packages to install. Default is None.
    """

    def __init__(self, hostname, username, private_key_path, logger, timeout_minutes=5, package_list_path=None):
        self.hostname = hostname
        self.username = username
        self.private_key_path = private_key_path
        self.logger = logger  # Use the provided logger for enhanced logging
        self.timeout = timeout_minutes * 60  # Convert minutes to seconds
        self.package_list_path = package_list_path
        self.package_list = []

    def log_step(self, message):
        """
        Log a step with a timestamp.

        Args:
            message (str): The message to log.
        """
        # Log each step with a timestamp
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info(f'{current_time} - {message}')
    
    def log(self, action, command=None, output=None, level='info', timestamp=False):
        """
        Standardized logging method.

        Args:
            action (str): The primary action/message being performed.
            command (str, optional): The command being executed.
            output (str, optional): The output or result of the command.
            level (str): The log level ('info', 'error', 'warning', etc.)
            timestamp (bool): Whether to include a timestamp in the log.
        """
        # Timestamp prefix if needed
        prefix = time.strftime('%Y-%m-%d %H:%M:%S') + ' - ' if timestamp else ''

        # Log the action
        if level.lower() == 'info':
            self.logger.info(prefix + action)
        elif level.lower() == 'error':
            self.logger.error(prefix + action)
        elif level.lower() == 'warning':
            self.logger.warning(prefix + action)

        # Log the command if provided
        if command:
            self.logger.info(prefix + f"Command executed: {command}")

        # Log the output if provided
        if output:
            self.logger.info(prefix + f"Output: {output}")

    # def establish_connection(self):
    #     """
    #     Attempt to establish an SSH connection to the Gateway.

    #     Returns:
    #         bool: True if the SSH connection is successful, False otherwise.
    #     """
    #     try:
    #         start_time = time.time()  # Record the start time of the connection attempt
    #         self.log_step("Step 1: Attempting SSH connection")

    #         # Use the ssh command with subprocess to establish an SSH connection
    #         ssh_command = f'ssh -i {self.private_key_path} {self.username}@{self.hostname} exit'
            
    #         # Capture the command output and error separately
    #         completed_process = subprocess.run(ssh_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
    #         # Check if the process returned a non-zero exit code
    #         if completed_process.returncode != 0:
    #             error_message = f"Step 2: SSH connection failed with exit code {completed_process.returncode}\n"
    #             error_message += f"Command error output:\n{completed_process.stderr}"
    #             self.log_step(error_message)
    #             return False  # Return False if failed
            
    #         end_time = time.time()  # Record the end time of the connection attempt
    #         duration = end_time - start_time  # Calculate the duration

    #         success_message = f"Step 2: SSH connection successful (Duration: {duration:.2f} seconds)"
    #         self.log_step(success_message)
    #         return True  # Return True if successful
    #     except Exception as e:
    #         # Handle other exceptions and log the error message
    #         error_message = f"Step 2: SSH connection failed: {str(e)}"
    #         self.log_step(error_message)
    #         return False  # Return False if failed

    def establish_connection(self):
        """
        Attempt to establish an SSH connection to the Gateway.

        Returns:
            bool: True if the SSH connection is successful, False otherwise.
        """
        overall_timer = Timer()
        overall_timer.start()  # Start the timer for the entire method
        
        try:
            self.log('info', "Step 1: Attempting SSH connection")

            # Use the ssh command with subprocess to establish an SSH connection
            ssh_command = f'ssh -i {self.private_key_path} {self.username}@{self.hostname} exit'
            
            # Starting a timer for subprocess command
            command_timer = Timer()
            command_timer.start()
            completed_process = subprocess.run(ssh_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            command_duration = command_timer.stop()

            # Log the executed command and its duration
            self.log('info', f"Command executed: {ssh_command}")
            self.log('info', f"Command execution time: {command_duration:.2f} seconds")
            
            # Check if the process returned a non-zero exit code
            if completed_process.returncode != 0:
                error_message = f"Step 2: SSH connection failed with exit code {completed_process.returncode}"
                self.log('error', error_message)
                self.log('error', f"Error output: {completed_process.stderr}")
                return False  # Return False if failed
            
            success_message = f"Step 2: SSH connection successful"
            self.log('info', success_message)
            
        except Exception as e:
            # Handle other exceptions and log the error message
            error_message = f"Step 2: SSH connection failed: {str(e)}"
            self.log('error', error_message)
            return False  # Return False if failed

        # If the method completes without returning above, then log the success duration
        self.log('info', f"Total duration of the connection attempt: {overall_timer.stop():.2f} seconds")
        return True



    # def check_gateway(self):
    #     """
    #     Check if the Gateway has internet connectivity.

    #     Returns:
    #         bool: True if the Gateway has internet access, False otherwise.
    #     """
    #     if self.connect_with_timeout():
    #         self.log_step("Step 5: Checking internet connectivity.")
    #         if self.is_connected_to_internet():
    #             self.log_step("Gateway has internet access.")
    #             return True
    #         else:
    #             self.log_step("Gateway is accessible but does not have internet access.")
    #             return False
    #     return False

    # def connect_with_timeout(self):
    #     """
    #     Attempt to establish an SSH connection with a timeout.

    #     Returns:
    #         bool: True if the SSH connection is successful within the timeout, False otherwise.
    #     """
    #     start_time = time.time()
    #     while time.time() < start_time + self.timeout:
    #         if self.establish_connection():
    #             return True
    #         time.sleep(10)
    #     self.log_step("Step 3: Timeout reached. Exiting.")
    #     return False

    # def is_connected_to_internet(self):
    #     """        
    #     Check if the Gateway is connected to the internet.

    #     Returns:
    #         bool: True if the Gateway has internet access, False otherwise.
    #     """
    #     try:
    #         host = socket.gethostbyname("www.google.com")
    #         ssh_command = f'ssh -i {self.private_key_path} {self.username}@{self.hostname} ping -c 1 {host}'

    #         # Log the ping command executed
    #         self.logger.info("Command executed: %s", ssh_command)

    #         subprocess.check_call(ssh_command, shell=True)
    #         return True
    #     except (socket.error, subprocess.CalledProcessError):
    #         return False

    def check_gateway(self):
        """
        Check if the Gateway has internet connectivity.

        Returns:
            bool: True if the Gateway has internet access, False otherwise.
        """
        timer = Timer()
        timer.start()
        if self.connect_with_timeout():
            self.log('info', "Step 5: Checking internet connectivity.")
            if self.is_connected_to_internet():
                self.log('info', "Gateway has internet access.")
                self.log('info', f"Total time taken to check internet connectivity: {timer.stop():.2f} seconds")
                return True
            else:
                self.log('info', "Gateway is accessible but does not have internet access.")
                self.log('info', f"Total time taken to check internet connectivity: {timer.stop():.2f} seconds")
                return False
        self.log('info', f"Total time taken to check internet connectivity: {timer.stop():.2f} seconds")
        return False

    def connect_with_timeout(self):
        """
        Attempt to establish an SSH connection with a timeout.

        Returns:
            bool: True if the SSH connection is successful within the timeout, False otherwise.
        """
        timer = Timer()
        timer.start()
        start_time = time.time()
        while time.time() < start_time + self.timeout:
            if self.establish_connection():
                self.log('info', f"Time taken to establish connection: {timer.stop():.2f} seconds")
                return True
            time.sleep(10)
        self.log('info', "Step 3: Timeout reached. Exiting.")
        self.log('info', f"Total time taken to attempt connection: {timer.stop():.2f} seconds")
        return False

    def is_connected_to_internet(self):
        """
        Check if the Gateway is connected to the internet.

        Returns:
            bool: True if the Gateway has internet access, False otherwise.
        """
        timer = Timer()
        timer.start()
        try:
            host = socket.gethostbyname("www.google.com")
            ssh_command = f'ssh -i {self.private_key_path} {self.username}@{self.hostname} ping -c 1 {host}'

            # Log the ping command executed
            self.log('info', f"Command executed: {ssh_command}")

            subprocess.check_call(ssh_command, shell=True)
            self.log('info', f"Time taken for ping: {timer.stop():.2f} seconds")
            return True
        except (socket.error, subprocess.CalledProcessError):
            self.log('error', "Ping failed.")
            self.log('info', f"Time taken for ping: {timer.stop():.2f} seconds")
            return False


    def update_and_upgrade_if_needed(self):
        """
        Update and upgrade packages on the Gateway if needed.

        Returns:
            bool: True if updates were applied, False otherwise.
        """
        gateway_running = self.establish_connection()  # Check if the gateway is running

        # Log Gateway and internet access status
        self.logger.info(f"Gateway is Up & Running: {gateway_running}")
        internet_access = self.is_connected_to_internet()
        self.logger.info(f"Internet Access: {internet_access}")

        if gateway_running and internet_access:
            # Gateway is up, running, and has internet access
            # Run the command for updating and upgrading packages
            update_upgrade_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "export DEBIAN_FRONTEND=noninteractive && sudo apt update && sudo apt full-upgrade -y"'
            update_upgrade_output = subprocess.check_output(update_upgrade_command, shell=True, universal_newlines=True)
            self.logger.info("Update and Upgrade Command executed:\n%s", update_upgrade_command)
            self.logger.info("Update and Upgrade Output:\n%s", update_upgrade_output)

            # Check if there are updates applied
            if "0 upgraded, 0 newly installed" in update_upgrade_output:
                print("No updates were applied. Gateway will not reboot.")
                self.logger.info("No updates were applied. Gateway will not reboot")
                return False
            else:
                return True
        else:
            print("Gateway is not running or cannot be reached or has no internet access")
            self.logger.info("Gateway is not running or cannot be reached or has no internet access")
            return False

    def reboot_if_updates_applied(self):
        """
        Reboot the Raspberry Pi gateway if updates were applied.
        """
        if self.update_and_upgrade_if_needed():
            # Reboot the Gateway only if updates were applied
            self.logger.info("Rebooting Gateway")
            reboot_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo shutdown -r now"'
            reboot_output = subprocess.run(reboot_command, shell=True)
            # Log the 'uptime' command and output
            self.logger.info("Command executed: %s", reboot_command)
            self.logger.info("Command output:\n%s", reboot_output)

            # Wait for the gateway to reboot (adjust the timeout as needed)
            time.sleep(60)  # Wait for 1 minute

            # Attempt to connect to the gateway every 20 seconds for 1 minute
            for _ in range(3):
                time.sleep(20)
                connected = self.is_gateway_pi_running()
                if connected:
                    # If connected, check logs and record them
                    self.check_and_record_logs()
                    break

    def check_and_record_logs(self):
        """
        Check the gateway logs and record them in a separate file.

        This method retrieves the system logs from the Gateway via SSH, logs
        the executed command, and saves the logs in a separate file.

        Raises:
            subprocess.CalledProcessError: If there is an error executing the SSH command.
        """
        try:
            # SSH command to check logs on the gateway
            log_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "cat /var/log/syslog"'

            # Run the command and capture the logs
            logs_output = subprocess.check_output(log_command, shell=True, universal_newlines=True)

            # Log the command and log output
            self.logger.info("Log Command executed: %s", log_command)
            self.logger.info("Log Output:\n%s", logs_output)

            # Record the logs in a separate file
            logs_file_name = f'gateway_logs_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
            with open(logs_file_name, 'w') as logs_file:
                logs_file.write(logs_output)

            self.logger.info(f"Gateway logs recorded in file: {logs_file_name}")
        except subprocess.CalledProcessError as e:
            self.logger.error("Error while checking logs: %s", str(e))
    
    def free_resources(self):
        """
        Free up system resources on the gateway.

        This method removes unused Snap packages, purges Snapd and related packages,
        and runs 'apt autoremove' to clean up unused packages.

        Raises:
            Exception: If an error occurs while freeing resources.
        """
        try:
            self.log_step("Removing unused Snap packages...")
            snap_remove_command = "sudo snap list | awk '{if(NR>1)print $1}' | xargs -n1 sudo snap remove"
            snap_remove_output = subprocess.run(snap_remove_command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.info("Command executed: %s", snap_remove_command)
            self.logger.info("Command output:\n%s", snap_remove_output.stdout)
            self.logger.error("Command error output:\n%s", snap_remove_output.stderr)
            
            self.log_step("Purging Snapd and related packages...")
            snapd_purge_command = "sudo apt purge snapd -y"
            snapd_purge_output = subprocess.run(snapd_purge_command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.info("Command executed: %s", snapd_purge_command)
            self.logger.info("Command output:\n%s", snapd_purge_output.stdout)
            self.logger.error("Command error output:\n%s", snapd_purge_output.stderr)

            self.log_step("Running 'apt autoremove' to clean up unused packages...")
            autoremove_command = "sudo apt autoremove -y"
            autoremove_output = subprocess.run(autoremove_command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.logger.info("Command executed: %s", autoremove_command)
            self.logger.info("Command output:\n%s", autoremove_output.stdout)
            self.logger.error("Command error output:\n%s", autoremove_output.stderr)
        except Exception as e:
            self.logger.error("Error while freeing resources: %s", str(e))

    


    def change_gpu_memory_split(self, new_value):
        """
        Change the GPU memory split configuration.

        This method modifies the GPU memory split value in the gateway's configuration.
        
        Args:
            new_value (int): The new GPU memory split value in megabytes (MB).

        Raises:
            subprocess.CalledProcessError: If there is an error executing the SSH command.
        """
        try:
            # SSH command to read the current configuration
            read_config_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "cat /boot/firmware/config.txt"'
            current_config = subprocess.check_output(read_config_command, shell=True, universal_newlines=True)

            # Check if the GPU Memory Split setting already exists in the configuration
            if f'gpu_mem={new_value}' in current_config:
                self.logger.info(f"GPU Memory Split is already set to {new_value} MB")
                self.logger.info("Current GPU Memory Configuration:\n%s", current_config)
            else:
                # Log the current configuration
                self.logger.info("Current GPU Memory Configuration:\n%s", current_config)

                # Check if there is an existing GPU Memory Split setting
                gpu_mem_setting = [line for line in current_config.split('\n') if line.startswith('gpu_mem=')]

                if gpu_mem_setting:
                    # Update the existing GPU Memory Split setting, properly escaping single quotes
                    updated_config = current_config.replace(gpu_mem_setting[0], f'gpu_mem={new_value}'.replace("'", r"\'"))
                else:
                    # Add the new GPU Memory Split setting if it doesn't exist
                    updated_config = current_config + f'\ngpu_mem={new_value}'

                # SSH command to update the GPU Memory Split value
                # update_config_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "echo {escaped_updated_config} | sudo tee /boot/firmware/config.txt"'
                update_config_command = f'ssh -i {self.private_key_path} {self.username}@{self.hostname} "sudo sed -i \'$ a # Set GPU Memory Allocation\\n# Adjust the amount of memory allocated to the GPU.\\n# For headless mode and non-graphical applications, a lower value is often sufficient.\\n# Value is in megabytes (MB). Default is 64.\\n# Recommended: {new_value} for headless scenarios, adjust as needed.\\ngpu_mem={new_value}\' /boot/firmware/config.txt"'

                subprocess.check_call(update_config_command, shell=True)

                self.logger.info(f"Changed GPU Memory Split to {new_value} MB")

                # Log the updated configuration
                self.logger.info("Updated GPU Memory Configuration:\n%s", updated_config)

        except subprocess.CalledProcessError as e:
            self.logger.error("Error while changing GPU Memory Split: %s", str(e))



    def read_package_list(self):
        """
        Read the list of packages to install from a YAML file.

        This method reads the package list from a specified YAML file and stores it
        in the `package_list` attribute of the class.

        Raises:
            Exception: If an error occurs while reading the package list.
        """
        try:
            with open(self.package_list_path, 'r') as package_file:
                package_data = yaml.safe_load(package_file)
                if "gateway-packages-to-install" in package_data:
                    self.package_list = package_data["gateway-packages-to-install"]
                else:
                    self.logger.warning("No 'gateway-packages-to-install' section found in the YAML file.")
                self.logger.info("Packages to install: %s", ', '.join([package['name'] for package in self.package_list]))
        except Exception as e:
            self.logger.error(f"Error reading package list: {str(e)}")

    def check_installed_packages(self):
        """
        Check for installed packages on the gateway.

        This method remotely checks for installed packages on the gateway using the
        'dpkg -l' command.

        Returns:
            list: A list of installed package names.
        """
        try:
            installed_packages = []
            check_installed_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "dpkg -l"'
            process = subprocess.Popen(check_installed_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_text, stderr_text = process.communicate()
            return_code = process.returncode

            if return_code == 0:
                # Parse the output to get a list of installed package names
                lines = stdout_text.decode('utf-8').split('\n')
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] == 'ii':
                        installed_packages.append(parts[1])
            else:
                self.logger.error(f"Failed to check installed packages on {self.hostname}")
                self.logger.error(f"Error:\n{stderr_text.decode('utf-8')}")

            return installed_packages
        except Exception as e:
            self.logger.error(f"Error checking installed packages: {str(e)}")
            return []

    def install_packages(self):
        """
        Install packages on the gateway.

        This method installs packages on the gateway based on the package list
        obtained from `read_package_list`.

        Raises:
            Exception: If an error occurs during package installation.
        """
        try:
            self.read_package_list()

            if not self.package_list:
                self.logger.warning("No packages to install. Check your YAML file.")
                return

            installed_packages = self.check_installed_packages()

            packages_to_install = []
            for package in self.package_list:
                package_name = package.get('name', '')
                description = package.get('description', '')

                if package_name:
                    if package_name not in installed_packages:
                        packages_to_install.append(package_name)
                        self.logger.info(f"Package {package_name} not installed. Description: {description}")
                    else:
                        self.logger.info(f"Package {package_name} is already installed. Description: {description}")

            if not packages_to_install:
                self.logger.info("All packages are already installed. Nothing to do.")
                return

            for package_name in packages_to_install:
                install_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo apt-get install -y {package_name}"'
                process = subprocess.Popen(install_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout_text, stderr_text = process.communicate()
                return_code = process.returncode

                if return_code == 0:
                    self.logger.info(f"Installed {package_name} on {self.hostname}")
                else:
                    self.logger.error(f"Failed to install {package_name} on {self.hostname}")
                    self.logger.error(f"Error:\n{stderr_text.decode('utf-8')}")

            self.logger.info("Package installation completed.")
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            
    
    def enable_ip_forwarding(self):
        """
        Enable IP forwarding on the gateway.

        This method modifies the '/etc/sysctl.conf' file to enable IP forwarding.

        Raises:
            subprocess.CalledProcessError: If there is an error executing the SSH command.
        """
        try:
            self.log_step("Enabling IP Forwarding")
            
            # Read and log /etc/sysctl.conf before change
            read_sysctl_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "cat /etc/sysctl.conf"'
            sysctl_before_change = subprocess.check_output(read_sysctl_command, shell=True, universal_newlines=True)
            self.logger.info("Contents of /etc/sysctl.conf before change:\n%s", sysctl_before_change)
            
            # Check if net.ipv4.ip_forward=1 is uncommented or uncomment it
            set_ip_forward_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo sed -i \'s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g\' /etc/sysctl.conf"'
            subprocess.check_call(set_ip_forward_command, shell=True)
            
            # Log all the activities including the ubuntu gateway logs
            # self.check_and_record_logs()
            
            # Print /etc/sysctl.conf after change
            sysctl_after_change = subprocess.check_output(read_sysctl_command, shell=True, universal_newlines=True)
            self.logger.info("Contents of /etc/sysctl.conf after change:\n%s", sysctl_after_change)
            
        except subprocess.CalledProcessError as e:
            self.logger.error("Error while enabling IP forwarding: %s", str(e))

    def configure_firewall(self):
        """
        Configure firewall rules using nftables.

        This method configures filtering and forwarding rules on the gateway
        using nftables.

        Raises:
            subprocess.CalledProcessError: If there is an error configuring nftables.
        """
        try:
            self.log_step("Configuring Filtering and Forwarding rules")
            
            # Check if nftables is installed, otherwise install it
            check_nftables_installed_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "dpkg -l | grep nftables"'
            nftables_installed = subprocess.call(check_nftables_installed_command, shell=True)
            
            if nftables_installed != 0:
                self.logger.info("nftables is not installed. Installing...")
                install_nftables_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo apt-get install nftables -y"'
                subprocess.check_call(install_nftables_command, shell=True)
                self.logger.info("nftables installed successfully.")
            else:
                self.logger.info("nftables is already installed.")
            
            # Check if /etc/nftables.d exists, otherwise create it
            check_nftables_dir_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "test -d /etc/nftables.d || (sudo mkdir -p /etc/nftables.d && echo Created /etc/nftables.d)"'
            dir_created_output = subprocess.check_output(check_nftables_dir_command, shell=True, universal_newlines=True)
            self.logger.info("Checking and creating /etc/nftables.d directory:\n%s", dir_created_output)
            
            # Copy the required files to the gateway
            self.copy_files_to_gateway()
            
            # Log all the activities including the ubuntu gateway logs
            # self.check_and_record_logs()
            
        except subprocess.CalledProcessError as e:
            self.logger.error("Error while configuring nftables: %s", str(e))

    def copy_files_to_gateway(self):
        """
        Copy required files to the gateway.

        This method copies necessary configuration files from a Windows laptop
        to the gateway using SSH.

        Raises:
            subprocess.CalledProcessError: If there is an error copying files.
        """
        try:
            self.log_step("Copying files from Windows laptop to gateway")
            
            # List of files to copy
            files_to_copy = [
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/nftables.conf", "/etc/nftables.conf"),
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/defines.nft", "/etc/nftables.d/defines.nft"),
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/sets.nft", "/etc/nftables.d/sets.nft"),
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/filter-input.nft", "/etc/nftables.d/filter-input.nft"),
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/filter-output.nft", "/etc/nftables.d/filter-output.nft"),
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/filter-forward.nft", "/etc/nftables.d/filter-forward.nft"),
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/nat-prerouting.nft", "/etc/nftables.d/nat-prerouting.nft"),
                ("/c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/firewall-conf/nat-postrouting.nft", "/etc/nftables.d/nat-postrouting.nft")
            ]
            
            for source, destination in files_to_copy:
                copy_command = f'cat {source} | ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "cat > ~/temp_file && sudo mv ~/temp_file {destination}"'
                subprocess.check_call(copy_command, shell=True)
                self.logger.info(f"File {source} copied to {destination}")
            
        except subprocess.CalledProcessError as e:
            self.logger.error("Error while copying files to gateway: %s", str(e))
            
    def validate_nftables_config(self):
        """
        Validate the nftables configuration.

        This method validates the nftables configuration file ('/etc/nftables.conf')
        using the 'nft' command.

        Raises:
            subprocess.CalledProcessError: If there is an error validating the config.
        """
        try:
            self.log_step("Validating nftables.conf file")
            
            # Validate the nftables.conf file
            validate_nftables_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo nft -c -f /etc/nftables.conf"'
            validate_output = subprocess.check_output(validate_nftables_command, shell=True, universal_newlines=True)
            self.logger.info("Validation output:\n%s", validate_output)
            
        except subprocess.CalledProcessError as e:
            self.logger.error("Error while validating nftables.conf: %s", str(e))
    
    def check_enable_and_start_nftables_service(self):
        """
        Check and enable/start the nftables service.

        This method checks if the nftables service is enabled and active on the gateway.
        If not, it enables and starts the service.

        Raises:
            subprocess.CalledProcessError: If there is an error enabling or starting the service.
        """
        try:
            self.log_step("Enabling and starting nftables service")

            # Check if the nftables service is already enabled and active
            check_service_status_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo systemctl is-enabled nftables && sudo systemctl is-active nftables"'
            check_full_service_status_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo systemctl status nftables"'
            # Specify encoding="utf-8" to handle non-ASCII characters
            service_status_output = subprocess.check_output(check_service_status_command, shell=True, encoding="utf-8")
            full_service_status_output = subprocess.check_output(check_full_service_status_command, shell=True, encoding="utf-8")

            # Log the service status
            self.logger.info("nftables service status:\n%s", service_status_output)
            self.logger.info("nftables service status:\n%s", full_service_status_output)

            if "enabled\nactive" not in service_status_output:
                # The service is not enabled and active, so enable and start it
                enable_service_command = f'ssh -i {self.private_key_path} -q {self.username}@{self.hostname} "sudo systemctl enable nftables && sudo systemctl start nftables"'
                # Specify encoding="utf-8" to handle non-ASCII characters
                enable_service_output = subprocess.check_output(enable_service_command, shell=True, encoding="utf-8")

                # Log the enable and start actions
                self.logger.info("nftables service enable and start output:\n%s", enable_service_output)
            else:
                self.logger.info("nftables service is already enabled and active, no action needed.")

        except subprocess.CalledProcessError as e:
            self.logger.error("Error while enabling and starting nftables service: %s", str(e))

    
    def setup_dns(self):
        try:
            # SSH into the gateway
            ssh_command = f"ssh -i {self.private_key_path} -q {self.username}@{self.hostname}"
            
            self.log_step("Setting up DNS configuration")

            # Check if dnsmasq is installed and install it if not
            installed_packages = self.check_installed_packages()
            if "dnsmasq" not in installed_packages:
                self.logger.info("dnsmasq is not installed. Installing...")
                install_dnsmasq_command = f"{ssh_command} 'sudo apt-get install dnsmasq -y'"
                subprocess.check_call(install_dnsmasq_command, shell=True)
                self.logger.info("dnsmasq installed successfully.")
            else:
                self.logger.info("dnsmasq is already installed.")

            # Stop systemd-resolved
            stop_resolved_command = f"{ssh_command} sudo systemctl stop systemd-resolved"
            subprocess.check_call(stop_resolved_command, shell=True)
            self.logger.info("Stopping systemd-resolved...")
            self.logger.info(f"Command executed: {stop_resolved_command}")
            self.logger.info("systemd-resolved stopped.")

            # Specify DNS Port in /etc/systemd/resolved.conf
            set_dns_port_command = f'{ssh_command} "sudo sed -i \'s/^#DNS=/DNS=127.0.0.1:5353/\' /etc/systemd/resolved.conf || echo \'DNS=127.0.0.1:5353\' | sudo tee -a /etc/systemd/resolved.conf"'
            subprocess.check_call(set_dns_port_command, shell=True)
            self.logger.info("Specifying DNS Port in /etc/systemd/resolved.conf...")
            self.logger.info(f"Command executed: {set_dns_port_command}")

            # Restart systemd-resolved
            restart_resolved_command = f"{ssh_command} sudo systemctl restart systemd-resolved"
            subprocess.check_call(restart_resolved_command, shell=True)
            self.logger.info("Restarting systemd-resolved...")
            self.logger.info(f"Command executed: {restart_resolved_command}")
            self.logger.info("systemd-resolved restarted.")

            # Copy dnsmasq.conf to the remote server
            copy_dnsmasq_conf_command = f'cat /c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/dns-conf/dnsmasq.conf | {ssh_command} "cat > ~/dnsmasq.conf && sudo mv ~/dnsmasq.conf /etc/dnsmasq.d/"'
            subprocess.check_call(copy_dnsmasq_conf_command, shell=True)
            self.logger.info("Copying dnsmasq.conf to remote server...")
            self.logger.info(f"Command executed: {copy_dnsmasq_conf_command}")
        
            # Start dnsmasq
            start_dnsmasq_command = f"{ssh_command} sudo systemctl start dnsmasq"
            subprocess.check_call(start_dnsmasq_command, shell=True)
            self.logger.info("Starting dnsmasq...")
            self.logger.info(f"Command executed: {start_dnsmasq_command}")
            self.logger.info("dnsmasq started.")

            # Enable dnsmasq
            enable_dnsmasq_command = f"{ssh_command} sudo systemctl enable dnsmasq"
            subprocess.check_call(enable_dnsmasq_command, shell=True)
            self.logger.info("Enabling dnsmasq...")
            self.logger.info(f"Command executed: {enable_dnsmasq_command}")
            self.logger.info("dnsmasq enabled.")

        except Exception as e:
            self.logger.error(str(e))
            
    # def configure_load_balancer(self):
    #     try:
    #         # SSH into the gateway
    #         ssh_command = f"ssh -i {self.private_key_path} -q {self.username}@{self.hostname}"
            
    #         self.log_step("Setting up Load Balancer configuration")

    #         # Check if HAProxy is installed and install it if not
    #         installed_packages = self.check_installed_packages()
    #         if "haproxy" not in installed_packages:
    #             self.logger.info("haproxy is not installed. Installing...")
    #             install_haproxy_command = f"{ssh_command} 'sudo apt-get install haproxy -y'"
    #             subprocess.check_call(install_haproxy_command, shell=True)
    #             self.logger.info("haproxy installed successfully.")
    #         else:
    #             self.logger.info("haproxy is already installed.")
 
    #        # Copy haproxy.cfg to the remote server
    #         copy_haproxy_conf_command = f'cat /c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/load-balancer-conf/haproxy.cfg | {ssh_command} "cat > ~/haproxy.cfg && sudo mv ~/haproxy.cfg /etc/haproxy/"'
    #         subprocess.check_call(copy_haproxy_conf_command, shell=True)
    #         self.logger.info("Copying haproxy.cfg to remote server...")
    #         self.logger.info(f"Command executed: {copy_haproxy_conf_command}")
                            
    #         # copy_config_command = (
    #         #     f"cat /c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/load-balancer-conf/haproxy.cfg "
    #         #     f"| {ssh_command} 'cat > ~/haproxy.cfg && sudo mv ~/haproxy.cfg /etc/haproxy/haproxy.cfg'"
    #         # )
    #         # subprocess.check_call(copy_config_command, shell=True)
            
    #         # Check if the HAProxy configuration file is valid
    #         check_config_command = f'{ssh_command} "sudo haproxy -c -f /etc/haproxy/haproxy.cfg"'
    #         subprocess.check_call(check_config_command, shell=True)

    #         # Start HAProxy
    #         start_haproxy_command = f'{ssh_command} "sudo systemctl start haproxy"'
    #         subprocess.check_call(start_haproxy_command, shell=True)

    #         # Check HAProxy status
    #         status_haproxy_command = f'{ssh_command} "sudo systemctl status haproxy"'
    #         subprocess.check_call(status_haproxy_command, shell=True)

    #         # Enable HAProxy to boot on system startup
    #         enable_haproxy_command = f'{ssh_command} "sudo systemctl enable haproxy"'
    #         subprocess.check_call(enable_haproxy_command, shell=True)

    #         # Execute the commands one by one and print their outputs
    #         subprocess.run(copy_haproxy_conf_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #         print("HAProxy configuration copied successfully.")
            
    #         subprocess.run(check_config_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #         print("HAProxy configuration is valid.")
            
    #         subprocess.run(start_haproxy_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #         print("HAProxy started successfully.")
            
    #         subprocess.run(status_haproxy_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
    #         subprocess.run(enable_haproxy_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #         print("HAProxy enabled to boot on system startup.")
        
    #     except subprocess.CalledProcessError as e:
    #         print("Error:", e)
    #         print("Error Output:", e.stderr)
    #     except Exception as e:
    #         print("An error occurred:", e)

    # def configure_load_balancer(self):
    #     try:
    #         # SSH into the gateway
    #         ssh_command = f"ssh -i {self.private_key_path} -q {self.username}@{self.hostname}"
            
    #         self.log_step("Setting up Load Balancer configuration")

    #         # Check if HAProxy is installed and install it if not
    #         installed_packages = self.check_installed_packages()
    #         if "haproxy" not in installed_packages:
    #             self.logger.info("haproxy is not installed. Installing...")
    #             install_haproxy_command = f"{ssh_command} 'sudo apt-get install haproxy -y'"
    #             subprocess.check_call(install_haproxy_command, shell=True, encoding='utf-8', errors='replace')
    #             self.logger.info("haproxy installed successfully.")
    #         else:
    #             self.logger.info("haproxy is already installed.")
    
    #         # Copy haproxy.cfg to the remote server
    #         copy_haproxy_conf_command = f'cat /c/Users/amine/bin/github-projects/PiKube-Kubernetes-Cluster/build/load-balancer-conf/haproxy.cfg | {ssh_command} "cat > ~/haproxy.cfg && sudo mv ~/haproxy.cfg /etc/haproxy/"'
    #         result = subprocess.run(copy_haproxy_conf_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
    #         self.logger.info("Copying haproxy.cfg to remote server...")
    #         self.logger.info(f"Command executed: {copy_haproxy_conf_command}")
    #         self.logger.info(f"Output: {result.stdout}")
                                
    #         # Check if the HAProxy configuration file is valid
    #         check_config_command = f'{ssh_command} "sudo haproxy -c -f /etc/haproxy/haproxy.cfg"'
    #         result = subprocess.run(check_config_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
    #         self.logger.info("HAProxy configuration is valid.")
    #         self.logger.info(f"Command executed: {check_config_command}")
    #         self.logger.info(f"Output: {result.stdout}")
            
    #         # Start HAProxy
    #         start_haproxy_command = f'{ssh_command} "sudo systemctl start haproxy"'
    #         result = subprocess.run(start_haproxy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
    #         self.logger.info("HAProxy started successfully.")
    #         self.logger.info(f"Command executed: {start_haproxy_command}")
    #         self.logger.info(f"Output: {result.stdout}")
            
    #         # Check HAProxy status
    #         status_haproxy_command = f'{ssh_command} "sudo systemctl status haproxy"'
    #         result = subprocess.run(status_haproxy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
    #         self.logger.info(f"Command executed: {status_haproxy_command}")
    #         self.logger.info(f"Output: {result.stdout}")
            
    #         # Enable HAProxy to boot on system startup
    #         enable_haproxy_command = f'{ssh_command} "sudo systemctl enable haproxy"'
    #         result = subprocess.run(enable_haproxy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
    #         self.logger.info("HAProxy enabled to boot on system startup.")
    #         self.logger.info(f"Command executed: {enable_haproxy_command}")
    #         self.logger.info(f"Output: {result.stdout}")
        
    #     except subprocess.CalledProcessError as e:
    #         self.logger.error(f"Error during command execution: {e}")
    #         self.logger.error(f"Command stdout: {e.stdout}")
    #         self.logger.error(f"Command stderr: {e.stderr}")
    #     except Exception as e:
    #         self.logger.error(f"An unexpected error occurred: {e}")

    def configure_load_balancer(self):
        try:
            # SSH into the gateway
            ssh_command = f"ssh -i {self.private_key_path} -q {self.username}@{self.hostname}"
            
            # Check if HAProxy is installed and install it if not
            check_haproxy_installed = f"{ssh_command} 'dpkg -l | grep haproxy'"
            result = subprocess.run(check_haproxy_installed, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')

            if "haproxy" not in result.stdout:
                self.log("haproxy is not installed. Installing...")
                install_haproxy_command = f"{ssh_command} 'sudo apt-get install haproxy -y'"
                result = subprocess.run(install_haproxy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
                self.log("Installed haproxy.", command=install_haproxy_command, output=result.stdout, timestamp=True)
            else:
                self.log("haproxy is already installed.")

            # Copy haproxy.cfg to the remote server
            copy_haproxy_conf_command = f'cat /path/to/haproxy.cfg | {ssh_command} "cat > ~/haproxy.cfg && sudo mv ~/haproxy.cfg /etc/haproxy/"'
            result = subprocess.run(copy_haproxy_conf_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
            self.log("Copying haproxy.cfg to remote server...", command=copy_haproxy_conf_command, output=result.stdout, timestamp=True)

            # Check if the HAProxy configuration file is valid
            check_config_command = f'{ssh_command} "sudo haproxy -c -f /etc/haproxy/haproxy.cfg"'
            result = subprocess.run(check_config_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
            self.log("HAProxy configuration is valid.", command=check_config_command, output=result.stdout, timestamp=True)

            # Start HAProxy
            start_haproxy_command = f'{ssh_command} "sudo systemctl start haproxy"'
            result = subprocess.run(start_haproxy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
            self.log("HAProxy started successfully.", command=start_haproxy_command, output=result.stdout, timestamp=True)
            
            # Check HAProxy status
            status_haproxy_command = f'{ssh_command} "sudo systemctl status haproxy"'
            result = subprocess.run(status_haproxy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
            self.log("HAProxy status checked.", command=status_haproxy_command, output=result.stdout, timestamp=True)

            # Enable HAProxy to boot on system startup
            enable_haproxy_command = f'{ssh_command} "sudo systemctl enable haproxy"'
            result = subprocess.run(enable_haproxy_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='replace')
            self.log("HAProxy enabled to boot on system startup.", command=enable_haproxy_command, output=result.stdout, timestamp=True)

        except subprocess.CalledProcessError as e:
            self.log(f"Error during command execution: {e}", command=e.cmd, output=e.stdout, level='error', timestamp=True)

        except Exception as e:
            self.log(f"An unexpected error occurred: {e}", level='error', timestamp=True)

