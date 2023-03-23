<template>
<login />
<h1>{{ loginMsg }}</h1>
<div v-if="!(hash)">
    <button @click="modalOpen = true">login</button>
    <p>Here we go</p>
    <teleport to="body">
        <div v-if="modalOpen" class="modal">
            <div>
                Login:
                <label for="username"><b>Username</b></label>
                <input v-model="uname" type="text" placeholder="Enter Username" name="username">
                <label for="password"><b>Password</b></label>
                <input v-model="pass" type="password" placeholder="Enter Password" name="password">
                <button @click="getHash">submit</button>
            </div>
        </div>
    </teleport>
</div>
<div v-else>
    <router-link to="/app/songs/200/">This is a link</router-link>
    in!
    <label for="song id"><b>Song ID</b></label>
    <input v-model="songId" placeholder="song id" />
    <button @click="getSong">get Song</button>
    <router-link :to="getSongDetailUrl()">song list</router-link>
    <div>
        <!-- <SongDetail v-bind:songId="songId">
        </SongDetail> -->
        <!-- <SongList /> -->
        <!-- <EventDetail v-bind:eventId="songId" /> -->
       
    </div>
    <!-- <div>
      <song-list-2 v-model:pageNum="page" />
    </div> -->
</div>
</template>

<script>
import SongDetail from './SongDetail.vue'
import SongList from './SongList.vue'
import EventDetail from './EventDetail.vue'
import {
    computed
} from 'vue'
import Login from './Login.vue'

export default {
    name: 'MassPlannerApp',
    props: {
        //loginMsg: String,
        //pre: String,
    },
    data() {
        return {
            pre: "http://192.168.1.245:8000",
            loginMsg: "Song",
            songId: "200",
            modalOpen: false,
            uname: null,
            pass: null,
            song: null,
            editSong: false,
            page: 1,
        }
    },
    created() {
        if (this.debug) {
            console.log("in planner");
        }
        if (!this.hash.value) {
            if (this.debug) {
                console.log("trying to login")
            }
            this.$router.push('/')
        }
    },
    methods: {
        getSongDetailUrl() {
            return "/app/songs/" + this.songId;
        },
        getHash() {
            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: this.uname,
                    password: this.pass
                })
            };
            fetch(this.pre + "/api-token-auth/", requestOptions)
                .then(response => response.json())
                .then(data => this.hash = data.token)
            //.then(this.getSong())
            //console.log(App);
        },
        // getSong(){
        //   this.song = null;
        //     const requestOptions = {
        //         method: "GET",
        //         headers: { "Content-Type": "application/json",
        //                    "Authorization": "Token " +  this.hash},
        //         //body: JSON.stringify({username: this.uname, password: this.pass})
        //     };
        //     console.log(requestOptions);
        //     console.log(this.hash)
        //   fetch(this.pre+"/songs/api/songs/"+this.songId, requestOptions)
        //     .then(response=>response.json(), error=>null)
        //     .then(data=>(('detail' in data)? null : this.song=data))
        //     //.then(getAuth());
        //   const requestOptionsOptions = {
        //         method: "OPTIONS",
        //         headers: { "Content-Type": "application/json",
        //                    "Authorization": "Token " +  this.hash},
        //         //body: JSON.stringify({username: this.uname, password: this.pass})
        //     };
        //   fetch(this.pre+"/songs/api/songs/"+this.songId, requestOptionsOptions)
        //     .then(response=>response.json())
        //     .then(data=>this.editSong = ('actions' in data && 'PUT' in data['actions'])); 
        // }

    },
    components: {
        SongDetail,
        SongList,
        EventDetail,
        Login,
    },
    provide() {
        return {
            //hash: computed(() => this.hash),
            prefix: this.pre,
        }
    },
    inject: ['hash', 'debug', 'prefix'],
}
</script>

<style>
/* 
.modal {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: rgba(0, 0, 0, .5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.modal div {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: white;
    width: 300px;
    height: 300px;
    padding: 5px;
} */
</style>
