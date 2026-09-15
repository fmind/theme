// https://github.com/sddm/sddm/blob/v0.21.0/docs/THEMING.md
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
Rectangle {
    id: root
    objectName: "fmindGreeter"
    width: 960
    height: 720
    color: "#ffffff"
    property bool busy: false
    property string message: ""
    property string powerAction: ""
    property date now: new Date()
    property bool showKeyboard: false
    onShowKeyboardChanged: if (!showKeyboard) scroll.contentY = 0
    LayoutMirroring.enabled: Qt.application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    function startLogin() {
        if (busy || user.editText.trim().length === 0 || session.currentIndex < 0 || session.currentIndex >= session.count)
            return;
        busy = true;
        message = "";
        login.forceActiveFocus();
        // Empty passwords are passed to SDDM; PAM owns authentication policy.
        sddm.login(user.editText.trim(), password.text, session.currentIndex);
        password.clear();
    }
    function requestPower(action) {
        if (busy || (action === "suspend" && !sddm.canSuspend) || (action === "reboot" && !sddm.canReboot) || (action === "powerOff" && !sddm.canPowerOff))
            return;
        if (["suspend", "reboot", "powerOff"].indexOf(action) < 0)
            return;
        powerAction = action;
        powerDialog.open();
    }
    function confirmPower() {
        const action = powerAction;
        powerDialog.close();
        if (busy) return;
        if (action === "suspend" && sddm.canSuspend) sddm.suspend();
        if (action === "reboot" && sddm.canReboot) sddm.reboot();
        if (action === "powerOff" && sddm.canPowerOff) sddm.powerOff();
        powerAction = "";
    }
    Timer { interval: 1000; repeat: true; running: true; onTriggered: root.now = new Date() }
    Connections {
        target: sddm
        ignoreUnknownSignals: true
        function onLoginFailed() {
            root.busy = false;
            root.message = qsTr("Sign-in failed. Check your username and password, then try again.");
            password.clear();
            password.forceActiveFocus();
        }
        function onLoginSucceeded() {
            password.clear();
            root.message = qsTr("Starting your session…");
        }
        function onInformationMessage(message) { root.message = message; }
    }
    Flickable {
        id: scroll
        objectName: "greeterScroll"
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: keyboardLoader.top
        contentWidth: width
        contentHeight: form.childrenRect.height + 48
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
        ColumnLayout {
            id: form
            objectName: "greeterForm"
            width: Math.min(420, Math.max(0, scroll.width - 48))
            x: (scroll.width - width) / 2
            y: 24
            spacing: 10
            FLabel { text: "Fmind"; font.pixelSize: 36; font.weight: Font.Medium; Layout.fillWidth: true }
            FLabel { text: Qt.formatDateTime(root.now, Qt.DefaultLocaleShortDate); color: "#595d62"; Layout.fillWidth: true }
            Loader {
                Layout.fillWidth: true
                active: config.showBattery === "true"
                source: config.batteryProvider === "plasma5" ? "Battery5.qml" : "Battery6.qml"
            }
            FLabel { text: qsTr("Sign in"); font.pixelSize: 24; Layout.topMargin: 12; Layout.fillWidth: true }
            FLabel { text: qsTr("Username"); Layout.fillWidth: true }
            FCombo {
                id: user
                objectName: "username"
                Layout.fillWidth: true
                editable: true
                model: userModel
                textRole: "name"
                currentIndex: userModel.lastIndex
                editText: userModel.lastUser
                enabled: !root.busy
                Accessible.name: qsTr("Username")
                onActivated: { password.clear(); password.forceActiveFocus(); }
                onAccepted: password.forceActiveFocus()
                Component.onCompleted: {
                    if (editText.length === 0) forceActiveFocus();
                    else password.forceActiveFocus();
                }
            }
            FLabel { text: qsTr("Password"); Layout.fillWidth: true }
            FField {
                id: password
                objectName: "password"
                Layout.fillWidth: true
                echoMode: TextInput.Password
                inputMethodHints: Qt.ImhHiddenText | Qt.ImhSensitiveData | Qt.ImhNoPredictiveText
                enabled: !root.busy
                Accessible.name: qsTr("Password")
                onAccepted: root.startLogin()
                onActiveFocusChanged: if (activeFocus && root.showKeyboard) scroll.contentY = Math.max(0, form.y + y - 48)
            }
            FLabel { objectName: "capsLockWarning"; visible: keyboard.capsLock; text: qsTr("Caps Lock is on"); color: "#934900"; Layout.fillWidth: true }
            FLabel { text: qsTr("Desktop session"); Layout.fillWidth: true }
            FCombo {
                id: session
                objectName: "session"
                Layout.fillWidth: true
                model: sessionModel
                textRole: "name"
                currentIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : (count > 0 ? 0 : -1)
                enabled: !root.busy && count > 0
                Accessible.name: qsTr("Desktop session")
            }
            FLabel { text: qsTr("Keyboard layout"); visible: keyboard.enabled && keyboard.layouts.length > 1; Layout.fillWidth: true }
            FCombo {
                objectName: "keyboardLayout"
                Layout.fillWidth: true
                visible: keyboard.enabled && count > 1
                model: keyboard.layouts
                textRole: "longName"
                currentIndex: keyboard.currentLayout
                onActivated: keyboard.currentLayout = currentIndex
                enabled: !root.busy
                Accessible.name: qsTr("Keyboard layout")
            }
            FLabel {
                objectName: "loginMessage"
                Layout.fillWidth: true
                visible: text.length > 0
                text: session.count === 0 ? qsTr("No desktop sessions are installed.") : root.message
                color: root.busy ? "#174ea6" : "#a50e0e"
                Accessible.role: Accessible.AlertMessage
                Accessible.name: text
            }
            FButton {
                id: login
                objectName: "loginButton"
                Layout.fillWidth: true
                primary: true
                text: root.busy ? qsTr("Signing in…") : qsTr("Sign in")
                enabled: !root.busy && user.editText.trim().length > 0 && session.currentIndex >= 0 && session.currentIndex < session.count
                onClicked: root.startLogin()
            }
            FButton {
                objectName: "keyboardButton"
                Layout.fillWidth: true
                text: root.showKeyboard ? qsTr("Hide on-screen keyboard") : qsTr("On-screen keyboard")
                enabled: !root.busy
                onClicked: { root.showKeyboard = !root.showKeyboard; if (root.showKeyboard) password.forceActiveFocus(); }
            }
            GridLayout {
                Layout.fillWidth: true
                columns: form.width < 340 ? 1 : 3
                columnSpacing: 8
                rowSpacing: 8
                FButton { objectName: "suspendButton"; text: qsTr("Sleep"); Layout.fillWidth: true; enabled: sddm.canSuspend && !root.busy; onClicked: root.requestPower("suspend") }
                FButton { objectName: "rebootButton"; text: qsTr("Restart"); Layout.fillWidth: true; enabled: sddm.canReboot && !root.busy; onClicked: root.requestPower("reboot") }
                FButton { objectName: "powerOffButton"; text: qsTr("Shut down"); Layout.fillWidth: true; enabled: sddm.canPowerOff && !root.busy; onClicked: root.requestPower("powerOff") }
            }
        }
    }
    Loader {
        id: keyboardLoader
        objectName: "virtualKeyboard"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        active: root.showKeyboard
        onLoaded: item.hidden.connect(function() { root.showKeyboard = false; })
        source: config.qtVersion === "5" ? "VirtualKeyboard.qml" : "VirtualKeyboard6.qml"
        height: item ? Math.min(item.implicitHeight, root.height * 0.45) : 0
    }
    Popup {
        id: powerDialog
        objectName: "powerDialog"
        anchors.centerIn: parent
        width: Math.min(400, root.width - 32)
        modal: true
        focus: true
        padding: 20
        closePolicy: Popup.CloseOnEscape
        onClosed: root.powerAction = ""
        background: Rectangle { color: "#ffffff"; border.color: "#9aa0a6"; radius: 8 }
        Overlay.modal: Rectangle { color: "#ffffff" }
        contentItem: ColumnLayout {
            spacing: 16
            FLabel { text: root.powerAction === "suspend" ? qsTr("Put this computer to sleep?") : root.powerAction === "reboot" ? qsTr("Restart this computer?") : qsTr("Shut down this computer?"); Layout.fillWidth: true }
            RowLayout {
                FButton { text: qsTr("Cancel"); onClicked: powerDialog.close() }
                FButton { objectName: "confirmPower"; text: qsTr("Confirm"); primary: true; onClicked: root.confirmPower() }
            }
        }
    }
}
