// https://invent.kde.org/plasma/plasma-workspace/-/tree/Plasma/5.27/lookandfeel
import QtQuick 2.15
import org.kde.plasma.core 2.0 as PlasmaCore
FLabel {
    objectName: "batteryStatus"
    id: root
    property var battery: source.data["Battery"] || ({})
    visible: battery["Has Battery"] === true
    text: qsTr("Battery: %1%").arg(Math.round(battery["Percent"] || 0)) + ((source.data["AC Adapter"] || {})["Plugged in"] ? qsTr(" · Connected to power") : "")
    color: (battery["Percent"] || 0) < 20 ? "#a50e0e" : "#595d62"
    PlasmaCore.DataSource {
        id: source
        engine: "powermanagement"
        connectedSources: ["Battery", "AC Adapter"]
    }
}
