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
with open('definitions.txt') as fd:
    definitions = fd.read()
    
# class ReviewsDF():
#     """Class for storing reviews of annotations (as a dataframe)"""

#     def __init__(self, filename):
#         try:
#             self.df = pd.read_csv(filename)
#         except FileNotFoundError:
#             self.df = pd.DataFrame(columns=review_cols)

#     def update(self, data):
#         if any(self.df['hash'] == data['hash']):
#             self.df.loc[self.df['hash'] == data['hash'], data.keys()] = data.values()
#         else:
#             self.df.loc[len(self.df)] = data

#     def get(self, hash):
#         result_df = self.df[self.df['hash'] == hash]
#         if len(result_df) == 0:
#             results = None
#         else:
#             results = result_df.iloc[0].to_dict()
#         return results

#     def get_values(self, hash):
#         review = self.get(hash)
#         if review is None:
#             text = ""
#             bfc = None
#             understanding = None
#         else:
#             text = review['comment']
#             bfc = review['bfc']
#             understanding = review['understanding']
#         return text, bfc, understanding

#     def save(self, filename):
#         self.df.to_csv(filename, index=False)

# review_cols = ['hash', 'reviewer', 'bfc', 'comment', 'understanding']
# review_filename = 'reviews.csv'

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
        
        def change_commit(commit):
            hash = commit['hash']
            see_commit_link = f"[Link to commit]({URL}{hash})"
            return hash,  gr.update(value=see_commit_link), gr.update(value=commit['message'])
        
        # ON SELECT COMMIT
        @bfcs_df.select(inputs=[bfcs_df], outputs=[current_commit, see_commit_link, current_commit_message])
        def select_commit(event: gr.SelectData, bfcs):
            return change_commit(bfcs.iloc[event.index[0]])
        
        # ON NEXT COMMIT
        @next_btn.click(inputs=[bfcs_df, current_commit], outputs=[current_commit, see_commit_link, current_commit_message])
        def next_commit(bfcs, current_commit_hash):
            index = bfcs[bfcs["hash"]==current_commit_hash].index.values[0]
            return change_commit(bfcs.iloc[index+1])
        
        # ON PREVIOUS COMMIT
        @previous_btn.click(inputs=[bfcs_df, current_commit], outputs=[current_commit, see_commit_link, current_commit_message])
        def previous_commit(bfcs, current_commit_hash):
            index = bfcs[bfcs["hash"]==current_commit_hash].index.values[0]
            return change_commit(bfcs.iloc[index-1])
        
        # SAVE REVIEW
        @save_btn.click(inputs=[
            current_commit, reviewer_txt, is_bfc_dd, is_obvious_dd, is_safety_dd, type_of_safety_related_dd,comment_txt
        ],outputs=[])
        def update_review(hash, reviewer, is_bfc, is_obvious, is_safety, type_of_safety_related, comment):
            errors = []
            if comment == "": errors.append("Comment is empty")
            if len(errors) > 0:
                raise gr.Error("\n".join(errors))
            else:
                gr.Info("Classification for commit %s saved!"%hash[:10])
            
        #bfcs_df.select(select_commit, inputs=[bfcs_df], outputs=[current_commit, current_commit_message])
            
demo.launch(server_name='localhost')