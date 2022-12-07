setwd(this.path::here())
rm(list = ls())

library(dplyr)
library(ggbreak)
library(ggplot2)
library(grid)
library(gridExtra)
library(rjson)

options(scipen=100000)

# Global memory plots ----

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

# Global runtime plots ----

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

# Detailed memory plot ----

results_files <- list.files("./results", pattern = "mprof*", full.names = TRUE)

detailed_memory_df = data.frame(matrix(NA, ncol=4, nrow=0))
colnames(detailed_memory_df) <- c("algorithm", "sequence_length", "memory_usage", "timepoint")

for (i in seq(length(results_files))){
  newdf <- read.csv(results_files[i], skip=1, sep=" ", header = FALSE)[-1]
  colnames(newdf) <- c("memory_usage", "timepoint")
  newdf$timepoint <- newdf$timepoint - newdf$timepoin[1]
  newdf <- cbind(newdf, list(algorithm = gsub(".*_([^_]*)_([^.]*).*", "\\1",
                                              results_files[i]),
                             sequence_length = as.numeric(
                               gsub(".*_([^_]*)_([^.]*).*", "\\2",
                                    results_files[i]))))
  detailed_memory_df <- rbind(detailed_memory_df, newdf)
}

# set timepoints to seconds
detailed_memory_df$timepoint <- detailed_memory_df$timepoint / 100

detailed_memory_df %>%
  filter(sequence_length <= 1000) %>%
  { ggplot(., aes(x = timepoint, y = memory_usage,
                group = algorithm, color = algorithm)) +
      geom_line() +
      theme_bw() +
      facet_wrap(~sequence_length, scales = "free", strip.position="right") +
      theme(axis.title.x = element_blank(),
            axis.title.y = element_blank())
  } %>%
  { . ->> detailed_memory_plot }

detailed_memory_df %>%
  filter(sequence_length == 10000) %>%
  { ggplot(., aes(x = timepoint, y = memory_usage,
                group = algorithm, color = algorithm)) +
      geom_line() +
      scale_x_cut(breaks = c(3.9), which = c(1), scales = 2) +
      theme_bw() +
      facet_grid("10000") +
      theme(legend.position = "none",
            axis.title.x = element_blank(),
            axis.title.y = element_blank())
  } %>%
  { . ->> detailed_memory_plot_10000 }

detailed_memory_df %>%
  filter(sequence_length == 100000) %>%
  { ggplot(., aes(x = timepoint, y = memory_usage,
                  group = algorithm, color = algorithm)) +
      geom_line() +
      scale_x_cut(breaks = c(14), which = c(1), scales = 2) +
      scale_color_manual(values = c("#7CAE00", "#00BFC4", "#C77CFF")) +
      theme_bw() +
      facet_grid("100000") +
      theme(legend.position = "none",
            axis.title.x = element_blank(),
            axis.title.y = element_blank())
  } %>%
  { . ->> detailed_memory_plot_100000 }

legend <- get_legend(
  detailed_memory_plot + theme(legend.box.margin = margin(0, 0, 0, 12))
)

y.grob <- textGrob("Memory usage (in MiB)", rot=90)
x.grob <- textGrob("Time (in seconds)")

bottom_plot <- detailed_memory_plot_10000 + detailed_memory_plot_100000
plots <- plot_grid(detailed_memory_plot + theme(legend.position="none"), bottom_plot, ncol = 1)
plots <- plot_grid(plots, legend, rel_widths = c(3, .4))

g <- grid.arrange(arrangeGrob(plots, left = y.grob, bottom = x.grob))

ggsave(filename = "results/detailed_memory_plot.svg", g)
