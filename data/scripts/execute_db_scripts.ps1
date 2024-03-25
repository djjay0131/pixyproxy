# PowerShell Script
# File: /data/scripts/create_db.ps1
# Description: This script will execute the create.sql and schema.sql scripts to create the database and schema.

# Execute scripts
Get-Content .\create.sql | mysql -u root -p 
Get-Content .\schema.sql | mysql -u pixyproxy -p