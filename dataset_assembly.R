options(width=150)

# Load libraries
library(tidyverse)

# Define infiles
feature_file = "/home/johannes/proj/crse/results/2018-11-21/feba_common_genes.tab"
class_file = "/home/johannes/proj/crse/results/2018-11-22/feba_experiment_classes.tab"
fitness_file = "/home/johannes/proj/crse/data/2018-11-20/feba_genefitness.csv.gz"

# Load data
features = read_tsv(feature_file)
classes = read_tsv(class_file)
fitness = read_csv(fitness_file)

# Add missing features as NA
features = select(features, -N) %>% spread(domainId, locusId) %>%
  gather(domainId, locusId, -orgId)

# Combine data
dataset = features %>% inner_join(classes) %>% left_join(fitness)

# If a feature is missing, replace its value with the average
avg_fit = filter(dataset, !is.na(fit)) %>%
  group_by(domainId) %>%
  summarise(fit = mean(fit))

dataset = filter(dataset, is.na(fit)) %>% select(-fit) %>%
  inner_join(avg_fit) %>% rbind(filter(dataset, !is.na(fit)))

# Format data for Python scikit-learn
dataset = select(
    dataset, orgId, expName, metal, antibiotics, domainId, fit
  ) %>% spread(domainId, fit)

feature_names = colnames(
  select(dataset, -orgId, -expName, -metal, -antibiotics)
)

X_features = select(dataset, -orgId, -expName, -metal, -antibiotics)
y_metal = dataset$metal
y_antibiotics = dataset$antibiotics

# Write data files for Python scikit-learn
write(
  feature_names,
  "/home/johannes/proj/crse/results/2018-11-22/feba_feature_names.txt"
)
write_csv(
  X_features,
  "/home/johannes/proj/crse/results/2018-11-22/feba_X.csv",
  col_names=F
)
write(
  y_metal,
  "/home/johannes/proj/crse/results/2018-11-22/feba_y_metal.txt",
  ncolumns = 1
)
write(
  y_antibiotics,
  "/home/johannes/proj/crse/results/2018-11-22/feba_y_antibiotics.txt",
  ncolumns = 1
)
