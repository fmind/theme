// https://doc.qt.io/qt-6/qml-qtquick-virtualkeyboard-inputpanel.html
import QtQuick 2.15
import QtQuick.VirtualKeyboard
import QtQuick.VirtualKeyboard.Settings
Item {
    id: root
    property bool activated: false
    signal hidden()
    property real maximumHeight: parent ? parent.parent.height * 0.45 : 320
    implicitHeight: panel.implicitHeight
    InputPanel {
        id: panel
        objectName: "inputPanel"
        onActiveChanged: {
            if (active) root.activated = true;
            else if (root.activated) root.hidden();
        }
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        width: Math.min(parent.width, parent.maximumHeight * 3)
    }
    Component.onCompleted: {
        VirtualKeyboardSettings.styleName = "Fmind6";
        Qt.inputMethod.show();
    }
}
