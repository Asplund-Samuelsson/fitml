options(width=150)

# Load libraries
library(tidyverse)

# Define infiles
dom_file = "/home/johannes/proj/crse/data/2018-11-20/feba_genedomain.csv.gz"

# Load data
genedomain = read_csv(dom_file)

# Check the number of unique TIGRFams per organism
# filter(genedomain, domainDb == "TIGRFam") %>% group_by(orgId) %>%
#   summarise(TIGRs = length(unique(domainId))) %>% as.data.frame
# -> Between 748 and 1529

# Check the number of unique TIGRFams in the whole dataset
# length(unique(filter(genedomain, domainDb == "TIGRFam")$domainId))
# -> 2796

# Count the number of TIGRFams per organism
dom_count = filter(genedomain, domainDb == "TIGRFam") %>%
  group_by(orgId, domainId) %>% summarise(n = length(domainId))

# Remove TIGRFams that have more than 1 representative in any organism
dom_single = dom_count %>% filter(!(domainId %in% filter(., n > 1)$domainId))

# Check the number of TIGRFams per organism
# dom_single %>% group_by(orgId) %>% summarise(TIGRs = length(domainId)) %>%
#   as.data.frame
# -> Between 375 and 839

# Keep only TIGRFams that occur in all organisms
dom_universal = dom_single %>% group_by(domainId) %>%
  summarise(N = length(orgId)) %>% filter(N == length(unique(dom_single$orgId)))
# 137 TIGRFams

# Keep only TIGRFams that occur in at least 50% of the organisms
dom_common = dom_single %>% group_by(domainId) %>%
  summarise(N = length(orgId)) %>%
  filter(N >= 0.5*length(unique(dom_single$orgId)))
# 459 TIGRFams

# Create lists
gene_universal = inner_join(
  dom_universal, select(genedomain, locusId, orgId, domainId)
)

gene_common = inner_join(
  dom_common, select(genedomain, locusId, orgId, domainId)
)

# Save tables
out_universal = "/home/johannes/proj/crse/results/2018-11-21/feba_universal_genes.tab"
out_common = "/home/johannes/proj/crse/results/2018-11-21/feba_common_genes.tab"
write_tsv(gene_universal, out_universal)
write_tsv(gene_common, out_common)
