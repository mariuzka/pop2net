import random
from typing import Optional

import pandas as pd


class DataReader:
    def __init__(
        self,
        df: pd.DataFrame,
        seed: Optional[int] = None,
    ) -> None:

        if seed:
            self.rng = random.Random(seed)
        else:
            self.rng = random.Random()

        self.df = df

    def sample(self, by: str, size: int, weights: Optional[str] = None) -> pd.DataFrame:

        if weights is None:
            unique_by = self.df[[by]].drop_duplicates(subset=by, keep="first")
            weight_col = None
        else:
            unique_by = self.df[[by, weights]].drop_duplicates(subset=by, keep="first")
            weight_col = unique_by[weights].tolist()

        id_col = unique_by[by].tolist()
        sample = self.rng.choices(id_col, weights=weight_col, k=size)

        subset_dfs = []
        len_counter = 0
        for sample_id in sample:

            subset = self.df[self.df[by] == sample_id]
            subset_dfs.append(subset)

            len_counter += len(subset)
            if len_counter >= size:
                break

        df = pd.concat(subset_dfs, axis=0)
        df = df.iloc[:size]

        return df
