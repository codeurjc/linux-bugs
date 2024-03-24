# Procedure for annotation

## Before starting annotation for the first time

Please, carefully read the [README.md](README.md), [context.md](context.md), and [definitions.md] in this directory, in that order. Become familiar with the definitions we are using, and understand the context of the annotation, including its aims, and its nuances.

## Starting annotating tool

Activate the Python virtual environment used to install it:

```shell
% python annotator_ui.py 
Running on local URL:  http://localhost:7860

To create a public link, set `share=True` in `launch()`.
```

This will launch the annotation tool. If it runs successfully, it shows the URL to write in the URL textbox in a browser to access the interface provided by the tool. There are some arguments that can be passed to the annotation tool, launch it with the `--help` flag to learn about them.

If this is the first time you start the tool to annotate, read "Start annotating for the first time", below. If not, read "Continue annotation by restarting the tool"

## Start annotating for the first time

First of all, fill in your annotator name. It should be a character string, with no spaces (to be on the safe side, use only letters and numbers). Your annotation file will use that string as a suffix. All your annotations will be saved to that file (but only when the "Save annotation" button is clicked, see below).

Start with the first commit in the commit list you see on the left column, by clicking on it. Move to the next commit once you are done with the annotation of the first commit, and so on. You can do that by clicking on it, or by clicking the "Next" button at the bottom of the middle column (preferible). If possible, don't come back to an already annotated commit, but do so if there are some errors or something you need to fix in your annotation.

Once the data for commit to annotate is loaded, you'll find that data in the middle column: the hash at the top, the commit comment at the bottom. There are also two buttons, to see the commit information in the kernel GitHub repository, which gives access to the changes to the source code and some more context, and to a search in the kernel lore based on the first line of the commit record. Important: if the commit is a merge commit, a message informing of that will also appear.

In the middle column there are also three checks to annotate: if the commit was found in the lore, which will be selected automatically when the corresponding button is pressed; if the commit was found in the lore; and if it is a part of a patchset). On the right column there is the rest of the information to provide as annotation.

Now, we're ready to annotate the first commit, and follow on with the next ones.

## Procedure for each commit

* Check if the commit is a merge commit. If it is, just move to the next commit.

* Search for the commit in the kernel lore. Mark that you searched for it, and if found it is a part of a patchset, mark that too. In this case, read the message describing the patchset, and have that information as context.

* Read carefully the text of the commit (in the middle column). Only click on the link to see the commit in GitHub if you really need it. Now, briefly describe the purpose of the commit. This is not exactly a summary of the commit, but a description that should inform your decisions. Usually it will be very short description of your understanding of it, and if you feel that's convenient, the reasons for your annotation (specially if they are not too obvious). For example, "Has into account a condition that was missing, fixing a bug with that. The bug could cause a hang when an interrupt is triggered." Remember that this information is mainly for people who may review your annotation. Fill in also how well you think you understand the commit.

* Annotate if the commit is a BFC, a BPC, a PRC or a NFC, in this order. Remember that it can be in more than one category, but only if there are specific reasons for it (re-read the context file if you don't remember about this). The scale for each of them should be read as "Of the five options, this is the one closer to my decision".

* Then, fill in if the commit is related to a change in specifications or an ASC.

* Then, only if you think the commit could be a BFC (anything above "No, I'm sure"), check if it is an obvious bug.

* Also, only if you think the commit could be a BFC, check if it is safety-related. In this latter case, check also at least one of the three categories (except if you are completely sure it doesn't belong to any of them), and fill in also the comment about your reasons for that.

* When done, click the "Save annotation" button at the bottom of the right column. Only then, the annotation will be saved.

## Continue annotation by restarting the tool

First of all, fill in your annotator name. Be sure of writing it exactly the same way you did the first time, because it will be used to find the name of your annotation file. If this file is found, it will be loaded, showing the state of your annotations. Check the list of commits, on the left column, to see it reflects your past annotations (if nedeed, use the "Show" filter).

Once your annotation file was loaded, go on annotating each commit as described above. Start with the commit next to the last one that you annotated earlier.

