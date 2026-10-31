# Fmind for Eclipse

Files: [preferences](fmind.epf), [theme XML](fmind.xml).

Format: [Eclipse preference import](https://help.eclipse.org/latest/topic/org.eclipse.platform.doc.user/tasks/timpandexp.htm) · [JDT PreferenceConstants](https://github.com/eclipse-jdt/eclipse.jdt.ui/blob/master/org.eclipse.jdt.ui/ui/org/eclipse/jdt/ui/PreferenceConstants.java) · [Eclipse Color Theme keys](https://github.com/eclipse-color-theme/eclipse-color-theme/blob/master/com.github.eclipsecolortheme/src/com/github/eclipsecolortheme/ColorThemeKeys.java)

## Installation

Select the Light workbench theme, then File → Import → General → Preferences and choose `fmind.epf`; restart. Covers core editors, JDT, CDT, Ant, debug console and PyDev. If using Eclipse Color Theme or DevStyle, import `fmind.xml` in that plugin’s Color Theme panel and select Fmind. The XML retains its upstream [MIT license](LICENSE).
