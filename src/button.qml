import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Controls.Styles 2.0
import QtGraphicalEffects 1.0

Item {
  height: 200
  width:  200
  
  property var baseColor: "#112244"
  
  Button {
    anchors.fill:parent
    
    style: ButtonStyle {
      background: Rectangle {
        id: background
        anchors.fill: parent
        radius: height/5
        
        gradient: Gradient {
          GradientStop { position: 1.00; color: Qt.lighter(baseColor, 0.6) }
          GradientStop { position: 0.80; color: Qt.lighter(baseColor, 0.5) }
          GradientStop { position: 0.00; color: Qt.lighter(baseColor, 0.1) }
        }
        
        Rectangle {
          id: innerBackground
          anchors.fill: parent
          anchors.margins: parent.height/20
          radius: height/5.5 // This ratio matches the iconmonstr icon style radius
          
          gradient: Gradient {
            GradientStop { position: control.pressed ? 0 : 1; color: Qt.lighter(baseColor, 0.8) }
            GradientStop { position: 0.66; color: Qt.lighter(baseColor, 1.0) }
            GradientStop { position: control.pressed ? 1 : 0; color: Qt.lighter(baseColor, 1.2) }
          }
        }
        
        Rectangle {
          id: iconFill
          visible: false
          anchors.fill: parent
          
          gradient: Gradient {
            GradientStop { position: 0.00; color: "#ABCDEF" }
            GradientStop { position: 0.33; color: "#789ABC" }
            GradientStop { position: 1.00; color: control.pressed ? "#349A78" : "#345678" }
          }
        }
        
        Image {
          id: icon
          visible: false
          anchors.fill: iconFill
          source: "./svg/iconmonstr-gear-10-icon.svg"
        }
        
        OpacityMask {
          anchors.fill: iconFill
          source: iconFill
          maskSource: icon
        }
        
        Canvas {
          id: highlight
          anchors.fill: innerBackground
          
          contextType: "2d"
          
          onPaint: {
            var radius = anchors.fill.radius
            
            var gradient = context.createLinearGradient(0, 0, 0, height)
            gradient.addColorStop(0.0, Qt.rgba(1, 1, 1, 0))
            gradient.addColorStop(0.4, Qt.rgba(1, 1, 1, 1))
            
            context.roundedRect(0, 0, width, height, radius, radius)
            context.clip()
            context.beginPath()
            
            context.arc(width/2, -width*0.85, width*1.2, 0, 3.14*2, false)
            context.fillStyle = gradient
            context.fill()
          }
          
          opacity: control.pressed ? 0.1 : 0.2
        }
        
      }
    }
  }
}
