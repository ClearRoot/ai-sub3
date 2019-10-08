import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueFullPage from 'vue-fullpage.js'

import 'expose-loader?$!expose-loader?jQuery!jquery'

Vue.use(VueFullPage);

import router from './router';

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
