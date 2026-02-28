"""
MIT License

Copyright (c) 2026 Xpresscat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
"""

from procedures import (
    read_masterfile, read_data_IRA_IRD, read_POS, read_users, read_pos_users, update_masterfile,
    update_data, create_IRA_IRD_POS_REEV, create_IRA_IRD_POS_Retail, create_csv_file_upadate_IRA_IRD)

masterfile_IRA = read_masterfile('file.csv',territory_prefix='IRA_', status='Active')
print(masterfile_IRA)
input("Press Enter to continue...masterfile_IRA")

masterfile_IRD = read_masterfile('file.csv',territory_prefix='IRD_', status='Active')
print(masterfile_IRD)
input("Press Enter to continue...masterfile_IRD")

data_IRA = read_data_IRA_IRD('file2.csv',territory_prefix='IRA',field ='TERRITORY_ACTIVATOR')
print(data_IRA)
input("Press Enter to continue...data_IRA")

data_IRD = read_data_IRA_IRD('file2.csv',territory_prefix='IRD',field ='TERRITORY')
print(data_IRD)
input("Press Enter to continue...data_IRD")


POS = read_POS('file3.csv')
print(POS)
input("Press Enter to continue...POS")

users = read_users('file4.csv')
print(users)
input("Press Enter to continue...users")

pos_users = read_pos_users('file5.csv')
print(pos_users)
input("Press Enter to continue...pos_users")

masterfile_IRA_checked = update_masterfile(masterfile_IRA,users)
print(masterfile_IRA_checked)
input("Press Enter to continue...masterfile_IRA_checked")

masterfile_IRD_checked = update_masterfile(masterfile_IRD,users)
print(masterfile_IRD_checked)
input("Press Enter to continue...masterfile_IRD_checked")

data_IRA_checked = update_data(data_IRA,POS)
print(data_IRA_checked)
input("Press Enter to continue...data_IRA_checked")

data_IRD_checked = update_data(data_IRD,POS)
print(data_IRD_checked)
input("Press Enter to continue...data_IRD_checked")

IRA_POS_REEV = create_IRA_IRD_POS_REEV(masterfile_IRA_checked,data_IRA_checked,field = 'TERRITORY_ACTIVATOR')
print(IRA_POS_REEV)
input("Press Enter to continue...IRA_POS_REEV")

IRA_POS_Retail = create_IRA_IRD_POS_Retail(masterfile_IRA_checked,pos_users)
print(IRA_POS_REEV)
input("Press Enter to continue...IRA_POS_Retail")

IRD_POS_REEV = create_IRA_IRD_POS_REEV(masterfile_IRD_checked,data_IRD_checked,field = 'TERRITORY')
print(IRD_POS_REEV)
input("Press Enter to continue...IRD_POS_REEV")

IRD_POS_Retail = create_IRA_IRD_POS_Retail(masterfile_IRD_checked,pos_users)
print(IRD_POS_REEV)
input("Press Enter to continue...IRD_POS_Retail")

create_csv_file_upadate_IRA_IRD('IRA_update.csv',IRA_POS_REEV,IRA_POS_Retail)

create_csv_file_upadate_IRA_IRD('IRD_update.csv',IRD_POS_REEV,IRD_POS_Retail)

