import pandas as pd
import json
import re
import html

class CommitCollection():
    """Class for storing current commits"""
    
    def __init__(self, filename):
        """Read commits from Perceval JSON-lines dump"""
        self.commits_list = []
        self.commit_map = {}
        with open(filename) as fd:
            for c in json.load(fd):
                # Remove the "Fixes: " line from the commit message
                message = re.sub(r'^Fixes:.*\n', '', c['data']['message'], flags=re.M)
                # Make links clickable
                message = html.escape(message)
                message = re.sub(r'(https?://\S+)', r'<a href="\1">\1</a>', message)
                # message = re.sub(r'(\S+@\S+)', r'<a href="mailto:\1">\1</a>', message)
                # Replace newlines with <br>
                message = message.replace('\n', '<br>')
                # Wrap in HTML tags
                message = f'<div style="border: 2px solid var(--block-border-color); background: var(--block-background-fill); padding: 10px;"><p>{message}</p></div>'
                commit = {
                    'lhash': c['data']['commit'],
                    'hash': c['data']['commit'][:10],
                    'annotated': False,
                    'message': message
                }
                self.commits_list.append(commit)
        self.df = pd.DataFrame(self.commits_list)
        self.df['id'] = self.df.index
    
    def asDataFrame(self):
        return self.df

    def getCommit(self, hash):
        """Get a commit data, as Series, given its short hash (hash)"""
        return self.df[self.df['hash'].str[:10] == hash].iloc[0]

    def updateCommitState(self, hash, state):
        self.df.loc[self.df['hash'] == hash, 'annotated'] = state
        # for c in self.commits_list:
        #     if c['hash'] == hash[:10]:
        #         c['annotated'] = state
                
    def setAnnotated(self, annotations):
        self.df[self.df]
        for c in self.commits_list:
            full_commit = self.commit_map[c['hash']]
            if annotations.get(full_commit['hash']) is not None:
                c['annotated'] = True
                self.commit_map[c['hash']]['annotated'] = True
