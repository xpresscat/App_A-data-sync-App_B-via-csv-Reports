"""
MIT License

Copyright (c) 2026 Xpresscat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
"""

import pandas as pd

def read_masterfile(file_path, encoding='latin-1', territory_prefix='IRA_', status='Active'):
    """
    Reads a CSV file, filters rows where 'territorio' starts with `territory_prefix` 
    and 'Status' equals `status`, and returns a list of dictionaries with the selected columns.

    Args:
    - file_path (str): Path to the CSV file.
    - encoding (str): Encoding used for reading the file. Default is 'latin-1'.
    - territory_prefix (str): The prefix to check at the start of the 'territorio' column. Default is 'IRA'.
    - status (str): The value to check in the 'Status' column. Default is 'Active'.

    Returns:
    - List of dictionaries with filtered rows.
    """
    
    # Read the CSV file with the appropriate encoding and selected columns
    df = pd.read_csv(file_path, usecols=['territorio', 'Username', 'E-mail', 'Status'], encoding=encoding)

    # Filter data where 'territorio' starts with `territory_prefix` and 'Status' equals `status`
    df_filtered = df[
    df['territorio'].str.contains(f'^{territory_prefix}', case=False, na=False) &
    df['Status'].str.contains(f'^{status}$', case=False, na=False)
    ]

    # Convert to list of dictionaries
    data = df_filtered.to_dict(orient='records')

    return data

def read_data_IRA_IRD(file_path, encoding='latin-1', territory_prefix='IRA_',field ='TERRITORY_ACTIVATOR'):
    
    # Read the CSV file with the appropriate encoding and selected columns
    df = pd.read_csv(file_path, usecols=['Account Commercial UUID', field], encoding=encoding)

    # Filter data where 'territorio' starts with `territory_prefix` and 'Status' equals `status`
    df_filtered = df[
    df[field].str.contains(f'^{territory_prefix}', case=False, na=False)
    ]

    # Convert to list of dictionaries
    data = df_filtered.to_dict(orient='records')

    return data  
    
def read_POS(file_path, encoding='latin-1'):
    
    # Read the CSV file with the appropriate encoding and selected columns
    df = pd.read_csv(file_path, usecols=['ISMS Code', 'Reev ID'], encoding=encoding)

    # Filter data where 'territorio' starts with `territory_prefix` and 'Status' equals `status`
    

    # Convert to list of dictionaries
    data = df.to_dict(orient='records')

    return data

def read_users(file_path, encoding='latin-1'):
    
    # Read the CSV file with the appropriate encoding and selected columns
    df = pd.read_csv(file_path, usecols=['Email', 'UserName'], encoding=encoding)

    # Filter data where 'territorio' starts with `territory_prefix` and 'Status' equals `status`
    

    # Convert to list of dictionaries
    data = df.to_dict(orient='records')

    return data

def read_pos_users(file_path, encoding='latin-1'):
    
    # Read the CSV file with the appropriate encoding and selected columns
    df = pd.read_csv(file_path, usecols=['ISMS Code', 'User email'], encoding=encoding)

    # Filter data where 'territorio' starts with `territory_prefix` and 'Status' equals `status`
    

    # Convert to list of dictionaries
    data = df.to_dict(orient='records')

    return data

def update_masterfile(masterfile, users):
    """
    Compares records from masterfile_IRA with users and updates the 'Username' and 'E-mail' fields
    based on the following rules:
    1. If Username + domain_add matches user['Email'], update 'Username' with user's 'Email'.
    2. If E-mail matches user['Email'], update 'E-mail' with user's 'Email'.
    3. If no match, remove the record from masterfile_IRA.

    Args:
    - masterfile_IRA (list): List of dictionaries representing the master records.
    - users (list): List of dictionaries representing the user records.
    
    Returns:
    - list: The updated masterfile_IRA list.
    """
    # Loop through all records in masterfile_IRA
    for record in masterfile[:]:

        domain_add = "@sample.net"

        # Get concatenated email for comparison (Username + domain_add)
        concatenated_email = str(record['Username']) + domain_add
        
        # Flag to track if a match is found
        matched = False
        
        # Loop through all user records and compare
        for user in users:
            # Compare concatenated email or E-mail field
            if concatenated_email.lower() == str(user['Email']).lower():
                # If match, update Username to Email from user
                record['E-mail'] = user['Email']
                matched = True   
                break  # No need to check other users if we already found a match
            
            elif str(record['E-mail']).lower() == str(user['Email']).lower() and str(record['Username']).lower() == str(user['UserName']).lower() :
                # If E-mail matches, update E-mail to user's Email
                record['E-mail'] = user['Email']
                matched = True
                break  # No need to check other users if we already found a match
        
        # If no match is found, delete the record
        if not matched:
            masterfile.remove(record)

    return masterfile

def update_data(data, POSS):

    for record in data[:]:

        matched = False

        for POS in POSS:
            if str(record['Account Commercial UUID']).lower() == str(POS['Reev ID']).lower():
                record['Account Commercial UUID'] = POS['ISMS Code']
                matched = True
                break 
        if not matched:
            data.remove(record)

    return data

def create_IRA_IRD_POS_REEV(masterfile, data, field = 'TERRITORY_ACTIVATOR' ):
    
    IRA_REEV = []   # declare as list (array) of dictionaries
    
    for record in masterfile[:]:
        
        for dat in data:

            territorio = str(dat[field]).lower()

            if str(record['territorio']).lower() in territorio:
                
                ira_entry = {}  # create a new dictionary for each match
                ira_entry['email'] = record['E-mail']
                ira_entry['isms'] = dat['Account Commercial UUID']
                
                IRA_REEV.append(ira_entry)  # add dictionary to list

    df = pd.DataFrame(IRA_REEV)

    # Export to CSV
    #df.to_csv('reev.csv', index=False)
    #print("CSV file created successfully.")

    return IRA_REEV


def create_IRA_IRD_POS_Retail(masterfile, data):
    
    IRA_RETAIL = []   # declare as list (array) of dictionaries
    
    for record in masterfile[:]:
        
        for dat in data:

            email = str(dat['User email']).lower()

            if str(record['E-mail']).lower() in email:
                
                ira_entry = {}  # create a new dictionary for each match
                ira_entry['email'] = dat['User email']
                ira_entry['isms'] = dat['ISMS Code']
                
                IRA_RETAIL.append(ira_entry)  # add dictionary to list

    #df = pd.DataFrame(IRA_RETAIL)

    # Export to CSV
    #df.to_csv('retail.csv', index=False)
    #print("CSV file created successfully.")            

    return IRA_RETAIL

def create_csv_file_upadate_IRA_IRD(file_path,IRX_POS_REEV, IRX_POS_Retail):

    CSV_file = []

    j = 0
    i = 0
    for reev in IRX_POS_REEV[:]:

        j = j + 1
        print(j,i)
        matched = False
        for retail in IRX_POS_Retail:
            if (str(reev['email']).lower() == str(retail['email']).lower() 
                and str(reev['isms']).lower() == str(retail['isms']).lower()
            ):    
                matched = True
                break  # No need to check other users if we already found a match

        if not matched:
            csv_entry = {}  # create a new dictionary for each match
            csv_entry['user_email*'] = reev['email']
            csv_entry['pos_isms_code*'] = reev['isms']
            csv_entry['auth_type*'] = "AZURE"
            csv_entry['remove_1'] = ""
            CSV_file.append(csv_entry)  # add dictionary to list

    for retail in IRX_POS_Retail[:]:

        i = i + 1
        print(j,i)
        matched = False
        for reev in IRX_POS_REEV:
            if (str(retail['email']).lower() == str(reev['email']).lower() 
                and str(retail['isms']).lower() == str(reev['isms']).lower()
            ):    
                matched = True
                break  # No need to check other users if we already found a match

        if not matched:
            csv_entry = {}  # create a new dictionary for each match
            csv_entry['user_email*'] = retail['email']
            csv_entry['pos_isms_code*'] = retail['isms']
            csv_entry['auth_type*'] = "AZURE"
            csv_entry['remove_1'] = "1"
            CSV_file.append(csv_entry)  # add dictionary to list

                
    print(CSV_file)
    
    df = pd.DataFrame(CSV_file)

    # Export to CSV
    df.to_csv(file_path, index=False)
    input("Press Enter to continue...CSV_file")      

                    
                


"""
def read_data_IRD(file_path, encoding='latin-1', territory_prefix='IRD_'):
    
    # Read the CSV file with the appropriate encoding and selected columns
    df = pd.read_csv(file_path, usecols=['Account Commercial UUID', 'TERRITORY'], encoding=encoding)

    # Filter data where 'territorio' starts with `territory_prefix` and 'Status' equals `status`
    df_filtered = df[
    df['TERRITORY'].str.contains(f'^{territory_prefix}', case=False, na=False)
    ]

    # Convert to list of dictionaries
    data = df_filtered.to_dict(orient='records')

    return data

"""  
