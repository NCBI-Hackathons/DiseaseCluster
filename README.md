# DiseaseCluster
==========
### DiseaseCluster is a pipeline of disease prediction based on transcriptomic clustering
#### Hackathon Team
Lead - Mathew Moss

SysAdmins - Gordon Lemmon, Yaxin Xue

Data Wrangler - Ben Harris

PseudoBulk Pipline, Data Finder, Writer - Meghan Ferrall-Fairbanks

### How to cite this work in a publication: [citation to be determined here]
[doi here]

In the move towards personalized medicine, it would be helpful if physicans could visualize their patients across different disease states to help determine potential therapeutic options for their patients. As wet-lab scientific techniques move from the bench-to-bedside, RNA-sequencing can allow physicians the opportunity to detect and quantify patient-specific mRNA signature and understand more about how they relate to cellular signaling in a disease-context. 

*DiseaseCluster* is a versatile workflow that using principle component analysis to clusters transcriptomic data for a variety of disease states and allows researchers and clinicians to visually compare an uploaded patient sample in the disease space. 

Objective: Create a resuable, reproducible, and interactive workflow to cluster transcriptomic data based on disease state. Furthermore, the workflow will allow for researchers/clinicians to upload new transcriptomic datasets to visualize how the new data compares to the disease space. The disease space currently describes cancer samples profiled in TCGA. 

This project was part of the [2018 Cold Spring Harbor Biological Data Science NCBI Hackathon](https://biohackathons.github.io/).

## Dependencies

## DiseaseCluster Workflow


The DiseaseCluster pipeline workflow is described in the figure above. First, TCGA transcriptomic data was downloaded and additional bulk RNAseq data will be added to expand disease types analyzed.  Data was coverted from FPKM to TPM, non-protein coding genes wer removed and the data was log transformed. UMAP (uniform manifold approximation and projection) was performed on the expression matrix to reduce the dimensionality to two dimensions in latent space based on gene expression. Clustered data was then overlaid with annotated information about the disease state, including known variants. This map is then visualized by a Boken interactive user interface.

## Deliverables 

## Installation

## Usage

## Input File Format

Researchers and clinicians can input new RNAseq disease samples.  The pipeline accepts a file format of X. 

## Output

## Exploration and Validation

## F.A.Q. 
1. How to cite? 

2. How to use? 

Follow the instructions on this page.

3. What if I need help?

Feel free to contact authors if you need help. 

## References

## People/Team
* *Matthew Moss*, CSHL, Cold Spring Harbor, NY, USA, [moss@cshl.edu](mailto:moss@cshl.edu) 
* *Meghan Ferrall-Fairbanks*, Moffitt Cancer Center and Research Institute, Tampa, FL, USA, [meghan.ferrall-fairbanks@moffitt.org](mailto:meghan.ferrall-fairbanks@moffitt.org) 
* *Benjamin Harris*, CSHL, Cold Spring Harbor, NY, USA, [bharris@cshl.edu](mailto:bharris@cshl.edu)
* *Gordon Howard Lemmon*, University of Utah, Salt Lake City, UT, USA, [gordon.lemmon@utah.edu](mailto:gordon.lemmon@utah.edu)
* *Yaxin Xue*, University of Bergen, Bergen, Norwary, [yaxin.xue@uib.no](mailto:yaxin.xue@uib.no)


