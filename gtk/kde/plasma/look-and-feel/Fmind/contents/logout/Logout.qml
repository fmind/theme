// https://develop.kde.org/docs/plasma/
import QtQuick 2.15

Rectangle {
    id: root
    objectName: "fmindLogout"
    color: "#ffffff"

    property int timeout: 30
    property int remaining: timeout
    property bool timerActive: true

    signal suspendRequested()
    signal restartRequested()
    signal shutdownRequested()
    signal logoutRequested()
    signal cancelRequested()

    Timer {
        interval: 1000
        repeat: true
        running: root.timerActive && root.remaining > 0
        onTriggered: {
            root.remaining -= 1;
            if (root.remaining === 0) {
                root.logoutRequested();
            }
        }
    }

    Column {
        id: dialogCard
        objectName: "logoutCard"
        anchors.centerIn: parent
        width: Math.min(520, parent.width - 48)
        spacing: 24

        Text {
            id: title
            objectName: "logoutTitle"
            width: parent.width
            text: qsTr("Leave Session")
            color: "#202124"
            font.family: "Google Sans"
            font.pixelSize: 24
            font.weight: Font.Medium
            horizontalAlignment: Text.AlignHCenter
            Accessible.role: Accessible.StaticText
            Accessible.name: text
        }

        Text {
            id: timerLabel
            objectName: "logoutTimer"
            width: parent.width
            text: qsTr("Automatic log out in %1 seconds…").arg(root.remaining)
            color: "#595d62"
            font.family: "Google Sans"
            font.pixelSize: 15
            horizontalAlignment: Text.AlignHCenter
            Accessible.role: Accessible.StaticText
            Accessible.name: text
        }

        Flow {
            id: actionGrid
            objectName: "logoutActions"
            width: parent.width
            spacing: 12

            Repeater {
                model: [
                    { name: qsTr("Suspend"), role: "suspend", icon: "⏾", destructive: false },
                    { name: qsTr("Restart"), role: "restart", icon: "↺", destructive: false },
                    { name: qsTr("Shut Down"), role: "shutdown", icon: "⏻", destructive: true },
                    { name: qsTr("Log Out"), role: "logout", icon: "⇥", destructive: false }
                ]

                Rectangle {
                    width: (actionGrid.width - 36) / 4
                    height: 80
                    radius: 6
                    color: btnMouse.pressed ? (modelData.destructive ? "#fad2cf" : "#d2e3fc") : (btnMouse.containsMouse ? (modelData.destructive ? "#fad2cf" : "#f1f3f4") : "#ffffff")
                    border.width: 1
                    border.color: btnMouse.containsMouse && modelData.destructive ? "#a50e0e" : (btnMouse.containsMouse ? "#174ea6" : "#9aa0a6")

                    Column {
                        anchors.centerIn: parent
                        spacing: 6

                        Text {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: modelData.icon
                            color: btnMouse.containsMouse && modelData.destructive ? "#a50e0e" : (btnMouse.containsMouse ? "#174ea6" : "#202124")
                            font.family: "Google Sans"
                            font.pixelSize: 22
                        }

                        Text {
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: modelData.name
                            color: btnMouse.containsMouse && modelData.destructive ? "#a50e0e" : (btnMouse.containsMouse ? "#174ea6" : "#202124")
                            font.family: "Google Sans"
                            font.pixelSize: 13
                            font.weight: Font.Medium
                        }
                    }

                    MouseArea {
                        id: btnMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            root.timerActive = false;
                            if (modelData.role === "suspend") root.suspendRequested();
                            else if (modelData.role === "restart") root.restartRequested();
                            else if (modelData.role === "shutdown") root.shutdownRequested();
                            else if (modelData.role === "logout") root.logoutRequested();
                        }
                    }
                }
            }
        }

        Rectangle {
            id: cancelButton
            objectName: "logoutCancel"
            anchors.horizontalCenter: parent.horizontalCenter
            width: 120
            height: 36
            radius: 4
            color: cancelMouse.pressed ? "#d2e3fc" : (cancelMouse.containsMouse ? "#f1f3f4" : "#ffffff")
            border.width: 1
            border.color: cancelMouse.containsMouse ? "#174ea6" : "#9aa0a6"

            Text {
                anchors.centerIn: parent
                text: qsTr("Cancel")
                color: "#202124"
                font.family: "Google Sans"
                font.pixelSize: 14
                font.weight: Font.Medium
            }

            MouseArea {
                id: cancelMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: root.cancelRequested()
            }
        }
    }
}
