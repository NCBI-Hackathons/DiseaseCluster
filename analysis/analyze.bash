#!/usr/bin/env bash

#../bin/decomposition.py --expression ../data/tcga/test_data.txt --project ../data/tcga/metadata/full_transcriptome_sample_sheet.txt --image_prefix test --tissue_map ../data/tcga/metadata/cancer_tissue_map.txt --umap_nn 15

for pca in PCA  KernelPCA SparsePCA
do
	../bin/decomposition.py --expression ../data/tcga/merged_tcga_data.txt.gz --project ../data/tcga/metadata/full_transcriptome_sample_sheet.txt --image_prefix tcga --tissue_map ../data/tcga/metadata/cancer_tissue_map.txt --pca $pca &
done

for i in 5 15 30 60 120
do
	../bin/decomposition.py --expression ../data/tcga/merged_tcga_data.txt.gz --project ../data/tcga/metadata/full_transcriptome_sample_sheet.txt --image_prefix tcga --tissue_map ../data/tcga/metadata/cancer_tissue_map.txt --umap_nn $i &
done
wait

