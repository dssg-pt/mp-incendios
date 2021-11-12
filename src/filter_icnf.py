# Imports
import pandas as pd
from pathlib import Path

# Constants
icnf_file_2015 = Path(__file__).parent.resolve() / '..' / 'data' / 'raw' / 'icnf_2015.csv'
icnf_file_2016 = Path(__file__).parent.resolve() / '..' / 'data' / 'raw' / 'icnf_2016.csv'
icnf_file_2017 = Path(__file__).parent.resolve() / '..' / 'data' / 'raw' / 'icnf_2017.csv'
icnf_file_2018 = Path(__file__).parent.resolve() / '..' / 'data' / 'raw' / 'icnf_2018.csv'
icnf_file_2019 = Path(__file__).parent.resolve() / '..' / 'data' / 'raw' / 'icnf_2019.csv'
icnf_file_2020 = Path(__file__).parent.resolve() / '..' / 'data' / 'raw' / 'icnf_2020.csv'
icnf_file_2021 = Path(__file__).parent.resolve() / '..' / 'data' / 'raw' / 'icnf_2021.csv'
OUTPUT_PATH = Path(__file__).parent.resolve() / '..' / 'data' / 'filtered_data' / 'icnf_2015_2021_filtered.csv'
OUTPUT_COLUMNS = ['CONCELHO', 'DHINICIO', 'AREATOTAL', 'X', 'Y', 'MES', 'ANO']

if __name__ == '__main__':

    # Reading and merging everything into one big dataset
    icnf_files = [pd.read_csv(i) for i in [icnf_file_2015, icnf_file_2016, icnf_file_2017, icnf_file_2018, icnf_file_2019, icnf_file_2020, icnf_file_2021]]
    merged = pd.concat(icnf_files, axis=0)
    print(f"In total, we have {merged.shape} entries in the dataset.")

    # Area filtering
    print("Let's filter by burnt area (remove all below the 5% percentile)...")
    n_merged = merged[merged['AREATOTAL'] < merged['AREATOTAL'].quantile(.05)].shape[0]
    print(f"{n_merged} rows to be removed...")
    area_quantile = merged['AREATOTAL'].quantile(.05)
    merged = merged[merged['AREATOTAL'] >= area_quantile].copy()

    print("Done! ✔")
    print("---\n")

    # False Alarm
    print("Let's filter by false alarme...")
    n_false = merged[merged['FALSOALARME'] == 1].shape[0]
    print(f"{n_false} rows to be removed...")
    merged = merged[merged['FALSOALARME'] != 1].copy()

    print("Done! ✔")
    print("---\n")

    # Saving relevant columns
    print(f"Filtering the relevant columns, {OUTPUT_COLUMNS}...")
    out_dataset =  merged[OUTPUT_COLUMNS]

    # Type castings
    for oc in OUTPUT_COLUMNS:
        out_dataset[oc] = out_dataset[oc].astype(str).copy()

    print(out_dataset.shape)
    
    # Let's just check if there are NaNs
    print(f"Are there NaNs? {out_dataset.isnull().values.any()}")
    out_dataset.to_csv(OUTPUT_PATH, index=False)
    print(f"New dataset saved with shape {out_dataset.shape} saved to {OUTPUT_PATH}. Done!")
