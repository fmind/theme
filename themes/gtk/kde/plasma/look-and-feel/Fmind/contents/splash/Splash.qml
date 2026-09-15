// https://develop.kde.org/docs/plasma/
import QtQuick 2.15

Rectangle {
    id: root
    objectName: "fmindSplash"
    color: "#ffffff"

    // KSplash owns this counter; its final value differs across Plasma releases.
    property int stage: 0
    readonly property int activityIndex: Math.max(0, stage) % 5

    Column {
        id: content
        objectName: "splashContent"
        anchors.centerIn: parent
        width: Math.max(0, Math.min(420, parent.width - 48))
        spacing: root.height < 240 ? 18 : 24

        Text {
            objectName: "splashTitle"
            width: parent.width
            text: "Fmind"
            color: "#202124"
            font.family: "Google Sans"
            font.pixelSize: root.height < 240 ? 48 : 64
            font.weight: Font.Medium
            fontSizeMode: Text.Fit
            minimumPixelSize: 24
            horizontalAlignment: Text.AlignHCenter
            Accessible.role: Accessible.StaticText
            Accessible.name: text
        }

        Text {
            objectName: "splashStatus"
            width: parent.width
            text: qsTr("Starting Plasma…")
            color: "#595d62"
            font.family: "Google Sans"
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            Accessible.role: Accessible.StaticText
            Accessible.name: text
        }

        Row {
            objectName: "splashActivity"
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 12
            Accessible.ignored: true

            Repeater {
                model: 5
                Rectangle {
                    objectName: "activityDot" + index
                    width: 10
                    height: 10
                    radius: 5
                    color: root.activityIndex === index ? "#174ea6" : "#ffffff"
                    border.width: 1
                    border.color: root.activityIndex === index ? "#174ea6" : "#9aa0a6"
                }
            }
        }
    }
}
