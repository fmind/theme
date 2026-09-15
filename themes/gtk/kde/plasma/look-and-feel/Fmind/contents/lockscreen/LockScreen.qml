// https://invent.kde.org/plasma/kscreenlocker/-/tree/Plasma/5.27/greeter
import QtQuick 2.15
import "../components"

Rectangle {
    id: root
    objectName: "fmindLockScreen"
    color: "#ffffff"

    property date now: new Date()
    property string userName: typeof kscreenlocker_userName === "undefined" ? "" : kscreenlocker_userName
    property string errorMessage: ""
    property bool capsLockOn: false
    // Plasma supplies this object. Never substitute local authentication.
    readonly property var auth: typeof authenticator === "undefined" ? null : authenticator
    property bool viewVisible: false
    property bool locked: true
    property bool suspendToRamSupported: false
    property bool suspendToDiskSupported: false
    property bool awaitingInput: false
    property bool secretPrompt: true
    readonly property bool busy: !awaitingInput
    signal suspendToRam()
    signal suspendToDisk()
    signal clearPassword()
    onClearPassword: passwordInput.clear()
    onViewVisibleChanged: {
        if (viewVisible && auth) auth.tryUnlock();
        else {
            passwordInput.clear();
            awaitingInput = false;
            retry.stop();
            if (auth) auth.cancel();
        }
    }
    LayoutMirroring.enabled: Qt.application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    function submit() {
        if (!auth || !awaitingInput) return;
        awaitingInput = false;
        // Empty responses and multi-factor conversations belong to PAM's policy.
        auth.respond(passwordInput.text);
        passwordInput.clear();
    }
    Connections {
        target: root.auth
        function onPromptForSecret(message) {
            root.secretPrompt = true;
            root.awaitingInput = true;
            passwordInput.clear();
            passwordInput.forceActiveFocus();
        }
        function onPrompt(message) {
            root.secretPrompt = false;
            root.errorMessage = message;
            root.awaitingInput = true;
            passwordInput.clear();
            passwordInput.forceActiveFocus();
        }
        function onInfoMessage(message) { root.errorMessage = message; }
        function onErrorMessage(message) { root.errorMessage = message; }
        function onFailed() {
            passwordInput.clear();
            root.awaitingInput = false;
            root.errorMessage = qsTr("Unlocking failed. Try again.");
            retry.restart();
        }
        function onSucceeded() {
            passwordInput.clear();
            root.awaitingInput = false;
            retry.stop();
            // The native greeter independently checks this state before exiting.
            if (root.auth.unlocked) Qt.quit();
        }
    }
    Timer {
        id: retry
        interval: 1000
        onTriggered: if (root.viewVisible && root.auth) root.auth.tryUnlock()
    }

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
            textFormat: Text.PlainText
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
            border.color: passwordInput.activeFocus ? "#174ea6" : "#595d62"

            TextInput {
                id: passwordInput
                objectName: "lockPasswordInput"
                anchors.fill: parent
                anchors.leftMargin: 12
                anchors.rightMargin: 44
                verticalAlignment: TextInput.AlignVCenter
                echoMode: root.secretPrompt ? TextInput.Password : TextInput.Normal
                enabled: root.auth !== null && root.awaitingInput
                inputMethodHints: Qt.ImhHiddenText | Qt.ImhSensitiveData | Qt.ImhNoPredictiveText
                color: "#202124"
                font.family: "Google Sans"
                font.pixelSize: 15
                focus: true
                activeFocusOnTab: enabled
                Accessible.name: qsTr("Authentication response")
                onAccepted: root.submit()
            }

            SessionButton {
                id: unlockButton
                objectName: "lockUnlockButton"
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.margins: 4
                width: 36
                text: "➔"
                Accessible.name: qsTr("Unlock")
                enabled: passwordInput.enabled
                onClicked: root.submit()
            }
        }

        Text {
            id: errorText
            objectName: "lockError"
            width: parent.width
            visible: !root.auth || root.errorMessage !== "" || root.capsLockOn
            text: !root.auth ? qsTr("Authentication unavailable") : (root.capsLockOn ? qsTr("Caps Lock is on") : root.errorMessage)
            textFormat: Text.PlainText
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
