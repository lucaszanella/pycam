import QtQuick 2.9
import QtQuick.Window 2.3
import QtQuick.Controls 2.1
import QtQuick.Controls.Material 2.1

Window {
    id: window
    visible: true
    width: 800
    height: 480
    title: qsTr("Hello World")
    color: "black"
    Material.theme: Material.Light
    Material.accent: Material.Purple

    Row {
        id: row
        anchors.fill: parent

        Flow {
            id: flow1
            width: parent.width * 0.8
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            clip: false

        }

        Column {
            id: column
            width: parent.width * 0.2
            anchors.right: parent.right
            anchors.rightMargin: 0
            transformOrigin: Item.Center
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
        }
    }
}
