from typing import Optional

import pandas as pd
import plotly.express as px
from flytekit import task, workflow


@task(disable_deck=False)
def iris_data(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
) -> pd.DataFrame:
    data = px.data.iris()
    if sample_frac is not None:
        data = data.sample(frac=sample_frac, random_state=random_state)
    return data


@workflow
def wf(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
):
    iris_data(sample_frac=sample_frac, random_state=random_state)
