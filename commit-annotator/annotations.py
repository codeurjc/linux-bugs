import pandas as pd

class Annotations():
    """Class for storing annotations (as a dataframe)"""

    class AnnotatorError (RuntimeError):
        "The annotator in some row doesn't fir self.annotator"

    def __init__(self, annotator=None):
        self.annotator = annotator
        self.fields = ['hash', 'annotator',
                       'understand', 'purpose', 'bfc', 'bpc', 'prc', 'nfc', 'specification',
                       'asc', 'obvious', 'safety', 'timing', 'memory', 'info', 'safety_exp', 'time']
        self.fields_defaults = ['', self.annotator, None, "", None, None, None, None, None,
                                None, None, None, None, None, None, "", 0]
        if annotator is None:
            self.filename = None
            self.df = pd.DataFrame(columns=self.fields)
        else:
            self.filename = f"annotations_{annotator}.csv"
            try:
                self.df = pd.read_csv(self.filename)
                annotators = self.df['annotator'].to_numpy()
                if not (self.annotator == annotators).all():
                    raise self.AnnotatorError
            except FileNotFoundError:
                self.df = pd.DataFrame(columns=self.fields)

    def update(self, data):
        self.annotator = data['annotator']
        if any(self.df['hash'] == data['hash']):
            self.df.loc[self.df['hash'] == data['hash'], data.keys()] = data.values()
        else:
            self.df.loc[len(self.df)] = data

    def get(self, hash):
        result_df = self.df[self.df['hash'] == hash]
        if len(result_df) == 0:
            results = None
        else:
            results = result_df.iloc[0].to_dict()
        return results

    def get_values(self, hash):
        annotation = self.get(hash)
        if annotation is None:
            values = self.fields_defaults
        else:
            values = [annotation[key] for key in self.fields]
        return values

    def save(self):
        self.df.to_csv(self.filename, index=False)