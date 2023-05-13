import pandas as pd

def read_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data, None
    except Exception as e:
        return None, str(e)
    