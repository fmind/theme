# Javadoc

Fmind theme for [Javadoc](https://docs.oracle.com/en/java/javase/).

Format: [JDK stylesheet variables](https://github.com/openjdk/jdk/blob/master/src/jdk.javadoc/share/classes/jdk/javadoc/internal/doclets/formats/html/resources/stylesheet.css) · [javadoc --add-stylesheet](https://docs.oracle.com/en/java/javase/21/docs/specs/man/javadoc.html)

## Install

Pass `--add-stylesheet /path/to/javadoc/stylesheet.css` when generating documentation with JDK 21 or later. The file keeps Javadoc's default stylesheet and overrides its color and font variables. Do not use `--main-stylesheet`: it replaces the default stylesheet, including its layout. Older JDKs have no style variables. Where Javadoc offers a dark theme, that theme keeps its own colors.
