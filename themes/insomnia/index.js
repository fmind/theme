module.exports.themes = [
  {
    name: "fmind",
    displayName: "Fmind",
    theme: {
      background: {
        default: "#ffffff",
        // Insomnia also uses these as text colors (e.g. HTTP method labels), so they stay dark.
        success: "#0d652d",
        notice: "#934900",
        warning: "#934900",
        danger: "#a50e0e",
        surprise: "#681da8",
        info: "#00636d",
      },
      foreground: {
        default: "#202124",
        success: "#ffffff",
        notice: "#ffffff",
        warning: "#ffffff",
        danger: "#ffffff",
        surprise: "#ffffff",
        info: "#ffffff",
      },
      highlight: {
        default: "#595d62",
      },
      styles: {
        sidebar: {
          background: {
            default: "#f1f3f4",
          },
          foreground: {
            default: "#202124",
          },
          highlight: {
            default: "#174ea6",
          },
        },
        paneHeader: {
          background: {
            default: "#ffffff",
            success: "#0d652d",
            notice: "#934900",
            warning: "#934900",
            danger: "#a50e0e",
            surprise: "#681da8",
            info: "#00636d",
          },
          foreground: {
            default: "#202124",
          },
        },
      },
    },
  },
];
