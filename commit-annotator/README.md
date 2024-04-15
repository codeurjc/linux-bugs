# Commit Annotator

This is the annotation tool, intended to annotate commits of the Linux kernel.

## Installation

Create a Python virtual environment, and install in it the dependencies found in the [requirements.txt](../requirements.txt) file in the parent directory. There are some more details about this process in the [README.md](../README.md) file in the parent directory.

## Annotation procedure

Read carefully the [procedure.md](procedure.md) file in this directory, to understand what to read before annotating, and the annotation procedure itself.

## Running the annotation tool

Activate the virtual environment used for the installation. Once that is done, run `annotator_ui.py`. The tool admits some arguments, launch it with the `--help` flag to learn about them.

## Annotator comments

If you have any comments about "special cases" that you find while annotation, please open an annotator comments file in this directory. The file name will be your annotator name (the same you're using in the annotation tool) plus ".md". Write the comments formatted as Markdown text (if any markup is needed).

This file is intended to be useful during the analysis of the annotations. Special cases would be cases where the definitions are not considering it, or you feel something is wrong with the approach, for example. This is different from your comments when annotating commits (where you can of course also include the same comment). This file would  be only for those rare cases which you don't want to forget when analyzing results. Be as much specific as possible when writting this file, including the hash of the affected commit.
