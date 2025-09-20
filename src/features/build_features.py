import logging
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from typing import Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_keywords(documents: pd.Series, ngram_range: Tuple[int, int] = (1, 3)) -> pd.DataFrame:
    logging.info(f"Extracting keywords with n-gram range {ngram_range}...")
    vectorizer = CountVectorizer(stop_words='english', ngram_range=ngram_range)
    # Ensure text is unicode and handle potential NaN values
    clean_documents = documents.fillna('').astype('U')
    X = vectorizer.fit_transform(clean_documents)
    term_freq_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    logging.info(f"Extracted {term_freq_df.shape[1]} unique keywords.")
    return term_freq_df

def calculate_dov_dod(term_freq_df: pd.DataFrame) -> pd.DataFrame:
    if term_freq_df.empty:
        return pd.DataFrame(columns=['TF', 'DF', 'DoV', 'DoD'])

    N = len(term_freq_df)
    tf = term_freq_df.sum(axis=0)
    df = (term_freq_df > 0).sum(axis=0)
    signals_df = pd.DataFrame({'TF': tf, 'DF': df})

    max_tf = signals_df['TF'].max()
    signals_df['DoV'] = signals_df['TF'] / max_tf if max_tf > 0 else 0
    signals_df['DoD'] = signals_df['DF'] / N if N > 0 else 0

    logging.info(f"Calculated DoV and DoD for {len(signals_df)} keywords.")
    return signals_df.sort_values(by='TF', ascending=False)