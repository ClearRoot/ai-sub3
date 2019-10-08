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
          content: '안녕하세요 ThinkB입니다.', 
          myself: false,
          participantId: 1,
          timestamp: { year: 0, month: 0, day: 0, hour: 0, minute: 0, second: 0, millisecond: 0 },
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
    onMessageSubmit: async function(message){
      message.content = message.content.replace(/\n/g, "")

      const axios = require('axios')

      let form = new FormData()
      form.append('question', message["content"])

      this.messages.push(message)

      await axios.post('http://13.125.199.238:5000/chat', form)
        .then( res => {
          console.log(res["data"]["answer"])
          let answer = {
            content: res["data"]["answer"],
            myself: false,
            participantId: 1,
            timestamp: { year: 0, month: 0, day: 0, hour: 0, minute: 0, second: 0, millisecond: 0 },
            uploaded: true
          }
          this.messages.push(answer)
          message.uploaded = true
        }).catch( err => {
          console.log(err)
        })
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