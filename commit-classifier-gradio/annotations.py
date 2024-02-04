import pandas as pd

annotation_cols = [
    'hash',
    'annotator',
    'bfc',
    'obvious',
    'safety',
    'safety_type',
    'confidence',
    'understand',
    'commitcomment',
    'comment',
]


class Annotations():
    """Class for storing annotations (as a dataframe)"""

    def __init__(self, annotator=None):
        self.annotator = annotator
        if annotator is None:
            self.filename = None
            self.df = pd.DataFrame(columns=annotation_cols)
        else:
            self.filename = f"annotations_{annotator}.csv"
            try:
                self.df = pd.read_csv(self.filename)
            except FileNotFoundError:
                self.df = pd.DataFrame(columns=annotation_cols)

    def update(self, data):
        print("Data:", data)
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
            annotator = self.annotator
            is_bug_fixing_commit = None
            is_obvious_bug = None
            is_safety_related = None
            type_of_safety_related = None
            confidence = None
            understand = None
            commitcomment = ""
            comment = ""
        else:
            annotator = annotation['annotator']
            is_bug_fixing_commit = annotation['is_bug_fixing_commit']
            is_obvious_bug = annotation['is_obvious_bug']
            is_safety_related = annotation['is_safety_related']
            type_of_safety_related = annotation['type_of_safety_related']
            confidence = annotation['confidence']
            understand = annotation['understand']
            commitcomment = annotation['commitcomment']
            comment = annotation['comment']
        return annotator, is_bug_fixing_commit, is_obvious_bug, is_safety_related, type_of_safety_related, confidence, \
            understand, commitcomment, comment

    def save(self):
        self.df.to_csv(self.filename, index=False)