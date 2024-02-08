# Code and data for the Linux bugs annotation project

## For annotators

### Installation

For running the annotator, you will need to use a version of Python (it has been tested with Python 3.11, it will likely work with 3.10 and other Python versions). It is recommended to use a virtual environment. You can create it and run it using the `venv` Python module. You can check a [detailed description of how venv works](https://docs.python.org/3/library/venv.html), but in summary, you will have to create it and activate it in your shell before running python scripts:

```python
python3 -m venv path/to/your/venv/directory
source path/to/your/venv/directory/bin/activate
```

Once the virtual environment is created and activated, install dependencies with `pip`:

```python
pip install -r requirements.txt
```

Now, you are ready to start your annotation.

### Annotation

Change to the directory commit-annotator, and run the script `annotator_ui.py`. For example:

```python
cd commit-annotator
python3 annotator_ui.py
```

This will launch a web server. To connect to it, and start annotating, launch a browser pointing to the url shown by the script. Then, check out all the information in the webpage, read the definitions of terms (below the "Previous" and "Next" buttons), write your annotator name in the top right text box (for example "jesus"), select a commit in the left column, and start annotating. When you are done with a commit, remember to save it.

>**Important**: For creating/loading the CSV file with the annotations, you have to fill out the form with the annotator name and presh the "Enter".

You can stop the process at any time, and kill the script. Every time you save a commit annotation, it will be saved to a CSV file. That file will be loaded when you launch the script again, and set in the browser the same annotator name. So, you will be able of resuming the annotation in the same state it was left.

For each commit, there are certain fields that should be filled in before the annotation can be saved: you will be informed by an info box if you try to save before filling them in.

If after reading the definitions in the browser there is something you don't understand, ask the annotation team before starting annotating.

When you are done with the annotation, look for your CSV file (it should be in the same directory), and send it to the annotation team.


#### Radio buttons version

Change to the radio buttons instead of dropdowns in the commit-annotator app, running the script `annotator_ui.py` with the following argument:

```python
cd commit-annotator
python3 annotator_ui.py --radio
```