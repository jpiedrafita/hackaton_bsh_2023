from entsoe import EntsoePandasClient
import pandas as pd

client = EntsoePandasClient(api_key='794ce2cd-1b5a-42b8-9a50-f52076ca828d')

start = pd.Timestamp('20230613', tz='Europe/Brussels')
end = pd.Timestamp('20230614', tz='Europe/Brussels')
country_code = 'BE'  # Belgium
country_code_from = 'FR'  # France
country_code_to = 'DE_LU' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"

ts = client.query_day_ahead_prices(country_code, start=start, end=end)
ts.to_csv('outfile.csv')
print(ts)
