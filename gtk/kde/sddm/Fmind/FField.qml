// https://doc.qt.io/qt-6/qml-qtquick-controls-textfield.html
import QtQuick 2.15
import QtQuick.Controls 2.15
TextField {
    id: control
    implicitHeight: 44
    leftPadding: 12
    rightPadding: 12
    font.family: "Google Sans"
    font.pixelSize: 18
    color: enabled ? "#202124" : "#595d62"
    placeholderTextColor: "#595d62"
    selectionColor: "#d2e3fc"
    selectedTextColor: "#202124"
    selectByMouse: true
    background: Rectangle {
        radius: 6
        color: "#ffffff"
        border.color: control.activeFocus ? "#174ea6" : "#9aa0a6"
        border.width: control.activeFocus ? 2 : 1
    }
}
