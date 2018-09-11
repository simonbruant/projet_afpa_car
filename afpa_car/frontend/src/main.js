import App from './App.vue';
import mymap from './leaflet/map_leaflet'
import _ from 'lodash';

// ~~~~~~~~ TESTLODASH ~~~~~~~~~~ //

var a = _.last([0, 1, false, 2, '', 3]);
console.log(a)

// ~~~~~~~~ TESTVUEJS ~~~~~~~~~~ //

new Vue({
    el: '#app',
    render: h => h(App),
});


