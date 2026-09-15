// https://invent.kde.org/plasma/plasma-workspace/-/blob/Plasma/5.27/logout-greeter/shutdowndlg.cpp
import QtQuick 2.15
import "../components"

Rectangle {
    id: root
    objectName: "fmindLogout"
    color: "#ffffff"
    property color backgroundColor: "#ffffff"
    property int timeout: 30
    property int remaining: timeout
    property bool resolved: false
    readonly property bool mayShutdown: typeof maysd !== "undefined" && maysd
    readonly property bool mayLogout: typeof canLogout !== "undefined" && canLogout
    readonly property bool maySuspend: typeof spdMethods !== "undefined" && spdMethods.SuspendState
    readonly property string requestedAction: {
        if (typeof sdtype === "undefined" || typeof ShutdownType === "undefined") return "";
        if (sdtype === ShutdownType.ShutdownTypeReboot) return "restart";
        if (sdtype === ShutdownType.ShutdownTypeHalt) return "shutdown";
        if (sdtype === ShutdownType.ShutdownTypeLogout) return "logout";
        return "";
    }
    readonly property bool timerActive: !resolved && remaining > 0 && allowed(requestedAction)
    signal suspendRequested(int method)
    signal rebootRequested()
    signal rebootRequested2(int option)
    signal haltRequested()
    signal logoutRequested()
    signal cancelRequested()
    signal lockScreenRequested()
    LayoutMirroring.enabled: Qt.application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true
    focus: true
    Keys.onEscapePressed: cancel()

    function allowed(action) {
        if (action === "restart" || action === "shutdown") return mayShutdown;
        if (action === "logout") return mayLogout;
        if (action === "suspend") return maySuspend;
        return false;
    }
    function request(action) {
        if (resolved || !allowed(action)) return;
        resolved = true;
        if (action === "restart") rebootRequested();
        else if (action === "shutdown") haltRequested();
        else if (action === "suspend") suspendRequested(2);
        else if (action === "logout") logoutRequested();
    }
    function cancel() {
        if (resolved) return;
        resolved = true;
        cancelRequested();
    }
    Timer {
        interval: 1000
        repeat: true
        running: root.timerActive
        onTriggered: {
            root.remaining -= 1;
            if (root.remaining === 0) root.request(root.requestedAction);
        }
    }
    Column {
        anchors.centerIn: parent
        width: Math.min(520, parent.width - 48)
        spacing: 24
        Text {
            width: parent.width
            text: qsTr("Leave Session")
            color: "#202124"
            font.family: "Google Sans"
            font.pixelSize: 24
            horizontalAlignment: Text.AlignHCenter
        }
        Text {
            width: parent.width
            visible: root.timerActive
            text: root.requestedAction === "restart" ? qsTr("Restarting in %1 seconds…").arg(root.remaining)
                : root.requestedAction === "shutdown" ? qsTr("Shutting down in %1 seconds…").arg(root.remaining)
                : qsTr("Logging out in %1 seconds…").arg(root.remaining)
            color: "#595d62"
            font.family: "Google Sans"
            font.pixelSize: 15
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }
        Flow {
            id: actions
            width: parent.width
            spacing: 12
            Repeater {
                model: [
                    { name: qsTr("Suspend"), role: "suspend" },
                    { name: qsTr("Restart"), role: "restart" },
                    { name: qsTr("Shut Down"), role: "shutdown" },
                    { name: qsTr("Log Out"), role: "logout" }
                ]
                SessionButton {
                    objectName: "logout-" + modelData.role
                    width: (actions.width - 12) / 2
                    height: 48
                    text: modelData.name
                    enabled: !root.resolved && root.allowed(modelData.role)
                    onClicked: root.request(modelData.role)
                }
            }
        }
        SessionButton {
            objectName: "logout-cancel"
            anchors.horizontalCenter: parent.horizontalCenter
            width: 120
            height: 40
            text: qsTr("Cancel")
            enabled: !root.resolved
            focus: true
            onClicked: root.cancel()
        }
    }
}
