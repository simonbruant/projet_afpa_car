var vm = new Vue ({
    delimiters: ['[[', ']]'],
    el: "#form_address",
    data: {
        zipCode: '',
        city: '',
        citiesName: [],
        options: {}
    },
    watch: { 
        zipCode : function() {
        this.citiesName = []
        if (this.zipCode.length == 5) {
            this.lookupZipCode()
            }
        }
    },
    methods: {
        lookupZipCode: _.debounce(function() {
            var app = this
            axios.get('https://geo.api.gouv.fr/communes?codePostal=' + app.zipCode)
                    .then(function (response) {
                    for (var key in response.data) {
                        app.citiesName.push(response.data[key].nom)
                    }
                    options = {
                        data: app.citiesName
                    }
                })
                .catch(function (error) {
                app.startingCity = "Invalid Zipcode"
                })
        }, 500),
    }
})


$("#id_zip_code").easyAutocomplete(vm.options);

new Vue({
    el: '#form_address2',
    data: {
    startingZip: '',
    startingCity: '',
    endingZip: '',
    endingCity: ''
    },
    watch: {
      startingZip: function() {
        this.startingCity = ''
        if (this.startingZip.length == 5) {
          this.lookupStartingZip()
        }
      },
      endingZip: function() {
        this.endingCity = ''
        if (this.endingZip.length == 5) {
          this.lookupEndingZip()
        }
      }
    },
    methods: {
      lookupStartingZip: _.debounce(function() {
        var app = this
        app.startingCity = "Searching..."
        axios.get('http://ziptasticapi.com/' + app.startingZip)
              .then(function (response) {
                app.startingCity = response.data.city + ', ' + response.data.state
              })
              .catch(function (error) {
                app.startingCity = "Invalid Zipcode"
              })
      }, 500),
      lookupEndingZip: _.debounce(function() {
        var app = this
        app.endingCity = "Searching..."
        axios.get('http://ziptasticapi.com/' + app.endingZip)
              .then(function (response) {
                app.endingCity = response.data.city + ', ' + response.data.state
              })
              .catch(function (error) {
                app.endingCity = "Invalid Zipcode"
              })
      }, 500)
    }
  })