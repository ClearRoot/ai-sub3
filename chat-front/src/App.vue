<template>
  <v-app>
    <v-content>
      <!-- 라우터 -->
      <v-container class="IntroBody" fluid fill-height aacontainer>
        <router-view></router-view>
      </v-container>
      <Chatbot></Chatbot>
      <!-- 라우터 -->
    </v-content>
  </v-app>
</template>

<script>
import Chatbot from "./components/Chatbot";

export default {
  name: 'App',
  components: {
    Chatbot
  },
  data() {
    return {
    };
  },
};
</script>

<style>
.IntroBody {
    height: 100vh;

    background-color:#ffe55f !important;
    background-image: url('./assets/pupper.gif');
    background-repeat: no-repeat;
    background-position: 91% 93%;
    background-size: 300px;

    animation-name: poodle;
    animation-duration: 4s;
    animation-duration: leaner;
    animation-direction: alternate;
    animation-fill-mode: forwards;
}

@-webkit-keyframes poodle {
    0%   {background-position: 3% 93%;}
    100% {background-position: 91% 93%;}
}
</style>