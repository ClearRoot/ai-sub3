<template>
  <v-app>
    <v-content class="view">
      <!-- 라우터 -->
      <v-flex fill-height aacontainer class="IntroBody">
        <router-view></router-view>
      </v-flex>
      <v-flex class="Chatbot">
        <Chatbot></Chatbot>
      </v-flex>
      <!-- 라우터 -->
    </v-content>
  </v-app>
</template>

<script>
import Chatbot from "./components/Chatbot";
import $ from "jquery";

export default {
  name: 'App',
  components: {
    Chatbot
  },
  data() {
    return {
    }
  }
}

$(document).ready(function() {
  $('.IntroBody').on('mousewheel', function(e){
    if( e.originalEvent.wheelDeltaY < 0 ){
      $('.IntroBody, .Chatbot').addClass('scrolled');
      return false;
    }
  })
})

$(document).ready(function() {
  $(window).on('mousewheel', function(e){
    if( e.originalEvent.wheelDeltaY > 0 ){
      $('.IntroBody, .Chatbot').removeClass('scrolled');
    }
  })
})

</script>

<style>
.view {
  height: 100vh;
}

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

	  transition: all 1.6s cubic-bezier(0.86, 0, 0.07, 1);
    transform: translate3d(0, 0, 0) scale(1);
}

@-webkit-keyframes poodle {
    0%   {background-position: 3% 93%;}
    100% {background-position: 91% 93%;}
}

.IntroBody.scrolled {
	transform: translate3d(0, -100%, 0) scale(.75);
	opacity: 0;
}

.Chatbot{
	transition: all 1.6s cubic-bezier(0.86, 0, 0.07, 1);
	transform: translate3d(0, 0, 0) scale(.75);
	opacity: 0;
}
.Chatbot.scrolled{
	transform: translate3d(0, -100%, 0) scale(1);	
	opacity: 1;
}
</style>