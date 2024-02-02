import pandas as pd

review_cols = [
    'hash', 
    "reviewer", 
    "is_bug_fixing_commit",
    "is_obvious_bug",
    "is_safety_related",
    "type_of_safety_related",
    "confidence",
    "understand",
    "commitcomment",
    "comment",
]

class ReviewsDF():
    """Class for storing reviews of annotations (as a dataframe)"""

    def __init__(self, filename):
        self.filename = filename
        self.reviewer = ""
        try:
            self.df = pd.read_csv(filename)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=review_cols)

    def update(self, data):
        self.reviewer = data['reviewer']
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
        review = self.get(hash)
        if review is None:
            reviewer=self.reviewer
            is_bug_fixing_commit= None
            is_obvious_bug= None
            is_safety_related= None
            type_of_safety_related= None
            confidence = None
            understand = None
            commitcomment = ""
            comment= ""
        else:
            reviewer = review['reviewer']
            is_bug_fixing_commit = review['is_bug_fixing_commit']
            is_obvious_bug = review['is_obvious_bug']
            is_safety_related = review['is_safety_related']
            type_of_safety_related = review['type_of_safety_related']
            confidence = review['confidence']
            understand = review['understand']
            commitcomment = review['commitcomment']
            comment = review['comment']
        return reviewer, is_bug_fixing_commit, is_obvious_bug, is_safety_related, type_of_safety_related, confidence, \
            understand, commitcomment, comment
            

    def save(self):
        self.df.to_csv(self.filename, index=False)