import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    
    
    final_df = data[['dateTime','city', 'latitude', 'longitude', 'aqi', 'category', 'dominantPollutant', 'displayName',
       'fullName', 'concentration_value']]

       # Extract columns needed for pivot
    pivot_cols = ['dateTime', 'city', 'latitude', 'longitude', "category", "aqi"]

    # Create a pivot table
    df_pivot = pd.pivot_table(final_df, values='concentration_value', index=pivot_cols, columns='displayName', aggfunc='first').reset_index()

    # Rename columns for clarity
    df_pivot.columns.name = None  # Remove the 'displayName' label from the columns
    df_pivot['dateTime'] = pd.to_datetime(df_pivot['dateTime'])
    df_pivot['Day'] = df_pivot['dateTime'].dt.date
    df_pivot['Time'] = df_pivot['dateTime'].dt.time
    df_pivot = df_pivot.drop(columns=['dateTime'], axis=1)
    df_pivot = df_pivot.rename(columns={'city': 'City','latitude': 'Lat','longitude': 'Lon', 'category': 'Category', 'aqi': 'AQI','CO': 'CO_concentration', 'NO2': 'NO2_concentration', 'O3': 'O3_concentration',
                                        'PM10': 'PM10_concentration', 'PM2.5': 'PM25_concentration', 'SO2': 'SO2_concentration'})

    df_pivot['Day'] = pd.to_datetime(df_pivot['Day'])


    print(df_pivot.info())


    return df_pivot


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
