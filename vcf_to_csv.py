#!/usr/bin/env python3

import numpy as np

#### Read in VCF
vcf_lines = []
with open('coral.vcf', 'r') as vcf:
    for line in vcf.readlines():
        l2 = line.rstrip()
        l3 = l2.split('\t')
        if line.startswith('#CHROM') or not line.startswith('#'):
            vcf_lines.append(l3)
        

#### Generate list of individuals and their id's from bams
##  Some individuals (like W104) have multiple reps (W104_1, W104_2)
##  ... deal with after making large table
header = vcf_lines[0]

ids = []
for column_name in header:
    if column_name.endswith('.bam'):
        # Split the id and keep location + tag number + replicate (if applicable) e.g. CN_xxx_1
        id_as_list = column_name.split('.')[0].split('_')[2:]

        # Join back into single string
        id = '_'.join(id_as_list)
    
        ids.append(id)

#### Generate new header as list of keys
##   Note info cols apply to snp's across all samples
default_vcf_cols = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER']
info_cols = []
format_cols = []

## Get info cols headers
for col in vcf_lines[1]:
    if ';' in col:
        full_info_cols_list = col.split(';')        # returns e.g. ['NS=149', 'DP=6637', 'AF=0.130868']        
        
        for info_col in full_info_cols_list:
            info_col_name = info_col.split('=')[0]

            ## there are two 'DP' columns...
            if info_col_name == 'DP':
                info_cols.append('INFO_DP')
            else:
                info_cols.append(info_col_name)
            
    
## Get format cols headers
for col in vcf_lines[1]:
    if 'GT' in col:
        format_cols = col.split(':')      # returns e.g. ['GT', 'DP', 'GL', 'PL', 'GP']
        

## Fix DP column in format cols (there are two DP columns...)
for i in range(len(format_cols)):
    if format_cols[i] == 'DP':
        format_cols[i] = 'FORMAT_DP'


## Combine into new header
new_header = default_vcf_cols + info_cols + format_cols
new_header.insert(0, 'BAM_ID')
new_header.insert(0, 'CORAL_ID')


#### Pivot Longer
# ['CORAL_ID', 'BAM_ID', 'CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'NS', 'DP', 'AF', 'GT', 'DP', 'GL', 'PL', 'GP']
tsv_rows = []
for i in range(len(ids)):
    # get the bam ID extracted from bam names
    bam_id = ids[i]

    # get the coral ID from the bam ID
    coral_id = bam_id.split('_')[1]

    # the index (column number) of this individual's format columns in the original csv 
    bam_id_index = 9 + i

    # loop over vcf
    for vcf_line in vcf_lines:
        # skip first line of vcf_lines (it's the old header line)
        if vcf_line[0].startswith('#'):
            continue
        
        # construct row column by column
        row = []

        # add coral id and bam_id as first two columns
        row.append(coral_id)
        row.append(bam_id)

        # add default/standard vcf cols 
        for i in range(len(vcf_line)):
            if i < 7: 
                row.append(vcf_line[i])

        # split the INFO column
        # this information per SNP will be constant across all individuals 
        info_cols = vcf_line[7].split(';')
        #print(info_cols)
        for col in info_cols:
            col_value = col.split('=')[1]
            row.append(col_value)


        # split the FORMAT column into individual columns and add them.
        # note for each coral ID this will have to depend on `coral_id_index` 
        # of the original file
        format_cols = vcf_line[bam_id_index].split(':')
        for col in format_cols:
            row.append(col)
        
        ts_row = '\t'.join(row)

        tsv_rows.append(ts_row)


#### Format csv_rows into actual csv rows
# add header
new_header_ts = '\t'.join(new_header)
tsv_rows.insert(0, new_header_ts)

# write to csv
with open('vcf.tsv', 'w') as tsv:
    for line in tsv_rows:
        tsv.write("%s\n" % line)
