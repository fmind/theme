// https://doc.qt.io/qt-6/qtquickcontrols-customize.html#customizing-combobox
import QtQuick 2.15
import QtQuick.Controls 2.15
ComboBox {
    id: control
    implicitHeight: 44
    font.family: "Google Sans"
    font.pixelSize: 16
    leftPadding: 12
    rightPadding: 32
    contentItem: TextInput {
        focus: control.editable
        onTextEdited: control.editText = text
        text: control.editable ? control.editText : control.displayText
        font: control.font
        color: control.enabled ? "#202124" : "#595d62"
        selectionColor: "#d2e3fc"
        selectedTextColor: "#202124"
        inputMethodHints: Qt.ImhSensitiveData | Qt.ImhNoPredictiveText
        readOnly: !control.editable
        selectByMouse: control.editable
        verticalAlignment: TextInput.AlignVCenter
        clip: true
    }
    indicator: Text {
        x: control.width - width - 12
        anchors.verticalCenter: parent.verticalCenter
        text: "⌄"
        font: control.font
        color: "#595d62"
    }
    background: Rectangle {
        color: "#ffffff"
        radius: 6
        border.color: control.activeFocus ? "#174ea6" : "#9aa0a6"
        border.width: control.activeFocus ? 2 : 1
    }
    delegate: ItemDelegate {
        width: control.width
        implicitHeight: 44
        text: control.textAt(index)
        highlighted: control.highlightedIndex === index
        contentItem: Text {
            text: parent.text
            textFormat: Text.PlainText
            font: control.font
            color: "#202124"
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
        background: Rectangle { color: parent.highlighted ? "#d2e3fc" : "#ffffff" }
    }
    popup: Popup {
        y: control.height
        width: control.width
        implicitHeight: Math.min(contentItem.implicitHeight + 2, 220)
        padding: 1
        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            ScrollIndicator.vertical: ScrollIndicator {}
        }
        background: Rectangle { color: "#ffffff"; border.color: "#9aa0a6"; radius: 6 }
    }
}
