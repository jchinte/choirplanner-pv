<template>
    <div v-if="html" v-html="html"></div>
</template>

<script>
import { client } from '../utils/fetch_utils.js'
export default {
    name: 'PageContainer',
    inject: 'prefix',
    props: {
        url: String,
    },
    data: function(){
        return {
            html: null,
        }
    },
    created(){
        client(url, ({}), this.prefix.value, false)
            .then(data=>this.html=data)
            .catch(e=>console.log(e))
    }
}
</script>