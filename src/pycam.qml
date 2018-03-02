import QtQuick 2.7
import QtQuick.Window 2.0
import QtQuick.Controls 2.0
import QtQuick.Controls.Material 2.0

Window {
    id: window
    visible: true
    width: 1280
    height: 720
    minimumWidth: 800
    minimumHeight: 520
    title: qsTr("PyCam")
    color: "black"
    Material.theme: Material.Light
    Material.accent: Material.Purple

    Row {
        id: row
        anchors.fill: parent
        state: "normal"
        width: window.width
        height: window.height
        Flow {
            id: flow1
            width: parent.width
            height: parent.height
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            clip: false

            Rectangle {
                id: rectangle
                width: parent.width*6.5/10
                height: this.width*9/16
                color: "#8ed586"
            }

            Rectangle {
                id: rectangle1
                width: this.height*16/9
                height: rectangle.height/2
                color: "#504abe"
                anchors.left: rectangle.right
                anchors.leftMargin: 0
            }

            Rectangle {
                id: rectangle2
                width: this.height*16/9
                height: rectangle.height/2
                color: "#cae274"
                anchors.top: rectangle1.bottom
                anchors.topMargin: 0
                anchors.left: rectangle.right
                anchors.leftMargin: 0
            }

            Rectangle {
                id: rectangle3
                width: rectangle2.width
                height: rectangle2.height
                color: "#ffffff"
                anchors.left: parent.left
                anchors.leftMargin: 0
                anchors.top: rectangle.bottom
                anchors.topMargin: 0
            }
            Rectangle {
                id: rectangle4
                width: rectangle2.width
                height: rectangle2.height
                color: "#2a4e95"
                anchors.left: rectangle3.right
                anchors.leftMargin: 0
                anchors.top: rectangle.bottom
                anchors.topMargin: 0
            }
            Rectangle {
                id: rectangle5
                width: rectangle2.width
                height: rectangle2.height
                color: "#2ce1b9"
                anchors.left: rectangle4.right
                anchors.leftMargin: 0
                anchors.top: rectangle.bottom
                anchors.topMargin: 0
            }
        }
        states: [
            State {
                name: "normal"
                PropertyChanges { target: row; x: 0; }
            },
            State {
                name: "column_opened"
                PropertyChanges { target: row; x: 300 }
            }
        ]
        transitions: [

            // When transitioning to 'middleRight' move x,y over a duration of 1 second,
            // with OutBounce easing function.
            Transition {
                from: "normal"; to: "column_opened"
                NumberAnimation { properties: "x,y"; easing.type: Easing.OutExpo; duration: 500 }
            },

            // When transitioning to 'bottomLeft' move x,y over a duration of 2 seconds,
            // with InOutQuad easing function.
            Transition {
                from: "column_opened"; to: "normal"
                NumberAnimation { properties: "x,y"; easing.type: Easing.OutExpo; duration: 500 }
            }
        ]
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
                PropertyChanges { target: column; x: width*0.3; }
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
                NumberAnimation { properties: "x,y"; easing.type: Easing.OutExpo; duration: 300 }
            }
        ]

    }

    Button {
        id: button
        x: 743
        y: 462
        width: 45
        height: 45
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        anchors.right: parent.right
        anchors.rightMargin: 20
        autoExclusive: false
        checked: false
        Material.foreground: false
        background: Image {
            anchors.topMargin: 0
            anchors.fill: parent
            source: "graphics/setup.png"
            fillMode: Image.PreserveAspectFit
        }
        checkable: true
        MouseArea {
            width: 45
            height: 45
            cursorShape: Qt.PointingHandCursor; acceptedButtons: Qt.DragMoveCursor }
        //Mouse area to react on click events
        onClicked: {
            row.state = "column_opened"
            column.state = column.state == "opened" ? column.state="closed" : column.state="opened"
        }
    }
}
