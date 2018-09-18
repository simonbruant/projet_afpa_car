<template>
  <div id="app" class="font-sans text-black min-h-screen bg-grey p-8">
    <div class="max-w-sm mx-auto bg-white rounded shadow-lg p-8">
      <Autocomplete v-model="selectedCityZip" :options="cityZipCodeList" :search="searchCityZip" 
      :holder="placeHolderCityZip" id="id_city_zip_code" @search="newSearchCityZip => searchCityZip = newSearchCityZip"/>
    </div>
    <br>
    <div class="max-w-sm mx-auto bg-white rounded shadow-lg p-8">
      <Autocomplete v-model="selectedAddress" :options="addressList" :search="searchAddress" 
      :holder="placeHolderAddress" id="id_address" @search="newSearchAddress => searchAddress = newSearchAddress"/>
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
      placeHolderCityZip: "Entre votre ville ou code postal...",
      placeHolderAddress: "Entrez votre adresse..."
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
        console.log("search", this.searchCityZip)
    if (!isNaN(this.searchCityZip)) {
        axios.get('https://geo.api.gouv.fr/communes?codePostal=' + this.searchCityZip)
            .then((response) => {
                console.log(response.data)
            if (response.data)  {
                for (let key in response.data) {
                    console.log(key)
                    console.log(response.data[key].nom)
                    let city = response.data[key].nom
                    let zipCode = this.searchCityZip
                    this.cityZipCodeList.push(city + " ("+ zipCode + ")")
                }
            }
        })} else {
        axios.get("https://geo.api.gouv.fr/communes?nom=" + this.searchCityZip)
            .then((response) => {
                if (response.data)  {
                for (let i in response.data) {
                    let city = response.data[i]
                    for (let j in city.codesPostaux) {
                        let zip = city.codesPostaux[j]
                    this.cityZipCodeList.push(city.nom + " (" + zip + ")")
                    }
                }
            }
          })}
    }, 500),
    lookupAddress: _.debounce(function () {
          let address = _.replace(this.searchAddress,/ /g, '+')
          axios.get('https://api-adresse.data.gouv.fr/search/?q=' + this.searchAddress) // + '&postcode=' //+ this.zipCode + '&city=' + this.city)
            .then((response) => {
              if (response.data.features) {
                for ( let i in response.data.features ){
                  let addr = response.data.features[i]
                  if (addr.properties.score > 0.5){
                    this.addressList.push(addr.properties.label)
                }
              }
            }
          })
        },),
    
  }
};
</script>
