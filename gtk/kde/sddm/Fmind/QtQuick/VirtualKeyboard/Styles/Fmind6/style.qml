// https://doc.qt.io/qt-6/qml-qtquick-virtualkeyboard-styles-keyboardstyle.html
import QtQuick 2.15
import QtQuick.VirtualKeyboard
import QtQuick.VirtualKeyboard.Styles
KeyboardStyle {
    id: style
    keyboardDesignWidth: 960
    keyboardDesignHeight: 320
    keyboardRelativeLeftMargin: 0.01
    keyboardRelativeRightMargin: 0.01
    keyboardRelativeTopMargin: 0.02
    keyboardRelativeBottomMargin: 0.02
    keyboardBackground: Rectangle { color: "#ffffff"; border.color: "#9aa0a6" }
    keyPanel: FKey {}
    backspaceKeyPanel: FKey { label: "⌫" }
    languageKeyPanel: FKey { label: qsTr("Lang") }
    enterKeyPanel: FKey { label: "↵" }
    hideKeyPanel: FKey { label: "⌄" }
    shiftKeyPanel: FKey { label: control.uppercased ? "⇧ •" : "⇧" }
    spaceKeyPanel: FKey { label: qsTr("Space") }
    symbolKeyPanel: FKey { label: control.displayText }
    modeKeyPanel: FKey {}
    handwritingKeyPanel: FKey { label: "✎" }
    // No magnified character popup: the login screen handles sensitive input.
    alternateKeysListItemWidth: 48 * scaleHint
    alternateKeysListItemHeight: 60 * scaleHint
    alternateKeysListDelegate: Text {
        width: style.alternateKeysListItemWidth
        height: style.alternateKeysListItemHeight
        text: model.text
        textFormat: Text.PlainText
        font.family: "Google Sans"
        font.pixelSize: 24 * style.scaleHint
        color: "#202124"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
    alternateKeysListBackground: Rectangle { color: "#ffffff"; border.color: "#9aa0a6" }
    alternateKeysListHighlight: Rectangle { color: "#d2e3fc" }
    selectionListHeight: 44 * scaleHint
    selectionListDelegate: SelectionListItem {
        width: word.implicitWidth + 24 * style.scaleHint
        height: style.selectionListHeight
        Text {
            id: word
            anchors.centerIn: parent
            text: display
            textFormat: Text.PlainText
            font.family: "Google Sans"
            font.pixelSize: 20 * style.scaleHint
            color: "#202124"
        }
    }
    selectionListBackground: Rectangle { color: "#ffffff"; border.color: "#9aa0a6" }
    selectionListHighlight: Rectangle { color: "#d2e3fc" }
    popupListDelegate: selectionListDelegate
    popupListBackground: Rectangle { color: "#ffffff"; border.color: "#9aa0a6" }
    popupListHighlight: Rectangle { color: "#d2e3fc" }
    navigationHighlight: Rectangle { color: "transparent"; border.color: "#174ea6"; border.width: 2 }
    fullScreenInputContainerBackground: Rectangle { color: "#ffffff" }
    fullScreenInputBackground: Rectangle { color: "#ffffff"; border.color: "#9aa0a6" }
    fullScreenInputColor: "#202124"
    fullScreenInputSelectionColor: "#d2e3fc"
    fullScreenInputSelectedTextColor: "#202124"
    fullScreenInputFont.family: "Google Sans"
    fullScreenInputFont.pixelSize: 20
}
