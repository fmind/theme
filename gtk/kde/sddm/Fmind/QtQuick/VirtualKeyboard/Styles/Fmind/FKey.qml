// https://doc.qt.io/qt-6/qml-qtquick-virtualkeyboard-styles-keypanel.html
import QtQuick 2.15
import QtQuick.VirtualKeyboard.Styles 2.4
KeyPanel {
    id: panel
    property string label: control.displayText
    Rectangle {
        anchors.fill: parent
        anchors.margins: Math.max(1, parent.height * 0.04)
        color: panel.control.pressed ? "#d2e3fc" : "#ffffff"
        border.color: "#9aa0a6"
        radius: 4
        Text {
            anchors.fill: parent
            anchors.margins: 2
            text: panel.label
            textFormat: Text.PlainText
            font.family: "Google Sans"
            font.pixelSize: Math.max(12, Math.min(24, parent.height * 0.4))
            minimumPixelSize: 9
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: panel.control.enabled ? "#202124" : "#595d62"
        }
    }
}
