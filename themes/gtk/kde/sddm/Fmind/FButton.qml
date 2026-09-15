// https://doc.qt.io/qt-6/qtquickcontrols-customize.html
import QtQuick 2.15
import QtQuick.Controls 2.15
Button {
    id: control
    property bool primary: false
    implicitHeight: 44
    implicitWidth: Math.max(100, label.implicitWidth + 32)
    font.family: "Google Sans"
    font.pixelSize: 16
    hoverEnabled: true
    contentItem: Text {
        id: label
        text: control.text
        textFormat: Text.PlainText
        font: control.font
        color: control.enabled ? "#202124" : "#595d62"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    background: Rectangle {
        radius: 6
        color: control.down || control.visualFocus || control.primary ? "#d2e3fc" : "#ffffff"
        border.color: control.visualFocus || control.hovered ? "#174ea6" : "#9aa0a6"
        border.width: control.visualFocus ? 2 : 1
    }
}
