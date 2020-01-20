import csv
import pandas as pd
import numpy as np
from datetime import datetime

# Decorator for printing function results. We return a results value to enable
# automated testing of the methods upon refactoring.

def output_decorator(msg=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            
            if msg:
                print(msg)
            else:
                print(f'{func.__name__} is now started')
            
            t = func(*args, **kwargs)
            print(f'{t["results"]} instances detected')
            print(f'Results saved at {t["output"]}')
            return t["results"]
        return inner
    return wrapper


class Test_1_Procedures:
    
    # 3.1.1 - Test 1.1 Check for gaps in journal entry numbers
    # This method assumes JE's are already sorted in ascending order
    
    @output_decorator()
    def check_for_gaps_in_JE_ID(
            GL_Detail, Journal_ID_Column = 'Journal_ID',
            output_file = 'Output_Folder/Test_3_1_1_check_for_gaps_in_JE_ID.csv'):        
        
        gaps = []
        previous = None
        
        # Loop through each Journal ID, compare to previous
        for item in GL_Detail[Journal_ID_Column]:
            if previous and (item - previous > 1):
                gaps.append([previous, item])
            previous = item      
        
        # Write results to the output csv file, set output_file = None for no
        # output_file.
        if output_file:
            with open(output_file, 'w') as file:
                writer = csv.writer(file)
                writer.writerow([f'Gap identified! Start gap number is followed by end gap number'])
                writer.writerows(gaps)
                writer.writerow(['Test Results:']) 
                writer.writerow([f'Total of {len(gaps)} gaps found'])
        
        return ({"results":len(gaps), "output":output_file})


    # 3.1.2 Compare listing of journal entry numbers from system to log file
    
    @output_decorator()
    def comparison_of_entries_of_GL_and_log_file(
            GL_Detail, Log_File, Journal_ID_Column = 'Journal_ID',
            output_file = "Output_Folder/Test_3_1_2_Comparison_of_Entries_of_GL_and_Log_File.csv"):
  
        In_GL_not_in_LOG = set(GL_Detail[Journal_ID_Column]) - set(Log_File[Journal_ID_Column])
        In_LOG_not_in_GL = set(Log_File[Journal_ID_Column]) - set(GL_Detail[Journal_ID_Column])
        
        if output_file:
            with open(output_file, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(['Following %a journal entries exist in General Ledger, but missing from the Log File:'
                             %(len(In_GL_not_in_LOG))])
                writer.writerow(list(In_GL_not_in_LOG))
                writer.writerow(['-'*85])
                writer.writerow(['Amounts of following %a journal entries do not match their amounts in Log File:'
                         %(len(In_LOG_not_in_GL))])
                writer.writerow(list(In_LOG_not_in_GL))

        return ({"results": (len(In_LOG_not_in_GL) + len(In_GL_not_in_LOG)),
                "output": output_file})

    # 3.1.3 Test 1.3 Compare total debit amounts and credit amounts of journal entries to system control totals by entry type
    
    @output_decorator()
    def comparison_of_amounts_of_GL_and_log_file(
            GL_Detail, Log_File, Journal_ID_Column = 'Journal_ID',
            Cr_Db_Indicator = 'Amount_Credit_Debit_Indicator',
            output_file = 'Output_Folder/Test_3_1_3_comparison_of_amounts_of_GL_and_log_file.csv'):
        
        index_cols = [Journal_ID_Column, Cr_Db_Indicator]

        recon_gl_to_log = GL_Detail.pivot_table(
                index = index_cols, values = 'Net',
                aggfunc = sum).reset_index().merge(
                        Log_File, on = index_cols, 
                        how = 'outer').fillna(0)

        recon_gl_to_log['Comparison'] = round(abs(recon_gl_to_log['Net']), 2) - round(abs(recon_gl_to_log['Total']), 2)
        recon_gl_to_log = recon_gl_to_log.drop('Entered_Date', axis=1)
        recon_gl_to_log = recon_gl_to_log.drop('Entered_Time', axis=1)
        
        failed_test = recon_gl_to_log.loc[recon_gl_to_log['Comparison'] != 0]
        
        if output_file:
            failed_test.to_csv(output_file)
        
        return ({"results": len(failed_test), "output": output_file})

class Test_2_Procedures:    
    # 3.2.1 - Examine population for missing or incomplete journal entries
    # Pivot by Journal_ID and make sure Net is 0 for each Journal ID, to check if debits and credits are equal for each entry

    @output_decorator()
    def check_for_incomplete_entries(GL_Detail,
                output_file='Output_Folder/Test_3_2_1_check_for_incomplete_entries.csv',
                Journal_ID_Column = 'Journal_ID'):
        
        GL_Pivot = GL_Detail.pivot_table(index=Journal_ID_Column, values='Net', aggfunc=sum)
        failed_test = GL_Pivot.loc[round(GL_Pivot['Net'], 2) != 0]
        failed_test = pd.DataFrame(failed_test.to_records())
        
        if output_file:
            failed_test.to_csv(output_file)
        
        return ({"results": len(failed_test[Journal_ID_Column]), "output": output_file})

    # 3.2.2 - Examine possible duplicate account entries
    # Check for Journal Entries that have same account and amount in the same period

    @output_decorator()
    def check_for_duplicate_entries(GL_Detail, Journal_ID_Column = 'Journal_ID',
                output_file='Output_Folder/Test_3_2_2_check_for_duplicate_entries.csv'):
        
        GL_Pivot = GL_Detail.pivot_table(index=['GL_Account_Number', 'Period', 'Net'], 
                                                            values=Journal_ID_Column, aggfunc= np.count_nonzero)
        GL_Pivot.columns = ['Journal_Entry_Count']
        Duplicates = GL_Pivot.loc[GL_Pivot['Journal_Entry_Count'] != 1]
        Duplicates = pd.DataFrame(Duplicates.to_records())
        GL_Copy = GL_Detail[['Journal_ID', 'GL_Account_Number', 'Period', 'Net']].copy()
        failed_test = GL_Copy.merge(Duplicates, on = ['GL_Account_Number', 'Period', 'Net'], how = 'right').fillna(0)
        
        if output_file:
            failed_test.to_csv(output_file)
        
        return ({'results':len(failed_test[Journal_ID_Column]),
                    'output':output_file})

    # 3.2.3 - Examine round-dollar entries
    # Devide Amounts by 1000 and look for remainder of 0 to check for journal entries with exact amounts in '000s

    @output_decorator()
    def check_for_round_dollar_entries(GL_Detail,
                Journal_ID_Column='Journal_ID',
                output_file='Output_Folder/Test_3_2_3_check_for_round_dollar_entries.csv'):
        
        GL_Copy = GL_Detail[[Journal_ID_Column, 'GL_Account_Number', 'Period', 'Net']].copy()
        GL_Copy['1000s Remainder'] = GL_Copy['Net'] % 1000
        failed_test = GL_Copy.loc[GL_Copy['1000s Remainder'] == 0] 
        
        if output_file:
            failed_test.to_csv(output_file)

        return ({'results':len(failed_test[Journal_ID_Column]),
                    'output':output_file})

    # 3.2.4 - Examine post-date entries:
    # Check if Document Date was later than Entry Date
    # Document_Date does not appear in Data Standards
    # optimize&clarify

    @output_decorator()
    def check_for_post_date_entries(GL_Detail,
                Journal_ID_Column='Journal_ID',
                output_file='Output_Folder/Test_3_2_4_check_for_post_date_entries.csv'):

        GL_Copy = GL_Detail[['Journal_ID', 'Document_Date', 'Entered_Date', 'Period', 'Net']].copy()
        failed_test = GL_Copy.loc[GL_Copy['Document_Date'] > (GL_Copy['Entered_Date'] + 100)] #optimize&"accurify"
   
        if output_file:
            failed_test.to_csv(output_file)
    
        return ({'results':len(failed_test[Journal_ID_Column]),
                    'output':output_file})


    # 3.2.5 - Examine entries posted on weekends/nights
    # Check if Entry Date falls on Saturday or Sunday
    
    @output_decorator()
    def check_for_weekend_entries(GL_Detail,
                Journal_ID_Column='Journal_ID',
                output_file='Output_Folder/Test_3_2_5.1_check_for_weekend_entries.csv'):
        
        GL_Copy = GL_Detail[[Journal_ID_Column, 'Entered_Date', 'Entered_Time']].copy()
        GL_Copy['Entry_Date_Time_Formatted'] = pd.to_datetime(GL_Copy['Entered_Date'].astype(str) + 
                                                              GL_Copy['Entered_Time'].astype(str), format='%Y%m%d%H%M%S')
        GL_Copy['WeekDayNo'] = GL_Copy['Entry_Date_Time_Formatted'].apply(lambda x: x.isoweekday())
        failed_test = GL_Copy.loc[GL_Copy['WeekDayNo'] >= 6]
        
        if output_file:
            failed_test.to_csv(output_file)

        return ({'results':len(failed_test[Journal_ID_Column]),
                    'output':output_file})

    # Check if Entry Time falls on between 8pm and 6am

    @output_decorator()
    def check_for_nights_entries(GL_Detail,
                Journal_ID_Column='Journal_ID',
                output_file='Output_Folder/Test_3_2_5.2_check_for_nights_entries.csv'):

        GL_Copy = GL_Detail[['Journal_ID', 'Entered_Date', 'Entered_Time']].copy()
        GL_Copy['Entry_Date_Time_Formatted'] = pd.to_datetime(GL_Copy['Entered_Date'].astype(str) + 
                                                              GL_Copy['Entered_Time'].astype(str), format='%Y%m%d%H%M%S')
        GL_Copy['Hour'] = GL_Copy['Entry_Date_Time_Formatted'].dt.hour
        failed_test = GL_Copy.loc[(GL_Copy['Hour'] >= 20) | (GL_Copy['Hour'] <= 5)]
        
        if output_file:
            failed_test.to_csv(output_file)

        return ({'results':len(failed_test[Journal_ID_Column]),
                    'output':output_file})

    # 3.2.6 - Summarize by person, type and period in order to identify individuals who normally do not post entries, 
    # and to identify accounts that are normally not used.
    # Check for individuals who posted 10 or fewer entries and identify entries made by these individuals
    
    @output_decorator()
    def check_for_rare_users(GL_Detail,
                Journal_ID_Column='Journal_ID',
                output_file='Output_Folder/Test_3_2_6.1_check_for_rare_users.csv'):
    
        GL_Pivot = GL_Detail.pivot_table(index=['Entered_By'], values='Journal_ID', 
                                                           aggfunc=np.count_nonzero).fillna(0)
        Rare_Users = GL_Pivot.loc[GL_Pivot['Journal_ID'] <= 10]
        Rare_Users = pd.DataFrame(Rare_Users.to_records())
        GL_Copy = GL_Detail[['Journal_ID', 'GL_Account_Number', 'Entered_By']].copy()
        failed_test = GL_Copy.merge(Rare_Users, on = ['Entered_By'], how = 'right').fillna(0)
        
        if output_file:
            failed_test.to_csv(output_file)

        return ({'results':len(failed_test['Entered_By']),
                    'output':output_file})

    # Check for accounts that were used 3 or fewer times and identify entries made to these accounts
    
    @output_decorator()
    def check_for_rare_accounts(GL_Detail,
                Journal_ID_Column='Journal_ID',
                output_file='Output_Folder/Test_3_2_6.2_check_for_rare_accounts.csv'):

        GL_Pivot = GL_Detail.pivot_table(index=['GL_Account_Number'], values='Journal_ID', 
                                                            aggfunc=np.count_nonzero).fillna(0)
        Rare_Accounts = GL_Pivot.loc[GL_Pivot['Journal_ID'] <= 3]
        Rare_Accounts = pd.DataFrame(Rare_Accounts.to_records())
        GL_Copy = GL_Detail[['Journal_ID', 'GL_Account_Number', 'Entered_By']].copy()
        failed_test = GL_Copy.merge(Rare_Accounts, on = ['GL_Account_Number'], how = 'right').fillna(0)
        
        if output_file:
            failed_test.to_csv(output_file)
        
        return ({'results':len(failed_test['GL_Account_Number']),
                    'output':output_file})
