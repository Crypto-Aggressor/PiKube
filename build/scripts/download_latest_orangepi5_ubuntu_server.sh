#!/bin/bash

# Set strict mode for error handling and unset variable checking
set -euo pipefail

# Check if /mnt/usb_sda1 is mounted and unmount if yes
if mount | grep -qs '/mnt/usb_sda1'; then
    echo "/mnt/usb_sda1 is already mounted. Unmounting..."
    sudo umount /mnt/usb_sda1
fi

echo "Available USB storage devices:"
lsblk -o NAME,MODEL,SIZE,VENDOR,RM | grep '1$' # Filter removable devices, assuming '1' in the RM column indicates removable

echo ""
echo "Please identify the correct USB device for the image burning process from the list above."
read -p "Enter the device name (e.g., sda): " usb_device

# Create a temporary directory for downloading and extracting the image
TEMP_DIR=$(mktemp -d -t orangepi-ubuntu-XXXXXX)
echo "Temporary directory created at: $TEMP_DIR"

# Define the URL for fetching the needed release details
echo "Do you want to download the latest version or a specific version of the Ubuntu image? (latest/specific)"
read -p "Enter your choice: " version_choice

if [ "$version_choice" == "latest" ]; then
    RELEASE_URL="https://api.github.com/repos/Joshua-Riek/ubuntu-rockchip/releases/latest"
elif [ "$version_choice" == "specific" ]; then
    read -p "Enter the specific version tag (e.g., v1.2): " version_tag
    RELEASE_URL="https://api.github.com/repos/Joshua-Riek/ubuntu-rockchip/releases/tags/$version_tag"
else
    echo "Invalid input. Exiting."
    exit 1
fi

# # Define the URL for fetching the latest release details
# RELEASE_URL="https://api.github.com/repos/Joshua-Riek/ubuntu-rockchip/releases/latest"

# Use curl to fetch the download URL for the server image and its SHA checksum file
# DOWNLOAD_URL=$(curl -s "$RELEASE_URL" | jq -r '.assets[] | select(.name | endswith("server-arm64-orangepi-5.img.xz")) | .browser_download_url')
# Use jq's test function to match both 'orangepi5' and 'orangepi-5'
DOWNLOAD_URL=$(curl -s "$RELEASE_URL" | jq -r '.assets[] | select(.name | test("server-arm64-orangepi-?5\\.img\\.xz$")) | .browser_download_url')
# SHA_URL=$(curl -s "$RELEASE_URL" | jq -r '.assets[] | select(.name | endswith("server-arm64-orangepi-5.img.xz.sha256")) | .browser_download_url')
# Use jq's test function to match both 'orangepi5' and 'orangepi-5' for the SHA checksum file
SHA_URL=$(curl -s "$RELEASE_URL" | jq -r '.assets[] | select(.name | test("server-arm64-orangepi-?5\\.img\\.xz\\.sha256$")) | .browser_download_url')

# Check if URLs are fetched successfully
if [ -z "$DOWNLOAD_URL" ] || [ -z "$SHA_URL" ]; then
    echo "No matching release or checksum file found."
    exit 1
fi

# Extract the file names from the URLs
IMAGE_FILE=$(basename "$DOWNLOAD_URL")
SHA_FILE=$(basename "$SHA_URL")

# Download the image and its SHA checksum file into the temporary directory
echo "Downloading Ubuntu server image for Orange Pi..."
wget -O "$TEMP_DIR/$IMAGE_FILE" "$DOWNLOAD_URL"
echo "Downloading SHA checksum file..."
wget -O "$TEMP_DIR/$SHA_FILE" "$SHA_URL"
echo "Download completed."

# Change to the temporary directory for file operations
cd "$TEMP_DIR"

# Verify the SHA checksum
echo "Verifying SHA checksum..."
sha256sum -c "$SHA_FILE" || { echo "Checksum verification failed."; exit 1; }

# Extract the image
echo "Extracting the image..."
xz -d "$IMAGE_FILE"

# Prompt for USB device confirmation
echo "You have selected /dev/$usb_device for the image burning process."
read -p "Proceed with writing the image to /dev/$usb_device? (y/N): " confirm && [[ $confirm == [yY] ]] || exit 1

# Proceed with burning the image to the confirmed USB device
echo "Burning the image to /dev/$usb_device. This will erase all data on the device."
sudo dd if="${IMAGE_FILE%.xz}" of="/dev/$usb_device" bs=4M status=progress conv=fdatasync

# Ensure all writes are flushed
sync

echo "Image burning process completed successfully."

# Clean up
echo "Cleaning up..."
rm -rf "$TEMP_DIR"
echo "Done."

# Mount /dev/sda1 to check for user-data file
echo "Mounting /dev/sda1 to update user-data..."
sudo mkdir -p /mnt/usb_sda1
sudo mount /dev/sda1 /mnt/usb_sda1

# Check if user-data exists in /mnt/usb_sda1
if [[ -f /mnt/usb_sda1/user-data ]]; then
    echo "user-data file found in /mnt/usb_sda1."
else
    echo "Error: user-data file not found in /mnt/usb_sda1. Creating a new one."
fi

# Ask for the hostname
read -p "Enter the hostname for the new setup: " new_hostname

# Conditionally set MAC address based on hostname
if [ "${new_hostname}" == "orange-worker" ]; then
    eth0_mac_id="92:6d:5c:66:ca:c3"
elif [ "${new_hostname}" == "mandarine-worker" ]; then
    eth0_mac_id="8e:73:87:03:50:a6"
else
    eth0_mac_id="put_default_mac_here_if_needed"  # Default MAC or leave empty if not needed
fi

# Proceed with updating user-data
echo "Updating user-data in /mnt/usb_sda1..."
sudo tee /mnt/usb_sda1/user-data > /dev/null <<EOF
#cloud-config

# Set TimeZone and Locale for UK
timezone: Europe/London
locale: en_GB.UTF-8

# Hostname
hostname: ${new_hostname}

# cloud-init not managing hosts file. only hostname is added
manage_etc_hosts: localhost

users:
  - name: pi
    primary_group: users
    groups: [adm, admin]
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: true
    ssh_authorized_keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCvE8ju9IxfwyEj0NSJhqrI2sob6QfpEuCAJurNc2XA54/pldF3CpvJlijTOPk2Q3m115DIE/MIGbltki8z59JdMmd/k+kxoXKfF/oZJmolyr6A6sxmtOyi+2Zcf+T/XPg6OEvYfIV3dK5lsIEUl4fDYRIGKcnzVplfJ/lG7N6IV55zvVzFTaehVA1HasLpJ2wDUUQVGMSnWFf16N8r0CscZebxZAzZoHB1SLUEZcQ3EkcM0+DMRXb9jtvLnnLJ6QNLnYOwS4gQ3Myrh2I1IyhnZIA2UQyYyqL1Z3iFfM27NhRFS8WvltDF1a58uXlN9p8bp6/dZRJnzMhNXrAMkwVixGx+nfmO9RNWHDQU7kUJEqmzXuyf6TjGtl1Csk+YvYpe+m1p4plyXDed5O3NtdHQ0O5BbXii5bLceTY2KucI15Mf4ClWihdVLmipRgwzNSmlZMoI8TRspOaTTI8KZ/VKvmbrKSBaNPKxTkP9+0J3fQPk10Qwc6xOJx80/ldOn30=

# Set MAC address of eth0 at each boot based on the hostname
bootcmd:
  - ip link set dev eth0 down
  - ip link set dev eth0 address ${eth0_mac_id}
  - ip link set dev eth0 up

EOF

echo "Displaying the current content of user-data:"
sudo cat /mnt/usb_sda1/user-data

# After making changes, inform the user
echo "Changes to user-data completed. Your device is ready to use."

# Unmount /dev/sda1 and /dev/sda2 after operations are done
echo "Unmounting /dev/sda1..."
sudo umount /mnt/usb_sda1

echo "USB device is ready to use."