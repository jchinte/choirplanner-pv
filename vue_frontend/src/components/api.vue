

<script>
const axios = require('axios').default;
export const api = axios.create({
    baseURL: process.env.VUE_APP_API || 'http://localhost:8000/'
})
export default {
    
}
</script>