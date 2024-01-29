import pandas as pd
import gradio as gr

def get_BFCs(results_df):
    df = results_df[['id', 'commit_hash', 'is_bug_fixing_commit']]
    df = df.rename(columns={'commit_hash': 'hash', 'is_bug_fixing_commit': 'BFC'})
    df['hash'] = df['hash'].str.slice(0, 10)
    return df

results_A = pd.read_csv('130_results_michel.csv')
results_B = pd.read_csv('130_results_abhishek.csv')
results_C = pd.read_csv('130_results_david.csv')

BFCs_A = get_BFCs(results_A)
BFCs_B = get_BFCs(results_B)
BFCs_C = get_BFCs(results_C)

BFCs = pd.merge(BFCs_A, BFCs_B, on='hash', how='inner', suffixes=('A', 'B'))

BFCs = pd.merge(BFCs, BFCs_C, on='hash', how='inner', suffixes=('', 'C'))
BFCs = BFCs[['hash', 'BFCA', 'BFCB', 'BFC']]
BFCs = BFCs.rename(columns={'BFC': 'BFCC'})

# Manage reviewer file
review_cols = ['hash', 'reviewer', 'bfc', 'comment', 'understanding']
review_filename = '130_review.csv'


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
            text = ""
            bfc = None
            understanding = None
        else:
            text = review['comment']
            bfc = review['bfc']
            understanding = review['understanding']
        return text, bfc, understanding

    def save(self, filename):
        self.df.to_csv(filename, index=False)


BFCs_R = ReviewsDF(review_filename)

def get_annotation(df, hash):
    """Produce markdown for the annotation of a given short hash
    in the annotation dataframe
    """
    rows = df.loc[df['commit_hash'].str.startswith(hash)]
    row = rows.iloc[0].to_dict()
    hash_long = row['commit_hash']
    link = f"https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?h=v6.7&id={hash}"
    is_bfc = row['is_bug_fixing_commit']
    is_obvious = row['is_obvious_bug']
    is_safety = row['is_safety_related']
    comment = row['comment']
    visited = row['link_visited']
    result = (f"[{hash}]({link})\n* bfc: {is_bfc}\n* obvious: {is_obvious}\n"
              f"* safety: {is_safety}\n* visited: {visited}\n"
              f"* comment: {comment}")
    return result


with gr.Blocks() as ui:
    with gr.Row():
        filter_ddw = gr.Dropdown(label="Select commits",
                                 choices=[("All", "all"),
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
            Rbfc_dd = gr.Dropdown(label="Bug fixing commit",
                                  choices=[("True", True), ("False", False)],
                                  interactive=False)
            Runderstd_dd = gr.Dropdown(label="All understand the commit the same way",
                                  choices=[("True", True), ("False", False)],
                                  interactive=False)
            R_btn = gr.Button("Save review", interactive=False)


    @filter_ddw.change(inputs=[filter_ddw], outputs=[bfcs_df, count_md])
    def filter_records(choice):
        if choice == "all":
            df = BFCs
        elif choice == "all-equal":
            df = BFCs.query("(BFCA == BFCB) and (BFCB == BFCC)")
        elif choice == "any-dif":
            df = BFCs.query("(BFCA != BFCB) or (BFCB != BFCC)")
        elif choice == "ab-dif":
            df = BFCs.query("BFCA != BFCB")
        elif choice == "bc-dif":
            df = BFCs.query("BFCB != BFCC")
        elif choice == "ac-dif":
            df = BFCs.query("BFCA != BFCC")
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
        text, bfc, understanding = BFCs_R.get_values(hash)
        # review = BFCs_R.get(hash)
        # if review is None:
        #     review_text = ""
        #     review_bfc = None
        # else:
        #     review_text = review['comment']
        #     review_bfc = review['bfc']
        return (hash,
                "**A**\n\n" + annot_A, "**B**\n\n" + annot_B, "**C**\n\n" + annot_C,
                gr.update(interactive=True, value=text),
                gr.update(interactive=True, value=bfc),
                gr.update(interactive=True, value=understanding))

    bfcs_df.select(select_commit, inputs=[bfcs_df],
                   outputs=[hash_txt, A_md, B_md, C_md, R_txt, Rbfc_dd, Runderstd_dd])

    @R_btn.click(inputs=[hash_txt, R_txt, Rbfc_dd, Runderstd_dd], outputs=[R_btn])
    def update_review(hash, review, bfc, understanding):
        BFCs_R.update({'hash': hash,
                       'reviewer': 'jesus',
                       'bfc': bfc,
                       'comment': review,
                       'understanding': understanding})
        BFCs_R.save(review_filename)
        return gr.update(interactive=False)

    def review_changed():
        return gr.update(interactive=True)

    R_txt.change(review_changed, inputs=[], outputs=[R_btn])
    Rbfc_dd.change(review_changed, inputs=[], outputs=[R_btn])

# port = 10020
# ui.launch(server_port=port)
ui.launch()