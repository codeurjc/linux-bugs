import pandas as pd
import gradio as gr

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

# Manage reviewer file
review_cols = ['hash', 'reviewer', 'iunderstd', 'understd',
               'bfc', 'bpc', 'asc', 'obc', 'safety', 'comment']
review_filename = 'review.csv'


class ReviewsDF():
    """Class for storing reviews of annotations (as a dataframe)"""

    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename)
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
            iunderstd = None
            understd = None
            bfc = None
            bpc = None
            asc = None
            obc = None
            safety = None
            text = ""
        else:
            iunderstd = review['iunderstd']
            understd = review['understd']
            bfc = review['bfc']
            bpc = review['bpc']
            asc = review['asc']
            obc = review['obc']
            safety = review['safety']
            text = review['comment']
        print(iunderstd)
        return iunderstd, understd, bfc, bpc, asc, obc, safety, text

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
    asc = row['asc']
    obvious = row['obvious']
    safety = row['safety']
    safety_exp = row['safety_exp']
    result = (f"[{hash}]({link})\n* Understand: {understand}\n"
              f"* bfc: {bfc}\n"
              f"* bpc: {bpc}\n* asc: {asc}\n"
              f"* obvious: {obvious}\n"
              f"* safety: {safety}\n"
              f"* **purpose:** {purpose}\n"
              f"* **safety_exp:** {safety_exp}\n")
    return result


with gr.Blocks() as ui:
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
        R_txt = gr.Textbox(label="Comment by reviewer",
                           lines=5, interactive=False)
        with gr.Column():
            hash_txt = gr.Textbox(label="Selected hash", interactive=False)
            Riunderstd_dd = gr.Dropdown(label="I understand the commit",
                                  choices=[0, 1, 2, 3, 4],
                                  interactive=False)
            Runderstd_dd = gr.Dropdown(label="All understand the commit the same way",
                                  choices=[("True", True), ("False", False)],
                                  interactive=False)
            Rbfc_dd = gr.Dropdown(label="Bug fixing commit",
                                  choices=[0, 1, 2, 3, 4],
                                  interactive=False)
            Rbpc_dd = gr.Dropdown(label="Bug preventing commit",
                                  choices=[0, 1, 2, 3, 4],
                                  interactive=False)
            Rasc_dd = gr.Dropdown(label="Auto-suggested commit",
                                  choices=[0, 1, 2, 3, 4],
                                  interactive=False)
            Robc_dd = gr.Dropdown(label="Obvious commit",
                                  choices=[0, 1, 2, 3, 4],
                                  interactive=False)
            Rsafety_dd = gr.Dropdown(label="Safety-related bug",
                                  choices=[0, 1, 2, 3, 4],
                                  interactive=False)
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
        iunderstd, understd, bfc, bpc, asc, obc, safety, text = BFCs_R.get_values(hash)
        print("iunderstand:", iunderstd)
        return (hash,
                 "**Michel**\n\n" + annot_A, "**Abishek**\n\n" + annot_B, "**David**\n\n" + annot_C,
                gr.update(interactive=True, value=iunderstd),
                gr.update(interactive=True, value=understd),
                gr.update(interactive=True, value=bfc),
                gr.update(interactive=True, value=bpc),
                gr.update(interactive=True, value=asc),
                gr.update(interactive=True, value=obc),
                gr.update(interactive=True, value=safety),
                gr.update(interactive=True, value=text),
                )

    bfcs_df.select(select_commit, inputs=[bfcs_df],
                   outputs=[hash_txt, A_md, B_md, C_md,
                            Riunderstd_dd, Runderstd_dd,
                            Rbfc_dd, Rbpc_dd, Rasc_dd, Robc_dd, Rsafety_dd,
                            R_txt])

    @R_btn.click(inputs=[hash_txt, R_txt, Riunderstd_dd, Runderstd_dd,
                         Rbfc_dd, Rbpc_dd, Rasc_dd, Robc_dd, Rsafety_dd],
                 outputs=[R_btn])
    def update_review(hash, review, iunderstd, understd,
                      bfc, bpc, asc, obc, safety):
        BFCs_R.update({'hash': hash,
                       'reviewer': 'jesus',
                       'iunderstd': iunderstd,
                       'understd': understd,
                       'bfc': bfc,
                       'bpc': bpc,
                       'asc': asc,
                       'obc': obc,
                       'safety': safety,
                       'comment': review
                       })
        BFCs_R.save(review_filename)
        return gr.update(interactive=False)

    def review_changed():
        return gr.update(interactive=True)

    R_txt.change(review_changed, inputs=[], outputs=[R_btn])
    Riunderstd_dd.change(review_changed, inputs=[], outputs=[R_btn])
    Runderstd_dd.change(review_changed, inputs=[], outputs=[R_btn])
    Rbfc_dd.change(review_changed, inputs=[], outputs=[R_btn])
    Rbpc_dd.change(review_changed, inputs=[], outputs=[R_btn])
    Rasc_dd.change(review_changed, inputs=[], outputs=[R_btn])
    Robc_dd.change(review_changed, inputs=[], outputs=[R_btn])
    Rsafety_dd.change(review_changed, inputs=[], outputs=[R_btn])

# port = 10020
# ui.launch(server_port=port)
ui.launch()