/* https://st.suckless.org/ */
/* Replace colorname and the four default color indices in config.h. */
static const char *colorname[] = {
    "#202124",
    "#a50e0e",
    "#0d652d",
    "#934900",
    "#174ea6",
    "#681da8",
    "#00636d",
    "#202124",
    "#595d62",
    "#a50e0e",
    "#0d652d",
    "#934900",
    "#174ea6",
    "#681da8",
    "#00636d",
    "#202124",
    /* Leave 16..255 to st's native extended palette. */
    [256] = "#174ea6",
    [257] = "#ffffff",
    [258] = "#202124",
    [259] = "#ffffff",
};
unsigned int defaultfg = 258;
unsigned int defaultbg = 259;
unsigned int defaultcs = 256;
static unsigned int defaultrcs = 257;
