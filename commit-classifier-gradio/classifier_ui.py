import pandas as pd
import gradio as gr
import json

URL = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?h=v6.7&id="

# Load 1000 random commits

with open('../linux-commits-2023-11-12_random-filtered.json') as fd:
    commits_json = json.load(fd)
    
commits_df = pd.DataFrame([ {
    'hash': c['data']['commit'], 
    'reviewed': False, 
    'message': c['data']['message'], 
    'full_hash': c['data']['commit']
} for c in commits_json])

# Load definitions
with open('definitions.md') as fd:
    definitions = fd.read()
    
review_cols = ['hash', "reviewer", "is_bug_fixing_commit","is_obvious_bug","is_safety_related","type_of_safety_related","comment"]
    
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
            comment= ""
        else:
            reviewer = review['reviewer']
            is_bug_fixing_commit = review['is_bug_fixing_commit']
            is_obvious_bug = review['is_obvious_bug']
            is_safety_related = review['is_safety_related']
            type_of_safety_related = review['type_of_safety_related']
            comment = review['comment']
        return reviewer, is_bug_fixing_commit, is_obvious_bug, is_safety_related, type_of_safety_related, comment

    def save(self):
        self.df.to_csv(self.filename, index=False)

review_filename = 'reviews.csv'
reviews = ReviewsDF(review_filename)

with gr.Blocks() as demo:
    with gr.Row():
        
        # LIST OF COMMITS
        with gr.Column(scale=1):
            bfcs_df = gr.Dataframe(value=commits_df)#[['hash']])
            
        # COMMIT INFO
        with gr.Column(scale=4):
            current_commit = gr.Textbox(label="Selected commit", interactive=False)
            see_commit_link = gr.Markdown()
            current_commit_message = gr.Code()
            
            with gr.Row():
                previous_btn =  gr.Button("Previous", scale=1)
                next_btn = gr.Button("Next", scale=1)
            
            with gr.Accordion("See definitions", open=False):
                gr.Markdown(definitions)
            
        # FORM
        with gr.Column(scale=3):
            
            reviewer_txt = gr.Textbox(label="Reviewer name")
            
            is_bfc_dd = gr.Dropdown(label="Is a Bug-Fixing Commit (BFC)",
                                  choices=[("True", True), ("False", False)],
                                  interactive=True)

            is_obvious_dd = gr.Dropdown(label="Is a BFC of an obvious bug",
                                  choices=[("True", "True"), ("False","False"), ("I don't know","I don't know")],
                                  interactive=True)

            is_safety_dd = gr.Dropdown(label="Is a BFC of a Safety-Related bug",
                                  choices=[("True", "True"), ("False","False"), ("I don't know","I don't know")],
                                  interactive=True)
            
            type_of_safety_related_dd = gr.Dropdown(label="Which type of Safety-Related commit",
                                  choices=[("Timing and execution", "True"), 
                                           ("Memory","Memory"), 
                                           ("Exchange of Information","Exchange of Information"), 
                                           ("I don't know","I don't know")],
                                  interactive=True)
            
            comment_txt = gr.Textbox(label="Comment by reviewer",
                           lines=5, interactive=True)
            
            save_btn = gr.Button("Save review", interactive=True,variant="primary")

        # EVENT FUNCTIONS
        
        # NEXT COMMIT
        
        updated_elements_on_commit_change = [
            current_commit, 
            see_commit_link, 
            current_commit_message, 
            reviewer_txt, 
            is_bfc_dd, 
            is_obvious_dd, 
            is_safety_dd, 
            type_of_safety_related_dd,
            comment_txt
        ]
        
        def change_commit(commit):
            hash = commit['hash']
            link = f"[Link to commit]({URL}{hash})"
            reviewer, is_bug_fixing_commit, is_obvious_bug, is_safety_related, type_of_safety_related, comment = reviews.get_values(hash)
            # On change commit, load review -> .get_values(hash)
            return hash,  gr.update(value=link), gr.update(value=commit['message']), gr.update(value=reviewer), gr.update(value=is_bug_fixing_commit), gr.update(value=is_obvious_bug), gr.update(value=is_safety_related), gr.update(value=type_of_safety_related), gr.update(value=comment)
        
        # ON SELECT COMMIT
        @bfcs_df.select(inputs=[bfcs_df], outputs=updated_elements_on_commit_change)
        def select_commit(event: gr.SelectData, bfcs):
            return change_commit(bfcs.iloc[event.index[0]])
        
        # ON NEXT COMMIT
        @next_btn.click(inputs=[bfcs_df, current_commit], outputs=updated_elements_on_commit_change)
        def next_commit(bfcs, current_commit_hash):
            index = bfcs[bfcs["hash"]==current_commit_hash].index.values[0]
            return change_commit(bfcs.iloc[index+1])
        
        # ON PREVIOUS COMMIT
        @previous_btn.click(inputs=[bfcs_df, current_commit], outputs=updated_elements_on_commit_change)
        def previous_commit(bfcs, current_commit_hash):
            index = bfcs[bfcs["hash"]==current_commit_hash].index.values[0]
            return change_commit(bfcs.iloc[index-1])
        
        # SAVE REVIEW
        @save_btn.click(inputs=[
            current_commit, reviewer_txt, is_bfc_dd, is_obvious_dd, is_safety_dd, type_of_safety_related_dd,comment_txt
        ],outputs=[save_btn])
        def update_review(hash, reviewer, is_bfc, is_obvious, is_safety, type_of_safety_related, comment):
            errors = []
            if comment == "": errors.append("Comment is empty")
            if len(errors) > 0:
                raise gr.Error("\n".join(errors))
            else:
                # Save review
                reviews.update({
                    'hash': hash,
                    'reviewer': reviewer,
                    'is_bug_fixing_commit': is_bfc,
                    'is_obvious_bug:': is_obvious,
                    'is_safety_related': is_safety,
                    'type_of_safety_related': is_safety,
                    'comment': comment
                })
                reviews.save()
                gr.Info("Classification for commit %s saved!"%hash[:10])
                return gr.update(interactive=False)
            
        #bfcs_df.select(select_commit, inputs=[bfcs_df], outputs=[current_commit, current_commit_message])
            
demo.launch(server_name='localhost')