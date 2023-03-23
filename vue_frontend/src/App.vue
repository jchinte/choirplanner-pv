<template>
 <router-view name="nav"></router-view>
<router-view />
</template>

<script>
import {
    provide,
    reactive,
    ref
} from 'vue'
import { prefix } from './utils/fetch_utils.js'
export default {
    name: 'App',
    components: {
    },
    data() {
        return {
            //hash: null,
            //username:null,
        }
    },
    setup() {
        //localStorage.clear()
        const debug = false;
        const hash = ref(localStorage.getItem('hash'));
        const username = ref(localStorage.getItem('username'))
        provide('hash', hash)
        const updateHash = (newHash, newUsername) => {
            if (debug){
              console.log(newHash)
              console.log(newUsername)
            }
            hash.value = newHash
            username.value = newUsername
            // localStorage.setItem('hash', newHash)
            // localStorage.setItem('username', newUsername);
        }
        const logout = () => {
        //   localStorage.removeItem('hash')
          localStorage.removeItem('username')
          hash.value = null
          username.value = null
        }
        const _prefix =  ref(prefix)
        provide('updateHash', updateHash)
        provide('username', username)
        provide('prefix', _prefix)
        provide('debug', debug)
    },
}


</script>

<style>

</style>
