import pandas as pd

'''Read in csv, clean data'''
df = pd.read_excel('input.xlsx', sheet_name='Sheet1', dtype = {'phone1': str, 'phone2': str, 'phone3': str,'phone4': str,'phone5': str,'phone6': str,'phone7': str,'phone8': str})
clean_for_appending = df.drop_duplicates(subset=['Property Address'])

'''Get duplicates based on property address'''

duplicate_for_file_gen = df[df.duplicated('Property Address', keep=False)]
duplicate_for_appending = df[df.duplicated('Property Address', keep='first')]
duplicate_for_appending.reset_index(drop = True, inplace = True)


''' Groupby '''
agg_functions = {'Property Address': 'first', 'Owner 1 Last Name': list} 
test = duplicate_for_file_gen.groupby(duplicate_for_file_gen['Property Address']).aggregate(agg_functions) 

'''Columns for additional owners'''
max_len = max(test['Owner 1 Last Name'].apply(len))
for ii in range(max_len):
    test['Owners%s '%ii] = [item[ii] if ii < len(item) else 'blank' for item in test['Owner 1 Last Name']]


'''Clean up and appending'''
test.pop('Owner 1 Last Name')
test.reset_index(drop = True, inplace = True)
res = (pd.merge(duplicate_for_appending, test, on='Property Address'))

final_output = pd.concat([res, clean_for_appending])

''' Generate output '''
final_output.to_excel('output.xlsx', index=False)

