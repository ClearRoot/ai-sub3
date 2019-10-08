<template>
    <v-row class="pt-12" justify="center">
        <section>
            <div class="loading loading08 mt-12 pt-12 mb-5">
                <span data-text="W">W</span>
                <span data-text="E">E</span>
                <span data-text="L">L</span>
                <span data-text="C">C</span>
                <span data-text="O">O</span>
                <span data-text="M">M</span>
                <span data-text="E">E</span>
            </div>
            <v-container>
                <div class="test text-center mb-12">
                    <v-btn outlined color="grey darken-1">ThinkB랑 대화하러 가기</v-btn>
                    <a href="#"><span></span></a>
                </div>
            </v-container>
        </section>
    </v-row>
</template>

<script>
export default {
    name: "HomePage",
    data () {
        return {
            clickbtn: false,
        }
    },
    computed: {
    },
    components: {
    },
}
</script>

<style>
.loading {
    font-size: 8vw;
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    text-align: center;
}
.loading span {
    display: inline-block;
    margin: 0 .12em;
}
.loading08 span {
    position: relative;
    color: rgba(0, 0, 0, 0.5);
    animation: loading08-parent 5s infinite;
}
.loading08 span::after {
    position: absolute;
    top: 0;
    left: 0;
    content: attr(data-text);
    color: #fff;
    opacity: 0;
    animation: loading08-child 5s infinite;
}
.loading08 span:nth-child(2)::after {
    animation-delay: 0.2s;
}
.loading08 span:nth-child(3)::after {
    animation-delay: 0.4s;
}
.loading08 span:nth-child(4)::after {
    animation-delay: 0.6s;
}
.loading08 span:nth-child(5)::after {
    animation-delay: 0.8s;
}
.loading08 span:nth-child(6)::after {
    animation-delay: 1s;
}
.loading08 span:nth-child(7)::after {
    animation-delay: 1.2s;
}

@keyframes loading08-parent {
    0%, 35%, 100% {
        color: rgba(0, 0, 0, 0.2);
    }
    60%, 80% {
        color: #fff;
    }
}
@keyframes loading08-child {
    0% {
        opacity: 1;
    }
    25%, 100% {
        opacity: 0;
    }
}

a {
  padding-top: 70px;
}
a span {
  position: absolute;
  top: 55vh;
  left: 50%;
  width: 24px;
  height: 24px;
  margin-left: -12px;
  border-left: 5px solid #fff;
  border-bottom: 5px solid #fff;
  -webkit-transform: rotate(-45deg);
  transform: rotate(-45deg);
  -webkit-animation: sdb 1.5s infinite;
  animation: sdb 1.5s infinite;
  box-sizing: border-box;
}
@-webkit-keyframes sdb {
  0% {
    -webkit-transform: rotate(-45deg) translate(0, 0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    -webkit-transform: rotate(-45deg) translate(-20px, 20px);
    opacity: 0;
  }
}
@keyframes sdb {
  0% {
    transform: rotate(-45deg) translate(0, 0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: rotate(-45deg) translate(-20px, 20px);
    opacity: 0;
  }
}
</style>