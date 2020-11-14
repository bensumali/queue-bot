import Vue from 'https://cdn.jsdelivr.net/npm/vue@latest/dist/vue.esm.browser.min.js'
import queue from '../queueFile.js';

new Vue({
  el: '#player-queue-container', // This should be the same as your <div id=""> from earlier.
  data: function() {
    return {
      queue: queue
    }
  }
})