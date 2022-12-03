setwd(this.path::here())
rm(list = ls())

library(ggplot2)
library(ggbreak)

results_files <- list.files("./results", pattern = "mprof*", full.names = TRUE)

memory_df = data.frame(matrix(NA, ncol = 3, nrow = 10))
colnames(memory_df) <- c("algorithm", "sequence_length", "memory_usage")

for (i in seq(length(results_files))){
  memory_df[i,] <- list(gsub(".*_([^_]*)_([^.]*).*", "\\1", results_files[i]),
                        gsub(".*_([^_]*)_([^.]*).*", "\\2", results_files[i]),
                        max(read.csv(results_files[i], skip=1, sep=" ")[2]))
}

memory_plot <- ggplot(memory_df, aes(x = sequence_length, y = memory_usage,
                                     group = algorithm, color = algorithm,
                                     shape = algorithm)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  ylim(60, 2000) +
  scale_y_cut(breaks = c(75, 200), which = 3, scales = 2) +
  xlab("Length of the original sequence") +
  ylab("Memory usage (in MiB)") +
  theme_bw()

ggsave("results/memory_plot.svg", memory_plot)

library(rjson)

runtimes_json <- fromJSON(file = "results/runtimes.json")

runtimes_df = data.frame(matrix(NA, ncol=3, nrow=0))
colnames(runtimes_df) <- c("algorithm", "sequence_length", "runtime")

for (seqlen in names(runtimes_json)){
  for (algo in names(runtimes_json[[seqlen]])){
    runtimes_df <- rbind(runtimes_df,
                         do.call(data.frame, setNames(list(algo,
                                                           as.numeric(seqlen),
                                                           as.numeric(runtimes_json[[seqlen]][[algo]][["mean"]])),
                                                      names(runtimes_df))))
  }
}

runtime_plot <- ggplot(runtimes_df, aes(x = sequence_length, y = runtime,
                                        group = algorithm, color = algorithm,
                                        shape = algorithm)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_y_continuous(trans = 'log10') +
  scale_x_cut(breaks = c(120, 1300, 120000), which = c(1, 3), scales = 2) +
  scale_x_continuous(limits = c(0, 1200000), breaks = c(10, 100, 1000, 10000, 100000, 1000000)) +
  xlab("Length of the original sequence") +
  ylab("Runtime (in seconds, log-scaled)") +
  theme_bw() +
  theme(legend.position = "top")

ggsave("results/runtime_plot.svg", runtime_plot)
