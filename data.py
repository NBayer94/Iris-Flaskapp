import pandas as pd
from sklearn.datasets import load_iris

def load_data():
    """
    Returns iris data
    """
    df = load_iris(as_frame=True)
    df = df['data'].join(df['target'])
    return df