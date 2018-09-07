new Vue ({
    delimiters: ['[[', ']]'],
    el: "#form_address",
    data: {
        cityZipCode: '',
        citiesZipCodesList: [],
        city: '',
        zipCode: '',
        address:'',
        fullAddress: '',
        addressesList: [],
        addressJSON: {},
        valid: false,
    },
    watch: { 
      cityZipCode : function() {
        if (! this.cityZipCode.includes("(")) {
          this.citiesZipCodesList = []
          this.lookupcityZipCode()
          this.city = ''
          this.zipCode = ''
        }
        if (! this.valid) {
        this.addressesList = []
        this.lookupAddress()
        }
        },
        address : function(){
          if (! this.valid) {
          this.addressesList = []
          this.lookupAddress()
        }
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
                }, 500)
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
              if (response.data.features.length) {
                for ( var i in response.data.features ){
                  var addr = response.data.features[i]
                  if (addr.properties.score > 0.5){
                    app.addressesList.push(addr)
                }
              }
            }
          })
        }, 500),
        selectedAddress: function(address) {
          this.cityZipCode = address.properties.city + " (" + address.properties.postcode + ")"
          this.address = address.properties.name
          this.city = address.properties.city
          this.zipCode = address.properties.postcode
          this.fullAddress = address.properties.label
          this.addressesList = []
          this.addressJSON = JSON.stringify(address)
          this.valid = true
          setTimeout(() => {
            this.valid = false
          }, 300)
        },                     
      }
})