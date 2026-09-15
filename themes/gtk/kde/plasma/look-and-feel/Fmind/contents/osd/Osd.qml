// https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/5.27/shell/osd.cpp
import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: root
    objectName: "fmindOsd"
    width: 260
    height: 72
    visible: false
    flags: Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    color: "#ffffff"
    x: (Screen.width - width) / 2
    y: Screen.height - height - 48

    // The host writes these names for both progress and text notifications.
    property string icon: ""
    property var osdValue: 0
    property int osdMaxValue: 100
    property string osdAdditionalText: ""
    property bool showingProgress: false
    property int timeout: 2000
    readonly property string label: !showingProgress ? String(osdValue)
        : osdAdditionalText !== "" ? osdAdditionalText
        : icon.indexOf("brightness") !== -1 ? qsTr("Brightness") : qsTr("Volume")

    Rectangle {
        anchors.fill: parent
        color: "#ffffff"
        border.width: 1
        border.color: "#595d62"
    }

    Column {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        Row {
            width: parent.width
            spacing: 8

            Text {
                id: titleText
                objectName: "osdTitle"
                width: parent.width - valueText.width - 8
                text: root.label
                textFormat: Text.PlainText
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
                text: Math.round(Number(root.osdValue)) + "%"
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
            border.color: "#595d62"

            Rectangle {
                id: progressFill
                objectName: "osdProgressFill"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: Math.max(0, Math.min(parent.width, parent.width * (root.osdValue / Math.max(1, root.osdMaxValue))))
                radius: 3
                color: "#174ea6"
            }
        }
    }
}
