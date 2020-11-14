import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.esm.browser.js'
import queue from '../queueFile.js';

new Vue({
  el: '#player-queue-container',
  data: function() {
    return {
      queue: []
    }
  },
  mounted: function() {
    let global = this;
    window.setInterval(() => {
        import('../queueFile.js').then(function(d){
              global.queue = d.default;
              console.log(d.default);
            }
        );
    },2000);
  }
})