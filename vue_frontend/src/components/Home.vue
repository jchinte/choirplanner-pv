<template>
<header class="sans-serif">
  <div class="cover bg-left bg-center-l" :style="'background-image: url(' + cover +')'">
    <div class="bg-black-60 pb5 pb6-m pb7-l">
        <Login />
      <div class="tc-l mt4 mt5-m mt6-l ph3">
        <h1 class="f2 f1-l fw2 white-90 mb0 lh-title">Praising Voices Choir</h1>
        <h2 class="fw1 f3 white-90 mt3 mb4">of St. Elizabeth Catholic Church, Milpitas, CA</h2>
        <a class="f6 no-underline grow dib v-mid bg-blue white ba b--blue ph3 pv2 mb3" href="/">Book us for your special event!</a>
        <span class="dib v-mid ph3 white-70 mb3">or</span>
        <a class="f6 no-underline grow dib v-mid white ba b--white ph3 pv2 mb3" href="">Learn about our choir</a>
      </div>
    </div>
  </div> 
</header>
</template>

<script>
import {
    inject
} from 'vue'
import Login from './Login.vue'

export default {
    components: {
        Login,
    },

    data() {
        return {
            cover:this.prefix + '/media/original_images/cover.jpg',

        }
    },
    created() {
        if (this.hash){
            this.goToMain();
        }
    },
    setup() {
        const hash = inject('hash')
        const updateHash = inject('updateHash')
        const prefix = inject('prefix')

        return {
            hash,
            updateHash,
            prefix,
        }
    },
    computed: {
    },
    methods: {
        goToMain() {
            console.log(this.$route);
            const next = this.$route.query.next;
            if (this.hash) {
                if (next){
                    const items = next.split('?')
                    if (items.length==1) {
                        this.$router.push(items[0]);
                    } 
                    else {
                        const params = items[1].split('&')
                        let q = {}
                        console.log(params)
                        for (let param of params){
                            let p = param.split('=')
                            if (p.length==2){
                                q[p[0]] = p[1];
                            }
                        }
                        this.$router.push({path: items[0], query: q});
                    }
                }
            }
        },
    }
}
</script>
