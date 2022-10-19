library(ggplot2)

map_data <- 
	read.table(file = commandArgs(TRUE)[1],
				sep = '\t')

map_data$V2 <- map_data$V1 + 30

out_plot <- 
	ggplot(map_data) +
		geom_segment(aes(
			x = V1, 
			xend = V2, 
			y = 1, 
			yend = 1),
			position = position_jitter(height = 1),
			alpha = 0.5) +
		ylim(c(1,5)) +
		theme_bw() + 
		geom_blank()

ggsave(out_plot, device = 'pdf')