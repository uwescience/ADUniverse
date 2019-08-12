import update_map
import pandas as pd

# FIXME: Call update_map with a value
# FIXME: Test if result is a file descriptor if called with a value
def test_update_map():
  result = update_map.update_map(pd.DataFrame(), pd.DataFrame())
  isinstance(result, object)
