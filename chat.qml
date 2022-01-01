import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import ChatModel 1.0

ApplicationWindow {
    id: root
    title: qsTr("Chat")
    width: 540
    height: 720
    visible: true

    SqlConversationModel {
        id: chat_model
    }

    ColumnLayout {
        anchors.fill: parent

        ListView {
            id: listView
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: pane.leftPadding + messageField.leftPadding
            displayMarginBeginning: 40
            displayMarginEnd: 40
            verticalLayoutDirection: ListView.BottomToTop
            spacing: 12
            model: chat_model
            delegate: Column {
                
                readonly property bool sentByMe: model.recipient !== "Me"

                anchors.right: sentByMe ? listView.contentItem.right : undefined
                spacing: 6

                Row {
                    id: messageRow
                    spacing: 6
                    anchors.right: sentByMe ? parent.right : undefined

                    Rectangle { // Message Blob
                        width: Math.min(messageText.implicitWidth + 24,
                            listView.width - (!sentByMe ? messageRow.spacing : 0))
                        height: messageText.implicitHeight + 24
                        radius: 15
                        color: sentByMe ? "steelblue" : "lightgrey"

                        Label {
                            id: messageText
                            text: model.message
                            color: sentByMe ? "white" : "black"
                            anchors.fill: parent
                            anchors.margins: 12
                            wrapMode: Label.Wrap
                        }
                    }
                }

                /*Label {
                    id: timestampText
                    text: Qt.formatDataTime(model.timestamp, "d MM hh:mm")
                    color: "lightgrey"
                    anchors.right: sentByMe ? parent.right : undefined
                }*/
            }

            ScrollBar.vertical: ScrollBar {}
        }

        Pane {
            id: pane
            Layout.fillWidth: true

            RowLayout {
                width: parent.width

                TextArea {
                    id: messageField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Compose message")
                    wrapMode: TextArea.Wrap
                }

                Button {
                    id: sendButton
                    text: qsTr("Send")
                    enabled: messageField.length > 0
                    onClicked: {
                        listView.model.send_message("machine", messageField.text, "Me");
                        messageField.text = "";
                    }
                }
            }
        }
    }
}


