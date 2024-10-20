from pathlib import Path
import pandas as pd

pd.set_option("display.max_columns", None)

def data_describe(dataframe):
     """This function takes a dataframe and returns information that
        describes the data.
 
        Parameters:
        dataframe (df): A pandas dataframe
 
        Returns:
        str: information about data
 
     """
     
     print(dataframe.shape)
     print(dataframe.head(5))
     print(dataframe.tail(5))
     print(dataframe.columns)
     print(dataframe.dtypes)
     print(dataframe.info)
     print(dataframe.describe)
     information = ""
     return information

def prepare_dataframe(df, npc_codes):

    # Remove nulls
    df = df.drop(index=0)
    df = df.drop(index=17)
    df = df.drop(index=31)
    df = df.reset_index(drop=True)

    # Make floats into ints
    float_columns = df.select_dtypes(include=['float64']).columns.tolist()
    for column in float_columns:
         df[column] = df[column].astype('int')
    
    # Change dates to datetime
    df['start'] = pd.to_datetime(df['start'], format='%d/%m/%Y')
    df['end'] = pd.to_datetime(df['end'], format='%d/%m/%Y')

    # Drop unnecessary columns
    #print(df.columns)
    df = df.drop(columns=['URL', 'disabilities_included', 'highlights'])
    #print(df_prepared.columns)

    missing_rows = df[df.isna().any(axis=1)]
    missing_columns = df.columns[df.isna().any(axis=0)]

    df = df.merge(npc_codes, how='left', left_on='country', right_on='Name')
    print(missing_columns, missing_rows)
    df_prepared = df.drop(columns=['Name'])

    # Strip whitespace
    df_prepared['type'] = df_prepared['type'].str.strip()
    df_prepared['type'] = df_prepared['type'].str.lower()

    duration = (df_prepared['end'] - df_prepared['start']).dt.days
    df_prepared.insert(
        loc=df_prepared.columns.get_loc('end') + 1,
        column='duration',
        value=duration
    )
    return df_prepared


if __name__ == '__main__':


    project_root = Path(__file__).parent.parent

    # Find the .csv file relative to the project root and join to that path the data folder and then the example.csv file
    csv_file = project_root.joinpath('tutorialpkg', 'data', 'paralympics_events_raw.csv')
    # csv_file = project_root / 'data' / 'example.csv' # this notation would also work, even though you think the '/' is only unix/macOS

    csvdf = pd.read_csv(csv_file)

    excel_file = project_root.joinpath('tutorialpkg', 'data', 'paralympics_all_raw.xlsx')
    
    try:
        exceldf = pd.read_excel(excel_file, sheet_name=1)
    except FileNotFoundError as e:
        print(f"File not found. Please check the file path. Error: {e}")

    medalstandingsdf = pd.read_excel(excel_file, sheet_name="medal_standings")

    #data_describe(csvdf)
    #data_describe(exceldf)
    #data_describe(medalstandingsdf)

    #csvdf = prepare_dataframe(csvdf)


    replacement_names = {
    'UK': 'Great Britain',
    'USA': 'United States of America',
    'Korea': 'Republic of Korea',
    'Russia': 'Russian Federation',
    'China': "People's Republic of China"
    }

    csvdf['countries'].replace(to_replace=replacement_names)

    npc_file = project_root.joinpath('tutorialpkg', 'data', 'npc_codes.csv')
    npc_codes = pd.read_csv(npc_file, encoding='utf-8', encoding_errors='ignore', usecols = ['Code', 'Name'])
    merged_df = prepare_dataframe(csvdf, npc_codes)

    save_path = project_root.joinpath('tutorialpkg', 'data', 'paralympics_events_prepared.csv')
    merged_df.to_csv(save_path, index=False)

    #print(merged_df[['country', 'Code', 'Name']])
    print(merged_df['type'].unique())