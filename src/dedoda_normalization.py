import pandas as pd
from pathlib import Path

if __name__ == '__main__':

    # Reading
    data_filepath = Path(__file__).parent.resolve() / '..' / 'data' / 'filtered_data' / 'All_data_1980_2021_grouped_centroids.csv'
    data = pd.read_csv(data_filepath) 
    print(f'Initial shape is {data.shape}\n')

    # First, the manual fixes
    loc_error_vb = data.loc[(data.concelho == 'Vila Do Bispo')].index.values[0]
    vb_x = data.loc[data.loc[(data.concelho == 'Vila do Bispo')].index.values[0]].x
    vb_y = data.loc[data.loc[(data.concelho == 'Vila do Bispo')].index.values[0]].y
    data.loc[loc_error_vb, "x"] = vb_x
    data.loc[loc_error_vb, "y"] = vb_y

    loc_error_tb = data.loc[(data.concelho == 'Terras De Bouro') & (data.year == 2002) & (data.month==5)].index.values[0]
    tb_x = data.loc[data.loc[(data.concelho == 'Terras de Bouro')].index.values[0]].x
    tb_y = data.loc[data.loc[(data.concelho == 'Terras de Bouro')].index.values[0]].y
    data.loc[loc_error_tb, "x"] = tb_x
    data.loc[loc_error_tb, "y"] = tb_y

    # Now let's do the "Do/Da/De" harmonization
    data.concelho = data.concelho.str.replace(" Da "," da ")
    data.concelho = data.concelho.str.replace(" De "," de ")
    data.concelho = data.concelho.str.replace(" Do "," do ")

    # We will have repeated councils/year/months
    dup_councils_xy = data[data.duplicated(['concelho','month','year'], keep='first')].index.tolist()
    dup_councils_noxy = data[data.duplicated(['concelho','month','year'], keep='last')].index.tolist()

    # For each council/year/month combination, find the duplicate council in `dup_councils_noxy` and add its burnt area
    for loc_xy, loc_noxy in zip(dup_councils_xy, dup_councils_noxy): 
        new_sum = data.loc[loc_xy]["sum"] + data.loc[loc_noxy]["sum"]
        data.loc[loc_xy, "sum"] = new_sum

    # Removing the duplicate councils with no xy and whose are has already been added
    data = data.drop(dup_councils_noxy)
    print(f'Final shape is {data.shape}\n')

    # Checking if we have duplicates, any NaN xy and the two problematic positions
    print("\nDo we have duplicates?\n")
    print(data[data.duplicated(['concelho','month','year'])])

    print("\nDo we have any NaN in the coordinates?\n")
    print(data[(data.isnull().any(axis=1))])

    print("\nHow's Terras de Bouro in May 2002 looking like?\n")
    print(data[(data.concelho == 'Terras de Bouro') & (data.year == 2002) & (data.month==5)])

    print("\nHow's Vila do Bispo in June 2008 looking like?\n")
    print(data[(data.concelho == 'Vila do Bispo') & (data.year == 2008) & (data.month==6)])