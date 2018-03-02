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
            width: window.width
            height: window.height
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            clip: false
        }
    }

    Column {
        id: column
        x: 0
        y: 0
        width: window.width
        height: window.height
        state: "closed"
        visible: true
        Rectangle {
            color: "#202226"
            anchors.fill: parent
          GridView {
            delegate: Rectangle {
              color: "transparent"
            }
          }
        }
        states: [
            State {
                name: "opened"
                PropertyChanges { target: column; x: width*0.1; }
            },
            State {
                name: "closed"
                PropertyChanges { target: column; x: window.width; }
            }
        ]

        Button {
            id: button1
            x: 8
            y: 9
            text: qsTr("Button")
        }

        transitions: [

            // When transitioning to 'middleRight' move x,y over a duration of 1 second,
            // with OutBounce easing function.
            Transition {
                from: "closed"; to: "opened"
                NumberAnimation { properties: "x,y"; easing.type: Easing.OutExpo; duration: 500 }
            },

            // When transitioning to 'bottomLeft' move x,y over a duration of 2 seconds,
            // with InOutQuad easing function.
            Transition {
                from: "opened"; to: "closed"
                NumberAnimation { properties: "x,y"; easing.type: Easing.OutExpo; duration: 1000 }
            }
        ]

    }

    Button {
        id: button
        x: 688
        y: 467
        text: qsTr("config")
        //Mouse area to react on click events
        onClicked: {
            button.text = "cjh"
            column.state = "opened"
        }
    }


}
