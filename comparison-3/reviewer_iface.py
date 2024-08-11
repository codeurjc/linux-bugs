import pandas as pd
import numpy as np
import gradio as gr

# Reviewer file
review_filename = 'review.csv'

# Link to LORE API search
URL_LORE = "https://lore.kernel.org/all/?q="

# Fields of interest for querying results
results_fields = ['bfc', 'bpc']
def get_results(results_df):
    df = results_df[['hash', *results_fields]]
    return df

# Read all annotations from the files created by annotators
annotations_A = pd.read_csv('annotations_Michel.csv')
annotations_B = pd.read_csv('annotations_Abhishek.csv')
annotations_C = pd.read_csv('annotations_David.csv')

# Produce results, a dataframe with the fields to search results,
# for all annotators
results_A = get_results(annotations_A)
results_B = get_results(annotations_B)
results_C = get_results(annotations_C)

results = pd.merge(results_A, results_B, on='hash', how='inner', suffixes=('A', 'B'))
results = pd.merge(results, results_C, on='hash', how='inner')
results_renaming = {name: name + 'C' for name in results_fields}
results = results.rename(columns=results_renaming)

# Configuration for the fields to fill in by the reviewer
review_dds_cfg = {
    "iunderstd": {'label': "I understand the commit",
                  'choices': [0, 1, 2, 3, 4],
                  'interactive': False},
    "understd": {'label': "All understand the commit the same way",
                 'choices': [("True", True), ("False", False)],
                 'interactive': False},
    "bfc": {'label': "Bug fixing commit",
            'choices': [0, 1, 2, 3, 4],
            'interactive': False},
    "bpc": {'label': "Bug preventing commit",
            'choices': [0, 1, 2, 3, 4],
            'interactive': False},
    "prc": {'label': "Perfective commit",
            'choices': [0, 1, 2, 3, 4],
            'interactive': False},
    "nfc": {'label': "New feature commit",
            'choices': [0, 1, 2, 3, 4],
            'interactive': False},
    "asc": {'label': "Auto-suggested commit",
            'choices': [0, 1, 2, 3, 4],
            'interactive': False},
    "spec": {'label': "Specifications change commit",
             'choices': [0, 1, 2, 3, 4],
             'interactive': False},
    "obc": {'label': "Obvious bug",
            'choices': [0, 1, 2, 3, 4],
            'interactive': False},
    "safety": {'label': "Safety-related bug",
               'choices': [0, 1, 2, 3, 4],
               'interactive': False},
    "patchset": {'label': "Is part of a patchset",
                 'choices': [("True", True), ("False", False)],
                 'interactive': False}
}
review_cols = ['hash', 'reviewer', *review_dds_cfg.keys(), 'comment']

class ReviewsDF():
    """Class for storing reviews of annotations (as a dataframe)"""

    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename)
            self.df.replace({np.nan: None}, inplace=True)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=review_cols)

    def update(self, data):
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
            values = [None] * len(review_dds_cfg)
            values.append("")
        else:
            values = [review[label] for label in review_dds_cfg.keys()]
            values.append(review['comment'])
        return values

    def save(self, filename):
        self.df.to_csv(filename, index=False)


results_R = ReviewsDF(review_filename)

def get_annotation(df, hash):
    """Produce markdown for the annotation of a given short hash
    in the annotation dataframe
    """
    rows = df.loc[df['hash'].str.startswith(hash)]
    row = rows.iloc[0].to_dict()
    link = f"https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id={hash}"
    understand = row['understand']
    purpose = row['purpose']
    bfc = row['bfc']
    bpc = row['bpc']
    prc = row['prc']
    nfc = row['nfc']
    specification = row['specification']
    asc = row['asc']
    obvious = row['obvious']
    safety = row['safety']
    safety_exp = row['safety_exp']
    is_merge_commit = row['is_merge_commit']
    is_part_patchset = row['is_part_patchset']
    result = (f"[{hash}]({link})\n* Understand: {understand}\n"
              f"* **bfc:** {bfc} **bpc:** {bpc} "
              f"**prc:** {prc} **nfc:** {nfc} "
              f"**asc:** {asc} "
              f"**spec:** {specification}\n"
              f"* **obvious:** {obvious} "
              f"**safety:** {safety}\n"
              f"* **merge:** {is_merge_commit} "
              f"**patchset:** {is_part_patchset}\n"
              f"* **purpose:** {purpose}\n"
              f"* **safety_exp:** {safety_exp}\n")
    return result


with (gr.Blocks() as ui):
    with gr.Row():
        filter_field_ddw = gr.Dropdown(label="Field for selection",
                                 choices=[("BFC", "bfc"),
                                          ("BPC", "bpc")],
                                 value="bfc")
        filter_ddw = gr.Dropdown(label="Select commits",
                                 choices=[("All", "all"),
                                          ("All difference <= 1", "all-dif<=1"),
                                          ("Any difference > 1", "any-dif>1"),
                                          ("All difference, added > 1", "all-dif-sum>1"),
                                          ("All annotators equal", "all-equal"),
                                          ("Any annotator different", "any-dif"),
                                          ("Annotators A, B different", "ab-dif"),
                                          ("Annotators B, C different", "bc-dif"),
                                          ("Annotators A, C different", "ac-dif")],
                                 value="all")
        search_txt = gr.Textbox(label="Search commit")
        count_md = gr.Markdown(f"Commits: {len(results.index)}")
    results_df = gr.Dataframe(value=results, height=300)
    with gr.Row():
        A_md = gr.Markdown()
        B_md = gr.Markdown()
        C_md = gr.Markdown()
    with gr.Row():
        with gr.Column():
            R_txt = gr.Textbox(label="Comment by reviewer",
                               lines=5, interactive=False)
            R_lore = gr.Markdown(value=f"[Link to LORE]({URL_LORE})")
        with gr.Column():
            hash_txt = gr.Textbox(label="Selected hash", interactive=False)
            review_dds = [gr.Dropdown(**cfg) for cfg in review_dds_cfg.values()]
            R_btn = gr.Button("Save review", interactive=False)


    @filter_ddw.change(inputs=[filter_field_ddw, filter_ddw],
                       outputs=[results_df, count_md])
    def filter_records(field, choice):
        if choice == "all":
            df = results
        elif choice == "all-equal":
            df = results.query(f"({field}A == {field}B) and ({field}B == {field}C)")
        elif choice == "all-dif<=1":
            df = results.query(f"(abs({field}A-{field}B) <= 1) "
                               f"and (abs({field}B-{field}C) <= 1) "
                               f"and (abs({field}A-{field}C) <= 1)")
        elif choice == "any-dif>1":
            df = results.query(f"(abs({field}A-{field}B) > 1) "
                               f"or (abs({field}B-{field}C) > 1) "
                               f"or (abs({field}A-{field}C) > 1)")
        elif choice == "all-dif-sum>1":
            df = results.query(f"abs({field}A-{field}B) "
                               f"+ abs({field}B-{field}C) "
                               f"+ abs({field}A-{field}C) > 1")
        elif choice == "any-dif":
            df = results.query(f"({field}A != {field}B) or ({field}B != {field}C)")
        elif choice == "a!=b":
            df = results.query(f"{field}A != {field}B")
        elif choice == "b!=c":
            df = results.query(f"{field}B != {field}C")
        elif choice == "a!=c":
            df = results.query(f"{field}A != {field}C")
        else:
            raise ValueError("Choice not recognized")
        count = len(df.index)
        return df, f"Commits: {count}"


    @search_txt.change(inputs=[search_txt], outputs=[results_df, count_md])
    def find_record(hash):
        df = results[results['hash'].str.startswith(hash)]
        count = len(df.index)
        return df, f"Commits: {count}"


    def select_commit(event: gr.SelectData, results):
        # print(event.index, event.target, event.value, bfcs)
        row = results.iloc[event.index[0]]
        hash = row['hash']
        annot_A = get_annotation(annotations_A, hash)
        annot_B = get_annotation(annotations_B, hash)
        annot_C = get_annotation(annotations_C, hash)
        values = results_R.get_values(hash)
        updates = [gr.update(interactive=True, value=value) for value in values]
        return (hash,
                "**Michel**\n\n" + annot_A, "**Abishek**\n\n" + annot_B, "**David**\n\n" + annot_C,
                *updates
                )

    results_df.select(select_commit, inputs=[results_df],
                   outputs=[hash_txt, A_md, B_md, C_md,
                            *review_dds, R_txt])

    @R_btn.click(inputs=[hash_txt, R_txt, *review_dds],
                 outputs=[R_btn])
    def update_review(hash, comment, *review_dds):
        """Save review to file"""
        widgets = {'hash': hash,
                   'reviewer': 'jesus'}
        for widget, label in zip(review_dds, review_dds_cfg.keys()):
            widgets[label] = widget
        widgets['comment'] = comment
        results_R.update(widgets)
        results_R.save(review_filename)
        return gr.update(interactive=False)

    def review_changed():
        return gr.update(interactive=True)

    R_txt.change(review_changed, inputs=[], outputs=[R_btn])
    for review_dd in review_dds:
        review_dd.change(review_changed, inputs=[], outputs=[R_btn])

# port = 10020
# ui.launch(server_port=port)
ui.launch()