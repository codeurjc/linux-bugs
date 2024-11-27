# Disagreements between annotators

This folder has the content of the session where the annotators (Abhishek, Michel and David) talked about their annotations and they (maybe) decided to change the annotations:

## First round

Annotators will discuss the disagreement they had annotating the commits, then they decide if the want to change the annotation of those commits. Those files should have the name `<annotator_name>_first_round.csv`.

- Disagreement on BPC, BFC, PRC, and NFC. When the difference is at least 1.


## Second round

On the commits that already there is a disagreement, the authors should check Jesús reviews of those commits and then annotate them again. Those files should have the name `<annotator_name>_second_round.csv`.


## Third round (TBD)

Add ML/AI annotations and compare


## CSV files in data folder

- `annotations_<name>.csv`: Annotations of the 1000 commits of each annotator, **before** round 1.
- `annotations_<name>1.csv`: Annotations of those commits where the annotator changed his mind during round 1.
- `round1_annotations_<name>.csv`: Annotations of the 1000 commits of each annotator, **after** round 1.
- `annotations_<name>2.csv`: Annotations of those commits where the annotator changed his mind during round 2.
- `round2_annotations_<name>.csv`: Annotations of the 1000 commits of each annotator, **after** round 2.
- `round0_disagreement_bfc_hashes.csv`: Hashes of those commits where the authors had disagreement in BFC **before** round 1.
- `round1_disagreement_bfc_hashes.csv`: Hashes of those commits where the authors had disagreement in BFC **before** round 2.
- `round2_disagreement_bfc_hashes.csv`: Hashes of those commits where the authors had disagreement in BFC **after** round 2.
- `reviews_jesus.csv`: Annotations of Jesus of those commits where the annotators had disagreement in BFC, **before** round 1.
- `round2_review_jesus_filtered_annotations.csv`: Annotations of Jesus of those commits where the annotators had disagreement in BFC, filtered only to those where the annotators have still disagreement **after** round 1.