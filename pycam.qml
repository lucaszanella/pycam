import QtQuick 2.7
import QtQuick.Window 2.0
import QtQuick.Controls 2.0
import QtQuick.Controls.Material 2.0

Window {
    id: window
    visible: true
    width: 800
    height: 520
    minimumWidth: 800
    minimumHeight: 520
    title: qsTr("PyCam")
    color: "black"
    Material.theme: Material.Light
    Material.accent: Material.Purple

    Row {
        id: row
        anchors.fill: parent

        Flow {
            id: flow1
            property var width_percentage : 1
            width: parent.width * width_percentage
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            clip: false

        }
    }

}
