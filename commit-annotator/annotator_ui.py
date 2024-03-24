import gradio as gr
import pandas as pd
from CommitCollection import CommitCollection
from annotations import Annotations
import argparse
import urllib.parse
import time

URL = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?h=v6.7&id="
URL_LORE = "https://lore.kernel.org/all/?q="
def open_link_js(url):
    # If arg is a url itself, its not necessary to pass the and url parameter
    return "(arg) => { window.open('"+url+"' + arg, '_blank'); return arg; }"

# Options sure - not sure
sure_not5 = [("Yes, I'm sure", 4),
             ("Likely, but I'm not sure", 3),
             ("I don't know", 2),
             ("I think it's not, but not sure", 1),
             ("No, I'm sure", 0),
             ("Undecided", None)]
sure_not3 = [("Yes, I'm sure", 4),
             ("I don't know", 2),
             ("No, I'm sure", 0),
             ("Undecided", None)]

# Time measurements
start_time = time.time()

# Current active commit
current_commit = None

# Load annotations (if file exists)
annots = Annotations()

# Load 1000 random commits
commits = CommitCollection('../linux-commits-2023-11-12_random-filtered-1.json')
commits_df = commits.asDataFrame()

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-rb', '--radio', action='store_true', help='Use radio buttons instead of dropdowns')
args = parser.parse_args()

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

with (gr.Blocks() as demo):
    with gr.Row():
        title_md = gr.Markdown(value=("# Annotation of commits\n"
                                      "Start by filling in the annotator name"
                                      " (for example, 'jesus'),"
                                      " then select a commit and start annotating."))
        annotator_txt = gr.Textbox(label="Annotator name (fill with your name and press Enter to create a new result's file or load and existing one)",)

    with gr.Row():
        
        # LIST OF COMMITS
        with gr.Column(scale=1):
            # Filter for commits
            filter_dd = gr.Radio(label="Show",
                                    choices=["All", "Annotated", "Not Annotated"], value="All")
            # Commits
            bfcs_df = gr.Dataframe(value=commits_s,
                                   height=600, datatype=['number', 'str'],
                                   interactive=False
            )

            @filter_dd.change(inputs=[filter_dd], outputs=[bfcs_df])
            def filter_commits(choice):
                if choice == "All":
                    df = commits.asDataFrame()
                elif choice == "Annotated":
                    df = commits.asDataFrame()[commits.asDataFrame()['annotated'] == True]
                elif choice == "Not Annotated":
                    df = commits.asDataFrame()[commits.asDataFrame()['annotated'] == False]
                commits_s = df[['id', 'hash']].style.apply(color_commits, axis=1)
                return commits_s
            
        # Commit info
        with gr.Column(scale=6):
            hash_txt = gr.Textbox(label="Selected commit", interactive=False)
            see_commit_link_btn = gr.Button("See commit")
            see_commit_clicked_cb = gr.Checkbox(label="I clicked on the commit link", visible=False)
            search_commit_lore_btn = gr.Button("Search commit in lore")
            lore_clicked_cb = gr.Checkbox(label="I looked for the commit in lore")
            lore_found_cb = gr.Checkbox(label="I found the commit in lore")
            is_part_patchset_dd = gr.Checkbox(label="The commit is in a PATCHSET")
            message_txt = gr.HTML()
            # The following text is just to store the commit message
            link_to_lore_no_visible = gr.Textbox(label="", interactive=False, visible=False)

            with gr.Row():
                previous_btn =  gr.Button("Previous", scale=1, interactive=False)
                next_btn = gr.Button("Next", scale=1, interactive=False)
            
            with gr.Accordion("See definitions", open=False):
                gr.Markdown(definitions)
            
        # Annotation form
        with gr.Column(scale=4) as annotation_col:
            # Radio buttons for understanding level
            
            # Radio buttons for understanding level
            if args.radio:
                understand_dd = gr.Radio(choices=[
                    ("I understand it completely", 4),
                    ("Mostly clear to me", 3),
                    ("Partial understanding", 2),
                    ("Struggling with key aspects", 1),
                    ("No understanding at all", 0),
                    ("Undecided", None)],
                    label='How well do you understand the purpose of the commit?',
                    interactive=False)
            else:
            # Dropdown for understanding level
                understand_dd = gr.Dropdown(choices=[
                    ("I understand it completely", 4),
                    ("Mostly clear to me", 3),
                    ("Partial understanding", 2),
                    ("Struggling with key aspects", 1),
                    ("No understanding at all", 0),
                    ("Undecided", None)],
                    label='How well do you understand the purpose of the commit?',
                    interactive=False)

            purpose_txt = gr.Textbox(label="Describe the purpose of the commit:",
                                     lines=3, interactive=False)


            # Radio buttons for understanding level
            if args.radio:
                bfc_dd = gr.Radio(label="Is it a Bug-Fixing Commit (BFC)?",
                                      choices=sure_not5,
                                      interactive=False)
    
                bpc_dd = gr.Radio(label="Is it a Bug-Preventing Commit (BPC)?",
                                        choices=sure_not5,
                                        interactive=False)

                prc_dd = gr.Radio(label="Is it a Perfective Commit (PRC)?",
                                  choices=sure_not5,
                                  interactive=False)

                nfc_dd = gr.Radio(label="Is it a New Feature Commit (NFC)?",
                                  choices=sure_not5,
                                  interactive=False)

                specification_dd = gr.Radio(label="Is it related to a specification change?",
                                  choices=sure_not3,
                                  interactive=False)
    
                asc_dd = gr.Radio(label="Is it an Auto-Suggested Commit (ASC)?",
                                        choices=sure_not3,
                                        interactive=False)
    
                obvious_dd = gr.Radio(label="Is the bug obvious?",
                                      choices=sure_not3,
                                      interactive=False)
    
                safety_dd = gr.Radio(label="Is the bug Safety-Related?",
                                      choices=sure_not5,
                                      interactive=False)
                
                timing_dd = gr.Radio(label="Is it a Timing and Execution bug?",
                                        choices=sure_not3,
                                        interactive=False)
    
                memory_dd = gr.Radio(label="Is it a Memory bug?",
                                        choices=sure_not3,
                                        interactive=False)
    
                info_dd = gr.Radio(label="Is it a Exchange of Information bug?",
                                        choices=sure_not3,
                                        interactive=False)
            else:
                bfc_dd = gr.Dropdown(label="Is it a Bug-Fixing Commit (BFC)?",
                                     choices=sure_not5,
                                     interactive=False)
                
                bpc_dd = gr.Dropdown(label="Is it a Bug-Preventing Commit (BPC)?",
                                     choices=sure_not5,
                                     interactive=False)

                prc_dd = gr.Dropdown(label="Is it a Perfective Commit (PRC)?",
                                  choices=sure_not5,
                                  interactive=False)

                nfc_dd = gr.Dropdown(label="Is it a New Feature Commit (NFC)?",
                                  choices=sure_not5,
                                  interactive=False)

                specification_dd = gr.Dropdown(label="Is it a Commit related to a specification change?",
                                            choices=sure_not3,
                                            interactive=False)
                
                asc_dd = gr.Dropdown(label="Is it an Auto-Suggested Commit (ASC)?",
                                     choices=sure_not3,
                                     interactive=False)
                
                obvious_dd = gr.Dropdown(label="Is the bug obvious?",
                                         choices=sure_not3,
                                         interactive=False,
                                         visible=False)
                
                safety_dd = gr.Dropdown(label="Is the bug Safety-Related?",
                                        choices=sure_not5,
                                        interactive=False,
                                        visible=False)
                
                timing_dd = gr.Dropdown(label="Is it a Timing and Execution bug?",
                                        choices=sure_not3,
                                        interactive=False,
                                        visible=False)
                
                memory_dd = gr.Dropdown(label="Is it a Memory bug?",
                                        choices=sure_not3,
                                        interactive=False,
                                        visible=False)
                
                info_dd = gr.Dropdown(label="Is it a Exchange of Information bug?",
                                      choices=sure_not3,
                                      interactive=False,
                                      visible=False)

            safety_txt = gr.Textbox(label="Reason for the classification (safety-related and kind)",
                           lines=2, interactive=True, visible=False)
            
            save_btn = gr.Button("Save annotation",
                                 interactive=True,
                                 variant="primary")

        # Lists of elements
        data_els = [hash_txt, see_commit_link_btn, search_commit_lore_btn, message_txt, link_to_lore_no_visible]
        annotation_els = [annotator_txt,
                          understand_dd, purpose_txt,
                          bfc_dd, bpc_dd, prc_dd, nfc_dd, specification_dd, asc_dd, obvious_dd,
                          safety_dd, timing_dd, memory_dd, info_dd, safety_txt,
                          see_commit_clicked_cb, lore_clicked_cb, lore_found_cb,
                          is_part_patchset_dd
                          ]
        updated_els_on_commit_change = data_els + annotation_els

        # Event functions
        def change_commit(hash):
            global start_time, current_commit
            start_time = time.time()
            """Return all elements that should be updated when a new commit is loaded"""
            message_raw = commits.getCommit(hash)['message_raw']
            first_line = message_raw.split('\n')[0]
            link_to_commit = f"{URL}{hash}"
            link_to_lore = f"{URL_LORE}{urllib.parse.quote(first_line)}"
            current_commit = commits.getCommit(hash)
            message = current_commit['message']
            updated_vals = annots.get_values(hash)[1:]
            updated_els = [
                # For hash
                gr.update(value=hash),
                # For link to commit button
                gr.update(),
                # For link to lore button
                gr.update(),
                # For commit message
                gr.update(value=message),
                # For link to lore (aux)
                gr.update(value=link_to_lore)
            # For annotation values
            ] + [gr.update(value=item) for item in updated_vals]
            return tuple(updated_els)

        # When see commit button is clicked
        @see_commit_link_btn.click(inputs=[hash_txt], outputs=[see_commit_clicked_cb], js=open_link_js(URL))
        def see_commit(_):
            return gr.update(value=True)

        # When see commit in lore button is clicked
        @search_commit_lore_btn.click(inputs=[link_to_lore_no_visible], outputs=[lore_clicked_cb], js=open_link_js(''))
        def see_commit_lore(_):
            return gr.update(value=True)

        # DROPDOWN'S CHANGE LISTENER

        @bfc_dd.change(inputs=[bfc_dd], outputs=[obvious_dd, safety_dd])
        def change_bfc(value):
            if value != None and value > 0:
                return gr.update(visible=True), gr.update(visible=True)
            else:
                return gr.update(visible=False), gr.update(visible=False)

        @safety_dd.change(inputs=[safety_dd], outputs=[timing_dd, memory_dd, info_dd, safety_txt])
        def change_safety(value):
            if value != None and value > 0:
                return gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
            else:
                return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

        # SET ANNOTATOR LISTENER

        @annotator_txt.submit(inputs=[annotator_txt, hash_txt],
                              outputs=[annotator_txt, understand_dd, purpose_txt,
                          bfc_dd, bpc_dd, prc_dd, nfc_dd, specification_dd, asc_dd, obvious_dd,
                          safety_dd, timing_dd, memory_dd, info_dd, bfcs_df])
        def set_annotator(annotator, current):
            global annots, commits_s
            try:
                annots = Annotations(annotator)
                commits_s = commits_df[['id', 'hash']].style.apply(color_commits, axis=1)
                return (gr.update(interactive=False), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(value=commits_s))
            except Annotations.AnnotatorError:
                gr.Info(f"Error loading annotations: some row has a different annotator than {annotator}")
                return (gr.update(interactive=True), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update())

        # When a commit is selected
        @bfcs_df.select(inputs=[bfcs_df, annotator_txt],
                        outputs=updated_els_on_commit_change + [save_btn, previous_btn, next_btn])
        def select_commit(event: gr.SelectData, bfcs, annotator):
            hash = bfcs.iloc[event.index[0]]['hash']
            return change_commit(hash) \
                + (gr.update(interactive=True), gr.update(interactive=True),
                   gr.update(interactive=True))
        
        # When next commit
        @next_btn.click(inputs=[bfcs_df, hash_txt],
                        outputs=updated_els_on_commit_change)
        def next_commit(bfcs, current_commit_hash):
            next_commit_hash = bfcs.iloc[bfcs[bfcs["hash"]==current_commit_hash[:10]].index.values[0]+1]['hash']
            if next_commit_hash == "": 
                next_commit_hash = current_commit_hash
                gr.Info("Already at last commit")
            return change_commit(next_commit_hash)
        
        # When previous commit
        @previous_btn.click(inputs=[bfcs_df, hash_txt],
                            outputs=updated_els_on_commit_change)
        def previous_commit(bfcs, current_commit_hash):
            prev_commit_hash = bfcs.iloc[bfcs[bfcs["hash"]==current_commit_hash[:10]].index.values[0]-1]['hash']
            if prev_commit_hash == "": 
                prev_commit_hash = current_commit_hash
                gr.Info("Already at first commit")
            return change_commit(prev_commit_hash)
        
        # Save annotation
        @save_btn.click(inputs=[hash_txt] + annotation_els,
                        outputs=[save_btn, bfcs_df])
        def update_annotation(hash, annotator, understand, purpose, bfc, bpc, prc, nfc, specification,
                              asc, obvious, safety, timing, memory, info, safety_exp,
                              see_commit_clicked, lore_clicked, lore_found,
                              is_part_patchset):
            global current_commit
            message = ""
            if annotator == "": message += "Fill in an annotator. "
            if hash == "": message += "Select a commit. "
            if understand is None: message += "Explain how do you understand the bug. "
            if purpose == "": message += "Explain the purpose of the commit. "
            if bfc == None: message += "Select if it is a Bug Fixing Commit. "
            if bpc == None: message += "Select if it is a Bug Preventing Commit. "
            if prc == None: message += "Select if it is a Perfective Commit. "
            if nfc == None: message += "Select if it is a New Feature Commit. "
            if specification == None: message += "Select if it is a Commit related to some specification change. "
            if asc == None: message += "Select if it is a Auto-Suggested Commit. "
            # if obvious == None: message += "Select if it is an obvious bug. "

            if message == "":
                # Save annotation
                # Save time
                end_time = time.time()
                annots.update({
                    'hash': hash,
                    'annotator': annotator,
                    'understand': understand,
                    'purpose': purpose,
                    'bfc': bfc,
                    'bpc': bpc,
                    'prc': prc,
                    'nfc': nfc,
                    'specification': specification,
                    'asc': asc,
                    'obvious': obvious,
                    'safety': safety,
                    'timing': timing,
                    'memory': memory,
                    'info': info,
                    'safety_exp': safety_exp,
                    'time': end_time - start_time,
                    'see_commit_clicked': see_commit_clicked,
                    'lore_clicked': lore_clicked,
                    'lore_found': lore_found,
                    'is_merge_commit': current_commit['is_merge'],
                    'is_part_patchset': is_part_patchset,
                })
                
                
                annots.save()
                commits.updateCommitState(hash, True)
                gr.Info("Classification for commit %s saved!" % hash[:10])
            else:
                gr.Info("Not saved!: " + message)
            global commits_df
            commits_df = commits.asDataFrame()
            commits_s = commits_df[['id', 'hash']].style.apply(color_commits, axis=1)
            return gr.update(interactive=True), gr.update(value=commits_s)

demo.launch(server_name='localhost')
