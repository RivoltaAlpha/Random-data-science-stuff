import ftplib

ftp_host = '48.216.216.1'
ftp_user = 'tiff'
ftp_pass = 'Photography@21'

local_file = "Typyreport.zip"
remote_file = "Typyreport.zip"   

# Connect to the FTP serve
ftp = ftplib.FTP(timeout=60)
ftp.connect(ftp_host)
ftp.login(ftp_user, ftp_pass)

# Change to the 'Tiffany' subdirectory
ftp.cwd('files')

# Open the local file in binary mode and upload it
with open(local_file, 'rb') as file:
    ftp.storbinary(f'STOR {remote_file}', file)

# Close the FTP connection
ftp.quit()

print(f"File '{local_file}' uploaded successfully to the 'Tiffany' directory on the FTP server.")






