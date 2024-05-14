#!/usr/bin/env sh

# Function to generate a timestamp in the format "Mon 01 2024 00:00:00 GMT"
timestamp() {
  date "+%b %d %Y %T %Z"
}

# Vault server URL. Replace the placeholder with the actual Vault server address.
URL=https://vault.picluster.homelab.com:8200

# Path to the file containing the unseal keys for Vault.
KEYS_FILE=/etc/vault/unseal.json

# Path to the log file where script output will be recorded.
LOG=/var/log/vault-unseal.log

# Flag to skip TLS verification in curl commands. Set to true to skip verification.
SKIP_TLS_VERIFY=true

# Parameters for curl command based on whether TLS verification is skipped.
CURL_PARAMS=$([ "$SKIP_TLS_VERIFY" = true ] && echo "-sk" || echo "-s")

# Ensure the log file exists and set its permissions correctly.
# These commands might fail if the script doesn't have the necessary permissions,
# so it's recommended to set up the log file and permissions outside this script.
touch $LOG
chown vault:vault $LOG
chmod 660 $LOG

# Log the start of the unseal process with a timestamp.
echo "$(timestamp): Vault-unseal initiated" | tee -a $LOG
echo "-------------------------------------------------------------------------------" | tee -a $LOG

# Check if Vault is initialized by querying its health endpoint.
initialized=$(curl $CURL_PARAMS $URL/v1/sys/health | jq '.initialized')

# If Vault is initialized, proceed with the unseal process.
if [ "$initialized" = true ]; then
  echo "$(timestamp): Vault is initialized" | tee -a $LOG

  # Continuously check if Vault is sealed and attempt to unseal it.
  while true; do
    status=$(curl $CURL_PARAMS $URL/v1/sys/health | jq '.sealed')
    
    # If Vault is sealed, attempt to unseal it using keys from the unseal.json file.
    if [ "$status" = true ]; then
        echo "$(timestamp): Vault is sealed. Attempting to unseal" | tee -a $LOG
        
        # Extract unseal keys from the JSON file and use them to unseal Vault.
        for i in $(jq -r '.unseal_keys_b64[]' $KEYS_FILE); do 
          curl $CURL_PARAMS --request PUT --data "{\"key\": \"$i\"}" $URL/v1/sys/unseal
        done

        # Wait for 10 seconds before checking the seal status again.
        sleep 10
    else
        # If Vault is unsealed, log the success and exit the loop.
        echo "$(timestamp): Vault successfully unsealed" | tee -a $LOG
        break
    fi
  done
else
  # If Vault is not initialized, log this status.
  echo "$(timestamp): Vault hasn't been initialized" | tee -a $LOG
fi
