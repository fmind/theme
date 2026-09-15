// https://develop.kde.org/docs/plasma/
import QtQuick 2.15

Rectangle {
    id: root
    objectName: "fmindOsd"
    width: 260
    height: 72
    radius: 8
    color: "#ffffff"
    border.width: 1
    border.color: "#9aa0a6"

    property string iconName: "audio-volume-high"
    property string iconText: "🔊"
    property string label: qsTr("Volume")
    property int osdValue: 50
    property int osdMax: 100
    property bool showingProgress: true

    Column {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        Row {
            width: parent.width
            spacing: 8

            Text {
                id: glyph
                objectName: "osdIcon"
                text: root.iconText
                color: "#202124"
                font.family: "Google Sans"
                font.pixelSize: 18
                verticalAlignment: Text.AlignVCenter
            }

            Text {
                id: titleText
                objectName: "osdTitle"
                width: parent.width - glyph.width - valueText.width - 16
                text: root.label
                color: "#202124"
                font.family: "Google Sans"
                font.pixelSize: 14
                font.weight: Font.Medium
                elide: Text.ElideRight
                verticalAlignment: Text.AlignVCenter
            }

            Text {
                id: valueText
                objectName: "osdValueText"
                visible: root.showingProgress
                text: Math.round((root.osdValue / Math.max(1, root.osdMax)) * 100) + "%"
                color: "#595d62"
                font.family: "Google Sans"
                font.pixelSize: 13
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: progressBar
            objectName: "osdProgress"
            visible: root.showingProgress
            width: parent.width
            height: 6
            radius: 3
            color: "#f1f3f4"
            border.width: 1
            border.color: "#9aa0a6"

            Rectangle {
                id: progressFill
                objectName: "osdProgressFill"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: Math.max(0, Math.min(parent.width, parent.width * (root.osdValue / Math.max(1, root.osdMax))))
                radius: 3
                color: "#174ea6"
            }
        }
    }
}
