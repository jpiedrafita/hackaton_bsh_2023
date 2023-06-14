from entsoe import EntsoePandasClient
import pandas as pd
from energychart import plot_from_json


client = EntsoePandasClient(api_key='794ce2cd-1b5a-42b8-9a50-f52076ca828d')

start = pd.Timestamp('20230614', tz='Europe/Brussels')
end = pd.Timestamp('20230616', tz='Europe/Brussels')
country_code = 'PL'  # Belgium
country_code_from = 'FR'  # France
country_code_to = 'DE_LU' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"

ts = client.query_day_ahead_prices(country_code, start=start, end=end)
ts.to_csv('outfile.csv')
out_json=ts.to_json(date_format='%Y-%m-%d %H:%M:%S')

print('Json:')
print(out_json)
print('DATAFRAME:')
print(ts)


ts = client.query_wind_and_solar_forecast(country_code, start=start,end=end, psr_type=None)
print(ts)

print("sdsdsdsd")
ts = client.query_generation_forecast(country_code, start=start,end=end)
print(ts)
