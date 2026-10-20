import plotly.express as px

def test_dataset_not_empty():
    df = px.data.tips()
    assert len(df) > 0
    assert {"total_bill", "tip"}.issubset(df.columns)
