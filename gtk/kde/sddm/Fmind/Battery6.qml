// https://invent.kde.org/plasma/plasma-workspace/-/blob/v6.4.5/lookandfeel/components/Battery.qml
import QtQuick 2.15
import org.kde.plasma.private.battery
FLabel {
    objectName: "batteryStatus"
    visible: battery.hasInternalBatteries
    text: qsTr("Battery: %1%").arg(Math.round(battery.percent)) + (battery.pluggedIn ? qsTr(" · Connected to power") : "")
    color: battery.percent < 20 ? "#a50e0e" : "#595d62"
    BatteryControlModel { id: battery }
}
