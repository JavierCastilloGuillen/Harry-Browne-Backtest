
import pandas as pd
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

start_session = pd.Timestamp('2005-01-3', tz='utc')
end_session = pd.Timestamp('2021-06-25', tz='utc')
register(
    'custom-csvdir-bundle',
     csvdir_equities(
        ['daily'], 
        '/Users/javie/Desktop/Harry Browne Backtest/data/csvs', 
        ),
        calendar_name='NYSE',
        start_session=start_session,
        end_session=end_session
        )
"""
Some commandline reference code on ingesting and cleaning up data bundles
zipline bundles
zipline clean -b custom-csvdir-bundle --keep-last 1
zipline clean -b custom-csvdir-bundle --after 2020-10-1
zipline ingest -b test-csvdir
"""