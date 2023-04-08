import nltk
import pandas as pd
from typing import Any, List
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from sklearn.base import BaseEstimator, TransformerMixin

from parsemanager import ParseManager

nltk.download('stopwords')


class TATransformer(BaseEstimator, TransformerMixin):

    _parsers = []

    def __init__(
            self,
            use_stopwords: bool = True,
            save_path: str = 'transformed_df.csv',
            load_path: bool = None):
        self.use_stopwords = use_stopwords
        self.save_path = save_path
        self.load_path = load_path

    def fit(self, X: pd.DataFrame, y: Any = None):
        self.morph_ = MorphAnalyzer()
        self.stopwords_ = set()
        self.new_cols_ = ParseManager.get_col_names()

        if self.use_stopwords:
            self.stopwords_ = \
                self.stopwords_ or set(stopwords.words('russian'))

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.load_path and self.load_path.endswith('.csv'):
            X = pd.read_csv(self.load_path)
        else:
            X = X.copy()
            X['text'] = X['text'].str.lower()

            new_data = pd.DataFrame(
                list(map(self.parse_text, X['text'])),
                columns=self.new_cols_
            )

            X = pd.concat([
                X,
                new_data
            ], axis=1)

            if self.save_path:
                if not self.save_path.endswith('.csv'):
                    raise ValueError("expected csv destination file")
                X.to_csv(self.save_path, index=False)

        return X

    def parse_text(self, text: str) -> List[str]:
        return ParseManager.parse_text(self.morph_, self.stopwords_, text)
