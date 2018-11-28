options(width=150)

# Load libraries
library(tidyverse)

# Define infiles
svm_file = "/home/johannes/proj/crse/results/2018-11-28/fitml_svm_output.tab"

# Load data
svm = read_tsv(svm_file)

# Calculate mean and sd accuracies
svm_avg = svm %>% group_by(classifier, split, C, gamma) %>% summarise(
    train_avg = mean(train), train_sd = sd(train),
    test_avg = mean(test), test_sd = sd(test),
    cross_avg = mean(cross), cross_sd = sd(cross)
  )

# Reshape data
svm_avg = gather(svm_avg, variable, value, -classifier, -split, -gamma, -C) %>%
  mutate(
    dataset = unlist(lapply(str_split(variable, "_"), "[[", 1)),
    variable = unlist(lapply(str_split(variable, "_"), "[[", 2))
  ) %>% spread(variable, value) %>% mutate(cv = sd/avg*100) %>%
  mutate(
    dataset = factor(dataset, levels=c("train", "test", "cross"))
  ) %>% filter(split %in% c(0.3,0.5,0.7))

# Plot the mean accuracies as a heatmap
gp = ggplot(svm_avg, aes(x=log10(C), y=log10(gamma), fill=avg, alpha=cv))
gp = gp + geom_tile()
gp = gp + theme_bw()
gp = gp + facet_grid(split ~ classifier + dataset)
gp = gp + scale_fill_distiller(palette="PuOr", direction=1)
gp = gp + theme(strip.background = element_blank())
gp = gp + coord_fixed()
gp = gp + scale_alpha_continuous(range=c(1,0.1))
gp = gp + scale_y_continuous(breaks=c(-4,-2,0,2))
gp = gp + scale_x_continuous(breaks=c(-2,0,2))
gp

ggsave(
  "/home/johannes/proj/crse/art/2018-11-28/fitml_svm_output.pdf", gp,
  height = 150/25.4, width=270/25.4
)
