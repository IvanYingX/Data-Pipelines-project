import os

csv_filename = './Data/Dictionaries/Team_Info.csv'
if not os.path.exists(csv_filename):
    csv_incomplete = './Data/Dictionaries/Teams_to_Complete.csv'
    if not os.path.exists(csv_incomplete):
        create_teamcsv()
    else:
        print(f'Go to {csv_incomplete}, manually check, fill it, \
                and save it as {csv_filename}')
                https://www.wunderground.com/history