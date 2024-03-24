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

Start with the first commit in the commit list you see on the left column, by clicking on it. Move to the next commit once you are done with the annoation of the first commit, and so on. You can do that by clikcing on it, or by clicking the "Next" button at the bottom of the middle column (preferible). If possible, don't come back to an already annotated commit, but do so if there are some errors or something you need to fix in your annotation.


## Continue annotation by restarting the tool

First of all, fill in your annotator name. Be sure of writing it exactly the same way you did the first time, because it will be used to find the name of your annotation file. If this file is found, it will be loaded, showing the state of your annoations. Check the list of commits, on the left column, to see it reflects your past annotations (if nedeed, use the "Show" filter).

Once your annoation file was loaded, go on annotating as described for the first time.
