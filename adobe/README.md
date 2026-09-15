# Fmind for Adobe

[Fmind.ase](Fmind.ase) is an Adobe Swatch Exchange palette with all 20 Fmind colors. It supplies document swatches, not an application UI theme. [swatches.json](swatches.json) is the readable color reference.

In Illustrator, open the Swatches panel’s library menu, choose **Other Library**, and select `Fmind.ase`. In InDesign, use **Load Swatches** and select the same file. Follow [Adobe’s swatch sharing instructions](https://helpx.adobe.com/ca/illustrator/desktop/manage-colors/use-swatches/share-swatches-between-applications.html) for your version.

The binary stores named RGB swatches in ASE 1.0 format. Offline checks decode every block and compare the names and RGB channels with the JSON reference. A current Adobe desktop import remains unverified. The format was checked against [Krita’s ASE reader](https://github.com/KDE/krita/blob/master/libs/pigment/resources/KoColorSet.cpp).
