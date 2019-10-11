<template>
  <v-row class="ChatBody" align="center" justify="center">
    <v-col class="innerChat" cols="12" sm="8" md="5">
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
        <v-dialog v-model="dialog" persistent max-width="400">
          <template v-slot:activator="{ on }">
            <v-btn
              fixed
              dark
              fab
              bottom
              right
              color="pink"
              v-on="on"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <div class="text-center">
                <h3>Think B 가르치기</h3>
              </div>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field v-model="question" label="이렇게 말하면" required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field v-model="answer" label="이렇게 대답해요" required></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="green darken-1" text @click="cancelData">취소</v-btn>
              <v-btn color="green darken-1" text @click="createData">가르치기</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
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
      dialog: false,
      question: "",
      answer: "",
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
    createData: function() {
      if (this.question.length == 0) {
        this.$swal('질문을 입력해주세요!', '어떻게 질문하면 이렇게 대답해야 할까요?', 'error')
        return false
      } else if (this.answer.length == 0) {
        this.$swal('답변을 입력해주세요!', '이 질문엔 어떻게 대답해야 좋을까요?', 'error')
        return false
      } else {
        this.$swal('Think B를 가르쳤어요!', '다음에는 이렇게 대답할게요!', 'success')
      }
      this.dialog = false
      this.question = ""
      this.answer = ""
    },
    cancelData: function() {
      this.dialog = false
      this.question = ""
      this.answer = ""
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