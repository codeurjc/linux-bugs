import pandas as pd
import json

class CommitCollection():
    """Class for storing current commits"""
    
    def __init__(self, filename):
        self.commits_list = []
        self.commit_map = {}
        with open(filename) as fd:
            for c in json.load(fd):
                commit = {
                    'hash': c['data']['commit'], 
                    'reviewed': False, 
                    'message': c['data']['message']
                }
                reduced_commit = {
                    'hash': c['data']['commit'][:10], 
                    'reviewed': False,
                }
                self.commits_list.append(reduced_commit)
                self.commit_map[commit['hash'][:10]] = commit
    
    def asDataFrame(self):
        return pd.DataFrame(self.commits_list)

    def getCommit(self, hash):
        return self.commit_map[hash[:10]]
    
    def updateCommitState(self, hash, state):
        self.commit_map[hash[:10]]['reviewed'] = state
        for c in self.commits_list:
            if c['hash'] == hash[:10]:
                c['reviewed'] = state
                
    def setReviewed(self, reviews):
        for c in self.commits_list:
            full_commit = self.commit_map[c['hash']]
            if reviews.get(full_commit['hash']) is not None:
                c['reviewed'] = True
                self.commit_map[c['hash']]['reviewed'] = True