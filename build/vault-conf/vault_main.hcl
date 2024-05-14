# Cluster address for server-to-server communication within a Vault cluster
cluster_addr  = "https://vault.picluster.homelab.com:8201"

# API address for client-to-server communication
api_addr      = "https://vault.picluster.homelab.com:8200"
# Note: If accessing Vault via IP address, ensure the IP is included in the SSL certificate's SAN

# Directory where Vault plugins are stored
plugin_directory = "/etc/vault/plugin"

# Enable the Vault UI
ui = true 

# Disable memory locking (mlock). Not recommended for production, but may be necessary on systems that do not support mlock
disable_mlock = true

# TCP listener configuration for incoming connections
listener "tcp" {
  address     = "0.0.0.0:8200"  # Listen on all interfaces
  tls_cert_file      = "/etc/vault/tls/public.crt"  # TLS certificate file for HTTPS
  tls_key_file       = "/etc/vault/tls/vault.key"   # TLS private key file for HTTPS
  tls_disable_client_certs = true  # Do not require client TLS certificates
}

# Storage backend configuration using Raft for high availability and data storage
storage "raft" {
  path = "/var/lib/vault"  # Directory where Raft data is stored
}

# Logging configuration (optional but recommended for monitoring and troubleshooting)
log_file   = "/var/log/vault/vault.log"  # Path to the log file
log_level  = "info"  # Log verbosity (e.g., "info", "debug")