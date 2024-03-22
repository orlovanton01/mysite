import { ref } from 'vue'
import { defineStore } from 'pinia'
// import { getSearch } from '@/App.vue'

export const useSearchStore = defineStore('search', ()=>{
    const search=ref('')
    function addSearch(arg){
      search.value=arg
    }
    return {search, addSearch}
 })