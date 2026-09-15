// https://develop.kde.org/docs/plasma/
import QtQuick 2.15

Rectangle {
    id: root
    objectName: "fmindLockScreen"
    color: "#ffffff"

    property date now: new Date()
    property string userName: "User"
    property string errorMessage: ""
    property bool capsLockOn: false
    property bool busy: false

    signal unlocked()

    Timer {
        interval: 1000
        repeat: true
        running: true
        onTriggered: root.now = new Date()
    }

    Column {
        id: centerBlock
        objectName: "lockContent"
        anchors.centerIn: parent
        width: Math.min(400, parent.width - 48)
        spacing: 20

        Text {
            id: clock
            objectName: "lockClock"
            width: parent.width
            text: Qt.formatTime(root.now, "hh:mm")
            color: "#202124"
            font.family: "Google Sans"
            font.pixelSize: 64
            font.weight: Font.Medium
            horizontalAlignment: Text.AlignHCenter
            Accessible.role: Accessible.StaticText
            Accessible.name: text
        }

        Text {
            id: dateLabel
            objectName: "lockDate"
            width: parent.width
            text: Qt.formatDate(root.now, Qt.DefaultLocaleLongDate)
            color: "#595d62"
            font.family: "Google Sans"
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            Accessible.role: Accessible.StaticText
            Accessible.name: text
        }

        Item { width: 1; height: 16 }

        Text {
            id: userLabel
            objectName: "lockUser"
            width: parent.width
            text: root.userName
            color: "#202124"
            font.family: "Google Sans"
            font.pixelSize: 20
            font.weight: Font.Medium
            horizontalAlignment: Text.AlignHCenter
            elide: Text.ElideRight
            Accessible.role: Accessible.StaticText
            Accessible.name: text
        }

        Rectangle {
            id: passwordBox
            objectName: "lockPasswordBox"
            width: parent.width
            height: 44
            radius: 4
            color: "#ffffff"
            border.width: passwordInput.activeFocus ? 2 : 1
            border.color: passwordInput.activeFocus ? "#174ea6" : "#9aa0a6"

            TextInput {
                id: passwordInput
                objectName: "lockPasswordInput"
                anchors.fill: parent
                anchors.leftMargin: 12
                anchors.rightMargin: 44
                verticalAlignment: TextInput.AlignVCenter
                echoMode: TextInput.Password
                inputMethodHints: Qt.ImhHiddenText | Qt.ImhSensitiveData | Qt.ImhNoPredictiveText
                color: "#202124"
                font.family: "Google Sans"
                font.pixelSize: 15
                focus: true
                onAccepted: {
                    if (text.length > 0) {
                        root.busy = true;
                        root.unlocked();
                    }
                }
            }

            Rectangle {
                id: unlockButton
                objectName: "lockUnlockButton"
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.margins: 4
                width: 36
                radius: 3
                color: unlockMouse.pressed ? "#174ea6" : (unlockMouse.containsMouse ? "#4285f4" : "#174ea6")

                Text {
                    anchors.centerIn: parent
                    text: "➔"
                    color: "#ffffff"
                    font.family: "Google Sans"
                    font.pixelSize: 16
                }

                MouseArea {
                    id: unlockMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (passwordInput.text.length > 0) {
                            root.busy = true;
                            root.unlocked();
                        }
                    }
                }
            }
        }

        Text {
            id: errorText
            objectName: "lockError"
            width: parent.width
            visible: root.errorMessage !== "" || root.capsLockOn
            text: root.capsLockOn ? qsTr("Caps Lock is on") : root.errorMessage
            color: "#a50e0e"
            font.family: "Google Sans"
            font.pixelSize: 14
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            Accessible.role: Accessible.AlertMessage
            Accessible.name: text
        }
    }
}
