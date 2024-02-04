import gradio as gr
import pandas as pd
from CommitCollection import CommitCollection
from annotations import Annotations

URL = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?h=v6.7&id="

# Load annotations (if file exists)
annots = Annotations()

# Load 1000 random commits
commits = CommitCollection('../linux-commits-2023-11-12_random-filtered.json')
commits_df = commits.asDataFrame()

# Apply styles to hash column
def color_commits(row):
    style=pd.Series()
    if row['hash'] in annots.df['hash'].values:
        style['hash'] = 'color: green'
        style['id'] = 'color: green'
    else:
        style['hash'] = 'color: red'
        style['id'] = 'color: red'
    return style

commits_s = commits_df[['id', 'hash']].style.apply(color_commits, axis=1)

# Load definitions
with open('definitions.md') as fd:
    definitions = fd.read()

with gr.Blocks() as demo:
    with gr.Row():
        title_md = gr.Markdown(value="# Annotation of commits")
        annotator_txt = gr.Textbox(label="Annotator name")

    with gr.Row():
        
        # LIST OF COMMITS
        with gr.Column(scale=1):
            bfcs_df = gr.Dataframe(value=commits_s,
                                   height=600, datatype=['number', 'str'],
                                   interactive=False
            )
            
            # Filtering on those what have been annotated
            filter_dd = gr.Dropdown(label="Show", choices=["All", "Annotated", "Not Annotated"], value="All")
            
            @filter_dd.change(inputs=[filter_dd], outputs=[bfcs_df])
            def filter_commits(choice):
                if choice == "All":
                    df = commits.asDataFrame()
                elif choice == "Annotated":
                    df = commits.asDataFrame()[commits.asDataFrame()['annotated'] == True]
                elif choice == "Not Annotated":
                    df = commits.asDataFrame()[commits.asDataFrame()['annotated'] == False]
                return df
            
        # Commit info
        with gr.Column(scale=6):
            current_commit = gr.Textbox(label="Selected commit", interactive=False)
            see_commit_link = gr.Markdown()
            current_commit_message = gr.Code()
            
            with gr.Row():
                previous_btn =  gr.Button("Previous", scale=1, interactive=False)
                next_btn = gr.Button("Next", scale=1, interactive=False)
            
            with gr.Accordion("See definitions", open=False):
                gr.Markdown(definitions)
            
        # Annotation form
        with gr.Column(scale=4) as annotation_col:
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
            confidence_rb = gr.Radio(choices=[0, 1, 2, 3, 4],
                                     label='Confidence about the classification, from low (0) to high (4)',
                                     interactive=True)
            
            # Radio buttons for understanding level
            understand_rb = gr.Radio(choices=[0, 1, 2, 3, 4],
                                     label='I understood the commit purpose, from low (0) to high (4)',
                                     interactive=True)
            
            commitcomment_txt = gr.Textbox(label="Commit purpose comment",
                                     lines=2, interactive=True)
            
            comment_txt = gr.Textbox(label="Classification reason",
                           lines=2, interactive=True)
            
            save_btn = gr.Button("Save annotation",
                                 interactive=False,
                                 variant="primary")

        # Event functions
        
        # Next commit
        
        updated_elements_on_commit_change = [
            current_commit, 
            see_commit_link, 
            current_commit_message, 
            annotator_txt,
            is_bfc_dd, 
            is_obvious_dd, 
            is_safety_dd, 
            type_of_safety_related_dd,
            confidence_rb,
            understand_rb,
            commitcomment_txt,
            comment_txt
        ]
        
        def change_commit(hash):
            link = f"[Link to commit]({URL}{hash})"
            (annotator, is_bug_fixing_commit, is_obvious_bug, is_safety_related,
                type_of_safety_related, confidence,
                understand, commitcomment, comment) = annots.get_values(hash)
            message = commits.getCommit(hash)['message']
            return (hash,  gr.update(value=link),
                           gr.update(value=message),
                           gr.update(value=annotator),
                           gr.update(value=is_bug_fixing_commit), 
                           gr.update(value=is_obvious_bug), 
                           gr.update(value=is_safety_related), 
                           gr.update(value=type_of_safety_related),
                           gr.update(value=confidence),
                           gr.update(value=understand),
                           gr.update(value=commitcomment),
                           gr.update(value=comment)
            )

        @annotator_txt.submit(inputs=[annotator_txt, current_commit],
                              outputs=[annotator_txt, bfcs_df, save_btn])
        def set_annotator(annotator, current):
            global annots, commits_s
            annots = Annotations(annotator)
            commits_s = commits_df[['id', 'hash']].style.apply(color_commits, axis=1)
            if len(current) > 0:
                save_inter = True
            else:
                save_inter = False
            return (gr.update(interactive=False), gr.update(value=commits_s),
                    gr.update(interactive=save_inter))

        # ON SELECT COMMIT
        @bfcs_df.select(inputs=[bfcs_df, annotator_txt],
                        outputs=updated_elements_on_commit_change + [save_btn, previous_btn, next_btn])
        def select_commit(event: gr.SelectData, bfcs, annotator):
            hash = bfcs.iloc[event.index[0]]['hash']
            if len(annotator) > 0:
                save_inter = True
            else:
                save_inter = False
            return change_commit(hash) \
                + (gr.update(interactive=save_inter), gr.update(interactive=True), gr.update(interactive=True))
        
        # ON NEXT COMMIT
        @next_btn.click(inputs=[bfcs_df, current_commit], outputs=updated_elements_on_commit_change)
        def next_commit(bfcs, current_commit_hash):
            next_commit_hash = bfcs.iloc[bfcs[bfcs["hash"]==current_commit_hash[:10]].index.values[0]+1]['hash']
            if next_commit_hash == "": 
                next_commit_hash = current_commit_hash
                gr.Info("You reach last commit")
            return change_commit(next_commit_hash)
        
        # ON PREVIOUS COMMIT
        @previous_btn.click(inputs=[bfcs_df, current_commit], outputs=updated_elements_on_commit_change)
        def previous_commit(bfcs, current_commit_hash):
            prev_commit_hash = bfcs.iloc[bfcs[bfcs["hash"]==current_commit_hash[:10]].index.values[0]-1]['hash']
            if prev_commit_hash == "": 
                prev_commit_hash = current_commit_hash
                gr.Info("No previous commit")
            # commit = commits.getCommit(prev_commit_hash)
            return change_commit(prev_commit_hash)
        
        # Save annotation
        @save_btn.click(inputs=[
            current_commit, annotator_txt, is_bfc_dd, is_obvious_dd, is_safety_dd, type_of_safety_related_dd, \
                confidence_rb, understand_rb, commitcomment_txt, comment_txt],outputs=[save_btn, bfcs_df])
        def update_annotation(hash, annotator, is_bfc, is_obvious, is_safety, type_of_safety_related, confidence, \
                          understand, commitcomment, comment):
            if hash == "": gr.Info("Select a commit")
            if is_bfc == []: gr.Info("Select if it is a BFC")
            if annotator == "": gr.Info("The annotator field cannot be empty")
            if comment == "": gr.Info("The classification reason cannot be empty")
            if commitcomment == "": gr.Info("The commit purpose comment cannot be empty")
            if confidence is None:
                gr.Info("Please select a confidence level")
            if understand is None:
                gr.Info("Please select a understood level")

            if hash != "" and is_bfc != [] and annotator != "" and comment != "" and confidence is not None \
                    and understand is not None and commitcomment != "":
                # Save annotation
                annots.update({
                    'hash': hash,
                    'annotator': annotator,
                    'bfc': is_bfc,
                    'obvious': is_obvious,
                    'safety': is_safety,
                    'safety_type': type_of_safety_related,
                    'confidence': confidence,
                    'understand': understand,
                    'commitcomment': commitcomment,
                    'comment': comment
                })
                annots.save()
                commits.updateCommitState(hash, True)
                gr.Info("Classification for commit %s saved!"%hash[:10])
#            return gr.update(interactive=True), gr.update(value=commits.asDataFrame())
            global commits_df
            commits_df = commits.asDataFrame()
            commits_s = commits_df[['id', 'hash']].style.apply(color_commits, axis=1)
            return gr.update(interactive=True), gr.update(value=commits_s)
            
demo.launch(server_name='localhost')