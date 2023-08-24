from typing import Optional

import numpy as np
import pandas as pd

class DataReader:
    def __init__(
        self,
        df: pd.DataFrame,
        seed: Optional[int] = None,
    ) -> None:

        if seed:
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng(None)

        self.df = df

    def sample(
        self,
        by: str,
        size: int,
        weights: Optional[str] = None,
        with_replacement: bool = True,
    ) -> pd.DataFrame:

        if weights is None:
            unique_by = self.df[[by]].drop_duplicates(subset=by, keep="first")
            weight_col = None
        else:
            unique_by = self.df[[by, weights]].drop_duplicates(subset=by, keep="first")
            weight_col = unique_by[weights]

        id_col = unique_by[by]
        if with_replacement or (size <= len(id_col)):
            sample = self.rng.choice(id_col, p=weight_col, replace=with_replacement, size=size)
        elif size <= len(self.df):
            # edge case:
            # sampling without replacement and non-unique sampling column while size
            # is larger than number of unique values to sample from
            sample = id_col.tolist()  # type: ignore
            self.rng.shuffle(sample)
        else:
            msg = f"Cannot sample size ({size}) larger than dataset ({len(self.df)}) without replacement!"
            raise ValueError(
                msg,
            )

        if not with_replacement:
            # Faster shortcut that is possible if sampling is done without replacement.
            # Therefore implemented separately.
            df = self.df.loc[self.df[by].isin(sample), :]
            df = df.iloc[:size]
        else:
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
