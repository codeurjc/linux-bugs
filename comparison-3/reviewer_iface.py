import pandas as pd
import numpy as np
import gradio as gr

URL_LORE = "https://lore.kernel.org/all/?q="

def get_BFCs(results_df):
    df = results_df[['hash', 'bfc']]
    return df

results_A = pd.read_csv('annotations_Michel.csv')
results_B = pd.read_csv('annotations_Abhishek.csv')
results_C = pd.read_csv('annotations_David.csv')

BFCs_A = get_BFCs(results_A)
BFCs_B = get_BFCs(results_B)
BFCs_C = get_BFCs(results_C)

BFCs = pd.merge(BFCs_A, BFCs_B, on='hash', how='inner', suffixes=('A', 'B'))

BFCs = pd.merge(BFCs, BFCs_C, on='hash', how='inner', suffixes=('', 'C'))
BFCs = BFCs[['hash', 'bfcA', 'bfcB', 'bfc']]
BFCs = BFCs.rename(columns={'bfc': 'bfcC'})

# Reviewer file
review_filename = 'review.csv'

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


BFCs_R = ReviewsDF(review_filename)

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
        count_md = gr.Markdown(f"Commits: {len(BFCs.index)}")
    bfcs_df = gr.Dataframe(value=BFCs, height=300)
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


    @filter_ddw.change(inputs=[filter_ddw], outputs=[bfcs_df, count_md])
    def filter_records(choice):
        if choice == "all":
            df = BFCs
        elif choice == "all-equal":
            df = BFCs.query("(bfcA == bfcB) and (bfcB == bfcC)")
        elif choice == "all-dif<=1":
            df = BFCs.query("(abs(bfcA-bfcB) <= 1) and (abs(bfcB-bfcC) <= 1) and (abs(bfcA-bfcC) <= 1)")
        elif choice == "any-dif>1":
            df = BFCs.query("(abs(bfcA-bfcB) > 1) or (abs(bfcB-bfcC) > 1) or (abs(bfcA-bfcC) > 1)")
        elif choice == "all-dif-sum>1":
            df = BFCs.query("abs(bfcA-bfcB) + abs(bfcB-bfcC) + abs(bfcA-bfcC) > 1")
        elif choice == "any-dif":
            df = BFCs.query("(bfcA != bfcB) or (bfcB != bfcC)")
        elif choice == "ab-dif":
            df = BFCs.query("bfcA != bfcB")
        elif choice == "bc-dif":
            df = BFCs.query("bfcB != bfcC")
        elif choice == "ac-dif":
            df = BFCs.query("bfcA != bfcC")
        count = len(df.index)
        return df, f"Commits: {count}"


    @search_txt.change(inputs=[search_txt], outputs=[bfcs_df, count_md])
    def find_record(hash):
        df = BFCs[BFCs['hash'].str.startswith(hash)]
        count = len(df.index)
        return df, f"Commits: {count}"


    def select_commit(event: gr.SelectData, bfcs):
        # print(event.index, event.target, event.value, bfcs)
        row = bfcs.iloc[event.index[0]]
        hash = row['hash']
        annot_A = get_annotation(results_A, hash)
        annot_B = get_annotation(results_B, hash)
        annot_C = get_annotation(results_C, hash)
        values = BFCs_R.get_values(hash)
        updates = [gr.update(interactive=True, value=value) for value in values]
        return (hash,
                "**Michel**\n\n" + annot_A, "**Abishek**\n\n" + annot_B, "**David**\n\n" + annot_C,
                *updates
                )

    bfcs_df.select(select_commit, inputs=[bfcs_df],
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
        BFCs_R.update(widgets)
        BFCs_R.save(review_filename)
        return gr.update(interactive=False)

    def review_changed():
        return gr.update(interactive=True)

    R_txt.change(review_changed, inputs=[], outputs=[R_btn])
    for review_dd in review_dds:
        review_dd.change(review_changed, inputs=[], outputs=[R_btn])

# port = 10020
# ui.launch(server_port=port)
ui.launch()