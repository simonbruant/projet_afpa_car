new Vue ({
    delimiters: ['[[', ']]'],
    el: "#form_address",
    data: {
        cityZipCode: '',
        citiesZipCodesList: [],
        city: '',
        zipCode: '',
        address:'',
        response: '',
    },
    watch: { 
      cityZipCode : function() {
        if (! this.cityZipCode.includes("(")) {
          this.citiesZipCodesList = []
          this.lookupcityZipCode()
          }
        },
        address : function(){
          this.lookupAddress()
        }
      },
    methods: {
        lookupcityZipCode: _.debounce(function() {
            var app = this
            axios.get('https://geo.api.gouv.fr/communes?codePostal=' + app.cityZipCode)
                    .then(function (response) {
                    if (response.data.length)  {
                      for (var key in response.data) {
                        city = response.data[key].nom
                        zipCode = app.cityZipCode
                        app.citiesZipCodesList.push([city, zipCode])
                      }
                    }
                })
                .catch(function (error) {
                app.startingCity = "Invalid Zipcode"
                })
            axios.get("https://geo.api.gouv.fr/communes?nom=" + app.cityZipCode)
            .then(function (response) {
              if (response.data.length)  {
                for (var i in response.data) {
                  city = response.data[i]
                  for (var j in city.codesPostaux) {
                    zip = city.codesPostaux[j]
                    app.citiesZipCodesList.push([city.nom, zip])
                  }
                }
              }
          })
        }, 500),
        selectedCityZip: function(cityZip) {
            this.cityZipCode = cityZip[0] + " (" + cityZip[1] + ")"
            this.city = cityZip[0]
            this.zipCode = cityZip[1]
            this.citiesZipCodesList = []
        },
        lookupAddress: _.debounce(function () {
          var app = this
          var address = _.replace(app.address,/ /g, '+')
          axios.get('https://api-adresse.data.gouv.fr/search/?q=' + address + '&postcode=' + app.zipCode + '&city=' + app.city)
            .then(function (response) {
              app.response = response.data
          })
        }, 500),                      
      }
})