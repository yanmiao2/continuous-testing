Instruction to run ECE484 MP0 Autograder with Verse
---
Yan (yanmiao2@illinois.edu)
3/26/2024

Running code ```python3 grading_wrapper.py```

The autograder will take all submissions (named with concat of netids) in `/submission` folder (currently one good DL and one bad DL there for example, full submissions can be found in `/23FA_MP0_Submission`) to evaluate. 

The scores will be stored in `class_mp1_score.txt`. The four logs (png, html, grade.txt, counter-example.txt) of each group will be stored in `/log`, naming after the netid of the first person in the group.

The other autograder functionality is available but not included in the repo for now due to security issue (i.e. private keys).