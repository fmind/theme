// https://doc.qt.io/qt-5/qml-qtquick-item.html
import QtQuick 2.15

Rectangle {
    id: root
    property string text
    signal clicked()
    activeFocusOnTab: enabled
    radius: 4
    color: mouse.pressed ? "#d2e3fc" : (mouse.containsMouse ? "#f1f3f4" : "#ffffff")
    border.width: activeFocus ? 2 : 1
    border.color: activeFocus ? "#174ea6" : "#595d62"
    Accessible.role: Accessible.Button
    Accessible.name: text
    Accessible.onPressAction: if (enabled) clicked()
    Keys.onSpacePressed: if (enabled && !event.isAutoRepeat) clicked()
    Keys.onReturnPressed: if (enabled && !event.isAutoRepeat) clicked()
    Keys.onEnterPressed: if (enabled && !event.isAutoRepeat) clicked()
    Text {
        objectName: "sessionButtonLabel"
        anchors.fill: parent
        anchors.margins: 5
        text: root.text
        textFormat: Text.PlainText
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: root.enabled ? "#202124" : "#595d62"
        font.family: "Google Sans"
        font.pixelSize: 14
    }
    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: { root.forceActiveFocus(); root.clicked(); }
    }
}
