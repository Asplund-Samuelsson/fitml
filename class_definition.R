options(width=150)

# Load libraries
library(tidyverse)

# Define infiles
exp_file = "/home/johannes/proj/crse/data/2018-11-20/feba_experiment.csv.gz"

# Load data
experiment = read_csv(exp_file, guess_max=1e6)

# Keep only interesting information
experiment = select(
    experiment,
    orgId, expName, expDesc, expGroup,
    condition_1, units_1, concentration_1,
    condition_2, units_2, concentration_2
  )

# Getting a list of all the conditions
conditions = unique(c(experiment$condition_1, experiment$condition_2))
# 170 conditions

toxic_metals = c(
  "nickel", "copper", "zinc", "cadmium",
  "uranyl", "cobalt", "aluminum", "thallium"
)

antibiotics = c(
  "sisomicin", "polymyxin", "phosphomycin", "fusidic acid",
  "chloramphenicol", "cycloserine", "ceftazidime", "rifampicin",
  "benzethonium", "lomefloxacin", "nalidixic acid", "benzalkonium chloride",
  "neomycin", "bacitracin", "tetracycline", "cephalothin",
  "doxycycline", "spectinomycin", "vancomycin", "carbenicillin",
  "gentamicin", "G418"
)

# Check that experiment identification works
toxic_metal_conditions = conditions[
  unlist(lapply(toxic_metals, function(x){grep(x, conditions, ignore.case=T)}))
]

antibiotics_conditions = conditions[
  unlist(lapply(antibiotics, function(x){grep(x, conditions, ignore.case=T)}))
]

# Parse the experiment conditions to determine classes
experiment = mutate(
  experiment,
  metal = ifelse(
    condition_1 %in% toxic_metal_conditions |
    condition_2 %in% toxic_metal_conditions,
    1, 0
  ),
  antibiotics = ifelse(
    condition_1 %in% antibiotics_conditions |
    condition_2 %in% antibiotics_conditions,
    1, 0
  )
)

# Write class definitions to table
write_tsv(
  select(experiment, orgId, expName, expDesc, metal, antibiotics),
  "/home/johannes/proj/crse/results/2018-11-22/feba_experiment_classes.tab"
)
