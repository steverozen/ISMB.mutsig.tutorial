# ISMB.mutsig.tutorial

Welcome to the ISMB2020 Online Mutational Signature Analysis Tutorial, July 11 and 12, 2020 (https://www.iscb.org/ismb2020-program/tutorials#tut1)

## Please do before the tutorial

1. Please have R >= 4.0.0 installed on your computer.

2. Please install the CRAN package ICAMS and its prerequisites.
```
install.packages("ICAMS")
```

3. Please install BSgenome.Hsapiens.1000genomes.hs37d5 from Bioconductor:
```
install.packages("BiocManager")
BiocManager::install("BSgenome.Hsapiens.1000genomes.hs37d5")
```
4. Additional R libraries that will be needed:

4.1 CRAN packages philentropy, gplots, factoextra

4.2 Github packages:
```
remotes::install_github("steverozen/mSigBG", ref = "1.0-branch")
remotes::install_github("steverozen/PCAWG7")
```

If you have difficulties contact Nanhai JIANG at nanhai.jiang@u.duke.nus.edu.

You will need this for the practicum on July 11. The practicum inputs will be released shortly. 

The slides are:

0. https://github.com/steverozen/ISMB.mutsig.tutorial/raw/master/Tut1.Lecture.0.short.intro.pptx
1. https://github.com/steverozen/ISMB.mutsig.tutorial/raw/master/Tut1.Lecture.1.Mutational-Signatures%202020_07_10.pptx
2. https://github.com/steverozen/ISMB.mutsig.tutorial/raw/master/Tut1.Lecture.2.data-mining.NMF.and.HPD.2020.07.10.pptx
3. https://github.com/steverozen/ISMB.mutsig.tutorial/raw/master/Tut1.lecture.3.landscape_tactics_20200710.pptx

