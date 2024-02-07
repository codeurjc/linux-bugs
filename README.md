# Code and data for the Linux bugs annotation project

## Annotation

Change to the directory commit-annotator, and run the script `annotator_ui.py`. For example:

```python
cd commit-annotator
python3 annotator_ui.py
```

This will launch a web server. To connect to it, and start annotating, launch a browser pointing to the url shown by the script. Then, check out all the information in the webpage, read the definitions of terms (below the "Previous" and "Next" buttons), write your annotator name in the top right text box (for example "jesus"), select a commit in the left column, and start annotating. When you are done with a commit, remember to save it.

You can stop the process at any time, and kill the script. Every time you save a commit annotation, it will be saved to a CSV file. That file will be loaded when you launch the script again, and set in the browser the same annotator name. So, you will be able of resuming the annotation in the same state it was left.

For each commit, there are certain fields that should be filled in before the annotation can be saved: you will be informed by an info box if you try to save before filling them in.

If after reading the definitions in the browser there is something you don't understand, ask the annotation team before starting annotating.

When you are done with the annotation, look for your CSV file (it should be in the same directory), and send it to the annotation team.