# Fmind theme for ggplot2
theme_fmind <- function() {
  ggplot2::theme_minimal(base_family = "Google Sans") +
    ggplot2::theme(
      plot.background = ggplot2::element_rect(fill = "#ffffff", color = NA),
      panel.background = ggplot2::element_rect(fill = "#ffffff", color = NA),
      panel.grid.major = ggplot2::element_line(color = "#f1f3f4"),
      panel.grid.minor = ggplot2::element_blank(),
      text = ggplot2::element_text(color = "#202124"),
      axis.text = ggplot2::element_text(color = "#595d62"),
      axis.title = ggplot2::element_text(color = "#202124", face = "bold"),
      plot.title = ggplot2::element_text(color = "#174ea6", face = "bold")
    )
}
