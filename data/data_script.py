import pandas as pd
import mysql.connector
import pyzipper
import os

db_config = {
    'host': '209.162.62.168',
    'user': 'interview_user',
    'password': 'dAQ8ryJ72!BfWRvM',
    'database': 'interview_db',
    'port': 3306
}

# Establishing a connection with the database
try:
    connection = mysql.connector.connect(**db_config)
    print("Database connected successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Using the SQL Query to extract the data
query = """
SELECT 
    m.MemberID,
    COUNT(DISTINCT r.callid) AS TotalUniqueCalls,
    d.drName,
    d.drAddress,
    d.drCity,
    d.drState,
    d.drZip
FROM Members m
JOIN results r ON m.MemberID = r.memberid
JOIN dispositions disp ON r.dispositionid = disp.dispositionid
JOIN Doctors d ON  m.drNpi = d.drNpi
WHERE 
    m.memberState = 'PA' 
    AND r.resulttime BETWEEN '2023-01-01' AND '2023-12-31'
    AND NOT (d.drCity = 'PHILADELPHIA' AND d.drState = 'PA') 
GROUP BY m.MemberID, d.drName, d.drAddress, d.drCity, d.drState, d.drZip;
"""

# Fetch the data
cursor = connection.cursor(dictionary=True)
cursor.execute(query)
data = cursor.fetchall()
df = pd.DataFrame(data)  
cursor.close()


# Generating a Pipe-Delimited CSV File
output_file = "python_datareport.csv"
df.to_csv(output_file, sep='|', index=False)

