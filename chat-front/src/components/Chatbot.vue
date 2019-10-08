<template>
  <v-row class="ChatBody" align="center" justify="center">
    <v-col cols="12" sm="8" md="5">
      <div id="thinkB_chat">
        <Chat 
        :participants="participants"
        :myself="myself"
        :messages="messages"
        :onType="onType"
        :onMessageSubmit="onMessageSubmit"
        :chatTitle="chatTitle"
        :placeholder="placeholder"
        :colors="colors"
        :borderStyle="borderStyle"
        :hideCloseButton="hideCloseButton"
        :closeButtonIconSize="closeButtonIconSize"
        :submitIconSize="submitIconSize"
        :asyncMode="asyncMode"/>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { Chat } from 'vue-quick-chat'

export default {
  name: 'Chatbot',
  components: {
    Chat
  },
  data() {
    return {
      participants: [
        {
          name: 'ThinkB',
          id: 1
        }
      ],
      myself: {
        name: 'YOU',
        id: 2
      },
      messages: [
        {
          content: 'received messages', 
          myself: false,
          participantId: 1,
          timestamp: { year: 2019, month: 3, day: 5, hour: 20, minute: 10, second: 3, millisecond: 123 },
          uploaded: true
        }
      ],
      chatTitle: 'ThinkB',
      placeholder: 'send your message',
      colors:{
        header:{
          bg: '#558B2F',
          text: '#fff',
        },
        message:{
          myself: {
            bg: '#fff',
            text: '#000'
          },
          others: {
            bg: '#43A047',
            text: '#fff'
          },
          messagesDisplay: {
            bg: '#f7f3f3'
          }
        },
        submitIcon: '#558B2F'
      },
      borderStyle: {
        topLeft: "10px",
        topRight: "10px",
        bottomLeft: "10px",
        bottomRight: "10px",
      },
      hideCloseButton: true,
      submitIconSize: "35px",
      closeButtonIconSize: "20px",
      asyncMode: true
    }
  },
  methods: {
    onType: function (event){
      //here you can set any behavior
    },
    onMessageSubmit: function(message){
      /*
      * example simulating an upload callback. 
      * It's important to notice that even when your message wasn't send 
      * yet to the server you have to add the message into the array
      */
      this.messages.push(message)
      
      /*
      * you can update message state after the server response
      */
      // timeout simulating the request
      setTimeout(() => {
        message.uploaded = true
      }, 2000)
    },
  }
}
</script>

<style>
  #thinkB_chat {
    height: 500px;
  }

  .ChatBody {
    height: 100vh;

    background: lightblue;
    background-image: url('../assets/poodle.png');
    background-repeat: no-repeat;
    background-position: 91% 90%;
    background-size: 250px;
  }
</style>