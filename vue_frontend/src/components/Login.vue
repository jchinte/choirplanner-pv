<template>
    <nav class="flex justify-between bb b--white-10 bg-black sans-serif">
    <a class="link white-70 hover-white no-underline flex items-center pa3" href="/">
        <svg
        class="dib h1 w1"
        data-icon="grid"
        viewBox="0 0 32 32"
        style="fill:currentcolor">
        <title>Super Normal Icon Mark</title>
        <path d="M2 2 L10 2 L10 10 L2 10z M12 2 L20 2 L20 10 L12 10z M22 2 L30 2 L30 10 L22 10z M2 12 L10 12 L10 20 L2 20z M12 12 L20 12 L20 20 L12 20z M22 12 L30 12 L30 20 L22 20z M2 22 L10 22 L10 30 L2 30z M12 22 L20 22 L20 30 L12 30z M22 22 L30 22 L30 30 L22 30z">
        </path>
        </svg>
    </a>
    <div class="flex-grow pa3 flex items-center">
        <router-link 
            v-for="menuItem in menu" 
            :key="menuItem.sort_order"
            :to="{ name: 'blog-post', params: { slug: menuItem.slug }}" 
            class="f6 link dib white dim mr3 mr4-ns">{{ menuItem.title }}</router-link>
        <!-- <a v-for="menuItem in menu" 
            :key="menuItem.sort_order" 
            class="f6 link dib white dim mr3 mr4-ns" 
            href="" 
            @click.prevent="loadPage(menuItem)">{{ menuItem.link_title }}</a> -->
        <router-link :to="{ name: 'blog' }" class="f6 link dib white dim mr3 mr4-ns">blog</router-link>
        <router-link v-if="(username.value && username.value.length)" :to="{ name: 'song-list' }" class="f6 link dib white dim mr3 mr4-ns">songs</router-link>
        <router-link v-if="(username.value && username.value.length)" :to="{ name: 'event-list' }" class="f6 link dib white dim mr3 mr4-ns">lineups</router-link>
        <a v-if="!(username.value && username.value.length)" class="f6 link dib white dim mr3 mr4-ns" href="#0" @click="openLogin">sign In</a>
        <!-- <a v-if="username.value&& username.value.length>0" class="f6 link dib white dim mr3 mr4-ns" href="#0">hello {{ username.value }}</a> -->
        <a v-if="username.value" class="f6 dib white bg-animate hover-bg-white hover-black no-underline pv2 ph4 br-pill ba b--white-20" href="#0" @click="logout">logout {{ username.value }}</a>
        <a v-else class="f6 dib white bg-animate hover-bg-white hover-black no-underline pv2 ph4 br-pill ba b--white-20" href="#0">sign up</a>
    </div>
  </nav>
  <!-- <div v-if="username.value && username.value.length>0" class="flex items-center justify-center pa1 bg-black">
      <span class="f6 dib white dim mr3 mr4-ns ph3"> hello {{ username.value }}</span>
  </div> -->
  <Modal v-model="loginOpen" max-width="500px">
            <!-- <div>
                Login:
                <label for="username"><b>Username</b></label>
                <input v-model="uname" type="text" placeholder="Enter Username" name="username">
                <label for="password"><b>Password</b></label>
                <input v-model="pass" type="password" placeholder="Enter Password" name="password">
                <button @click="getHash">submit</button>
            </div> -->
            <main class="pa4 black-80 bg-white">
                <form class="measure center" v-on:submit.prevent="getHash">
                    <fieldset id="sign_up" class="ba b--transparent ph0 mh0">
                    <legend class="f4 fw6 ph0 mh0">Sign In</legend>
                    <div class="mt3">
                        <label class="db fw6 lh-copy f6" for="email-address">Username</label>
                        <input v-model="uname" class="pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100" type="text" name="username"  id="username">
                    </div>
                    <div class="mv3">
                        <label class="db fw6 lh-copy f6" for="password">Password</label>
                        <input v-model="pass" class="b pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100" type="password" name="password"  id="password">
                    </div>
                    <label class="pa0 ma0 lh-copy f6 pointer"><input type="checkbox" v-model="remember"> Remember me</label>
                    </fieldset>
                    <div class="">
                    <input class="b ph3 pv2 input-reset ba b--black bg-transparent grow pointer f6 dib" type="submit" value="Sign in">
                    </div>
                    <div class="lh-copy mt3">
                    <a href="#0" class="f6 link dim black db">Sign up</a>
                    <a href="#0" class="f6 link dim black db">Forgot your password?</a>
                    </div>
                </form>
            </main>

  </Modal>


</template>

<script>
import { Modal } from 'vue-neat-modal'
import { client, localStorageKey, logout } from '../utils/fetch_utils.js'
export default {
    name: 'Login',
    components: {
        Modal,
    },
    data:function(){
        return {
            loginOpen: false,
            uname: '',
            pass: '',
            menu: [],
            remember: false,
        }
    },
    inject:['hash', 'prefix', 'updateHash', 'username'],
    created(){
        const username = localStorage.getItem('username')
        const token = localStorage.getItem(localStorageKey)
        if(token){
            this.$store.commit('login', {username, token})
        }
        client('api/menu/', ({}), this.prefix.value)
            .then(data=>{
                this.menu=data;
                return data;
            })
    },
    methods:{
        getHash() {
            console.log(this.hash, this.prefix, this.updateHash, this.username)
            client('dj-rest-auth/login/', {body:{username: this.uname, password: this.pass}}, this.prefix.value)
                .then(data =>{
                    console.log("data:", data)
                     this.updateHash(data.key, this.uname)
                     if (this.remember){
                         localStorage.setItem(localStorageKey, data.key)
                         localStorage.setItem('username', this.uname)
                     } else {
                         sessionStorage.setItem(localStorageKey, data.key)
                         sessionStorage.setItem('username', this.uname)
                     }
                     console.log(data.key, this.uname, this.username, localStorageKey)
                     console.log(this.$cookies);
                     this.loginOpen=false
                     this.$store.commit('login', {username: this.uname, token: data.key})
                })
                .catch(e=>{
                    console.log(e)
                    this.updateHash('', '')
                })
            //.then(this.getSong())
            //console.log(App);
        
        },
        openLogin(){
            this.loginOpen = true;
        },
        logout(){
            this.updateHash('', '')
            logout()
            window.localStorage.removeItem(localStorageKey)
            window.sessionStorage.removeItem(localStorageKey)
            window.localStorage.removeItem('username')
            window.sessionStorage.removeItem('username')
            this.$store.commit('logout')
            this.$router.push({name: 'root'})
        },
        loadPage(url){
            console.log(url)
        },
    }
}
</script>

<style scoped>

</style>