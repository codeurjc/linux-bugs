import pandas as pd
import gradio as gr
from CommitCollection import CommitCollection
from ReviewsDF import ReviewsDF

URL = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?h=v6.7&id="

# Load reviews (if exists)
reviews = ReviewsDF('reviews.csv')

# Load 1000 random commits
commits = CommitCollection('../linux-commits-2023-11-12_random-filtered.json')
commits.setReviewed(reviews)
commits_df = commits.asDataFrame()

# Load definitions
with open('definitions.md') as fd:
    definitions = fd.read()

with gr.Blocks() as demo:
    with gr.Row():
        
        # LIST OF COMMITS
        with gr.Column(scale=1):
            bfcs_df = gr.Dataframe(value=commits_df, 
                                   height=600, 
                                   interactive=False
            )
            
            # Filtering on those what have been reviewed
            filter_dd = gr.Dropdown(label="Show", choices=["All", "Reviewed", "Not Reviewed"], value="All")
            
            @filter_dd.change(inputs=[filter_dd], outputs=[bfcs_df])
            def filter_commits(choice):
                if choice == "All":
                    df = commits.asDataFrame()
                elif choice == "Reviewed":
                    df = commits.asDataFrame()[commits.asDataFrame()["reviewed"] == True]
                elif choice == "Not Reviewed":
                    df = commits.asDataFrame()[commits.asDataFrame()["reviewed"] == False]
                return df
            
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
            
            is_bfc_dd = gr.Radio(label="Is a Bug-Fixing Commit (BFC)",
                                  choices=[("True", True), ("False", False)],
                                  interactive=True)

            is_obvious_dd = gr.Radio(label="Is a BFC of an obvious bug",
                                  choices=[("True", True), ("False",False), ("I don't know","I don't know")],
                                  interactive=True)

            is_safety_dd = gr.Radio(label="Is a BFC of a Safety-Related bug",
                                  choices=[("True", True), ("False",False), ("I don't know","I don't know")],
                                  interactive=True)
            
            type_of_safety_related_dd = gr.Dropdown(label="Which type of Safety-Related commit",
                                  choices=[("Timing and execution", "Timing and execution"), 
                                           ("Memory","Memory"), 
                                           ("Exchange of Information","Exchange of Information"), 
                                           ("I don't know","I don't know")],
                                  interactive=True)
            
            # Radio buttons for confidence level
            confidence_rb = gr.Radio(choices=[0, 1, 2, 3, 4], label='Confidence about the classification, \
            from low (0) to high (4)')
            
            # Radio buttons for understanding level
            understand_rb = gr.Radio(choices=[0, 1, 2, 3, 4], label='I understood the commit purpose, \
                        from low (0) to high (4)')
            
            commitcomment_txt = gr.Textbox(label="Commit purpose comment",
                                     lines=2, interactive=True)
            
            comment_txt = gr.Textbox(label="Classification reason",
                           lines=2, interactive=True)
            
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
            confidence_rb,
            understand_rb,
            commitcomment_txt,
            comment_txt
        ]
        
        def change_commit(commit):
            hash = commit['hash']
            link = f"[Link to commit]({URL}{hash})"
            reviewer, is_bug_fixing_commit, is_obvious_bug, is_safety_related, type_of_safety_related, confidence, \
                understand, commitcomment, comment = reviews.get_values(hash)
            
            return (hash,  gr.update(value=link), 
                           gr.update(value=commit['message']),
                           gr.update(value=reviewer), 
                           gr.update(value=is_bug_fixing_commit), 
                           gr.update(value=is_obvious_bug), 
                           gr.update(value=is_safety_related), 
                           gr.update(value=type_of_safety_related),
                           gr.update(value=confidence),
                           gr.update(value=understand),
                           gr.update(value=commitcomment),
                           gr.update(value=comment)
            )
            
        # ON SELECT COMMIT
        @bfcs_df.select(inputs=[bfcs_df], outputs=updated_elements_on_commit_change)
        def select_commit(event: gr.SelectData, bfcs):
            commit = commits.getCommit(bfcs.iloc[event.index[0]]['hash'])
            return change_commit(commit)
        
        # ON NEXT COMMIT
        @next_btn.click(inputs=[bfcs_df, current_commit], outputs=updated_elements_on_commit_change)
        def next_commit(bfcs, current_commit_hash):
            next_commit_hash = bfcs.iloc[bfcs[bfcs["hash"]==current_commit_hash[:10]].index.values[0]+1]['hash']
            if next_commit_hash == "": 
                next_commit_hash = current_commit_hash
                gr.Info("You reach last commit")
            commit = commits.getCommit(next_commit_hash)
            return change_commit(commit)
        
        # ON PREVIOUS COMMIT
        @previous_btn.click(inputs=[bfcs_df, current_commit], outputs=updated_elements_on_commit_change)
        def previous_commit(bfcs, current_commit_hash):
            prev_commit_hash = bfcs.iloc[bfcs[bfcs["hash"]==current_commit_hash[:10]].index.values[0]-1]['hash']
            if prev_commit_hash == "": 
                prev_commit_hash = current_commit_hash
                gr.Info("No previous commit")
            commit = commits.getCommit(prev_commit_hash)
            return change_commit(commit)
        
        # SAVE REVIEW
        @save_btn.click(inputs=[
            current_commit, reviewer_txt, is_bfc_dd, is_obvious_dd, is_safety_dd, type_of_safety_related_dd, \
                confidence_rb, understand_rb, commitcomment_txt, comment_txt],outputs=[save_btn, bfcs_df])
        def update_review(hash, reviewer, is_bfc, is_obvious, is_safety, type_of_safety_related, confidence, \
                          understand, commitcomment, comment):
            if hash == "": gr.Info("Select a commit")
            if is_bfc == []: gr.Info("Select if it is a BFC")
            if reviewer == "": gr.Info("The reviewer field cannot be empty")
            if comment == "": gr.Info("The classification reason cannot be empty")
            if commitcomment == "": gr.Info("The commit purpose comment cannot be empty")
            if confidence is None:
                gr.Info("Please select a confidence level")
            if understand is None:
                gr.Info("Please select a understood level")
                
            
            if hash != "" and is_bfc != [] and reviewer != "" and comment != "" and confidence is not None \
                    and understand is not None and commitcomment != "":
                # Save review
                reviews.update({
                    'hash': hash,
                    'reviewer': reviewer,
                    'is_bug_fixing_commit': is_bfc,
                    'is_obvious_bug': is_obvious,
                    'is_safety_related': is_safety,
                    'type_of_safety_related': type_of_safety_related,
                    'confidence': confidence,
                    'understand': understand,
                    'commitcomment': commitcomment,
                    'comment': comment
                })
                reviews.save()
                commits.updateCommitState(hash, True)
                gr.Info("Classification for commit %s saved!"%hash[:10])
            return gr.update(interactive=True), gr.update(value=commits.asDataFrame())
            
demo.launch(server_name='localhost')