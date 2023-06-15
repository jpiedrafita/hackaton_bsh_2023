from entsoe import EntsoePandasClient
import pandas as pd


client = EntsoePandasClient(api_key='794ce2cd-1b5a-42b8-9a50-f52076ca828d')
start = pd.Timestamp('20230614', tz='Europe/Warsaw')
end = pd.Timestamp('20230616', tz='Europe/Warsaw')
country_code = 'PT'  # country code
country_code_from = 'FR'  # France
country_code_to = 'PL_CZ' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"

def get_data_fromENTSOE(country_code,timeframe):  #as timeframe as tuple like ('20230614', '20230615')
    print(timeframe)
    start=pd.Timestamp(str(timeframe[0]), tz='Europe/Warsaw')
    end = pd.Timestamp(str(timeframe[1]), tz='Europe/Warsaw')
    ts = client.query_wind_and_solar_forecast(country_code, start=start,end=end)
    return ts
