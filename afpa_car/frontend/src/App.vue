<template>
  <div id="app">
    <div class="max-w-sm mx-auto bg-white rounded">
      <Autocomplete v-model="selectedCityZip" :options="cityZipCodeList" :search="searchCityZip" 
      holder="Entre votre ville ou code postal..." id="id_city_zip_code" type="city" :data="cityZip"
      @search="newSearchCityZip => searchCityZip = newSearchCityZip"
      @data="newCityZip => cityZip = newCityZip"/>
    </div>
    <br>
    <div class="max-w-sm mx-auto bg-white">
      <Autocomplete v-model="selectedAddress" :options="addressList" :search="searchAddress" 
      holder="Entrez votre adresse..." id="id_address" type="addr" :data="addressJSON"
      @search="newSearchAddress => searchAddress = newSearchAddress"
      @data="newJson => addressJSON = newJson"/>
    </div>
    <br>
     <div class="max-w-sm mx-auto">
       <input v-model="addressJSON" placeholder="Json" id="id_json_hidden" name="json_hidden" required type="text" class="block mb-2 w-full px-3 py-2 border rounded" style="outline: 0;">
     </div>
     <div>
     <button @click="postAddress" class="btn btn-success">Envoyer</button>
     </div>
  </div>
</template>

<script>
import Autocomplete from "./components/Autocomplete.vue";
import axios from 'axios';
import _ from 'lodash'

export default {
  name: "app",
  components: {
    Autocomplete
  },
  data() {
    return {
      selectedCityZip: null,
      selectedAddress: null,
      searchCityZip: "",
      searchAddress: "",
      cityZipCodeList: [],
      addressList: [],
      addressJSON: "",
      cityZip: "",
      cityZipFilter: ""
    };
  },
  watch: {
    searchCityZip () {
      this.lookupcityZipCode()
      this.cityZipCodeList = []
    },
    searchAddress () {
      this.lookupAddress()
      this.addressList = []
    },
},
    methods: {
    lookupcityZipCode: _.debounce(function() {
        // console.log("search", this.searchCityZip)
    if (!isNaN(this.searchCityZip)) {
        axios.get('https://geo.api.gouv.fr/communes?codePostal=' + this.searchCityZip)
            .then((response) => {
                // console.log(response.data)
            if (response.data)  {
                for (let key in response.data) {
                    // console.log(key)
                    // console.log(response.data[key].nom)
                    let city = response.data[key].nom
                    let zipCode = this.searchCityZip
                    this.cityZipCodeList.push([city, zipCode]) 
                }                               
            }
        })} else {
        axios.get("https://geo.api.gouv.fr/communes?nom=" + this.searchCityZip)
            .then((response) => {
                if (response.data)  {
                for (let i in response.data) {
                    let city = response.data[i]
                    for (let j in city.codesPostaux) {
                        let zipCode = city.codesPostaux[j]
                    this.cityZipCodeList.push([city.nom, zipCode])
                    }
                }
            }
          })}
    }, 500),
    lookupAddress: _.debounce(function () {
        // console.log("cizip", this.cityZip)
          let address = _.replace(this.searchAddress,/ /g, '+')
          if (this.cityZip) {
            this.cityZipFilter = '&postcode=' + this.cityZip[1] + '&city=' + this.cityZip[0]
          }
          axios.get('https://api-adresse.data.gouv.fr/search/?q=' + address + this.cityZipFilter)
            .then((response) => {
              if (response.data.features) {
                for ( let i in response.data.features ){
                  let addr = response.data.features[i]
                  if (addr.properties.score > 0.5){
                    this.addressList.push(addr)
                }
              }
            }
          })
        }),
      postAddress (event) {
        event.preventDefault()
        console.log(this.addressJSON)
        axios.post('http://127.0.0.1:8000/profil/adresse/' + this.addressJSON)
        .then(response => {console.log(reponse.data)})
        .catch(error => console.log(error)
        )
        
      }
    
  }
};
</script>
