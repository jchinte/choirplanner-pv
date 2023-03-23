<template>
<div v-if="(song && song) || (title && composers)">
    <div @click="toggleExpanded()" class="mw9 center ph3-ns">
        <div class="cf">
            <div class="fl w-10 w-25-l">
                <div class="fl w-100 w-third-l">
                    <div class="no-underline black bg-animate hover-bg-black hover-white inline-flex items-center">
                    <font-awesome-icon v-if="isExpanded" icon="caret-square-down" />
                    <font-awesome-icon v-else icon="caret-square-up"  />
                    </div>
                </div>
                <div v-if="!inDialog" class="fl w-100 w-third-l"> <!-- placeholder -->
                </div>
                <div v-if="!inDialog" class="fl w-100 w-third-l">
                    <button v-if="!inDialog && canEditSong" class="no-underline black bg-animate hover-bg-black hover-white inline-flex items-center pa2 ba border-box" @click.stop="toggleEdit">
                        <font-awesome-icon v-if="canEditSong" icon="edit" :highlight="editSong" />
                    </button>
                </div>
            </div>
            <div class="fl w-90 w-75-l">
                <div class="mw9 center">
                    <div class="fl w-100 w-two-thirds-ns tc tl-ns">
                        <div>
                            <a href="#" v-if="inDialog" class="f6 link dim ph3 pv2 mb2 white bg-black" @click.stop="select($event)">
                            {{ title }}
                            </a>
                            <template v-else-if="!editSong">
                                <router-link v-if="!focused" :to="{ name:'song-detail', params:{ songId: songId, expanded: true } }" class="f5 fw9 link dim br3 ph2 pv1 mb2 dib black">
                                {{ title }}
                                </router-link>
                                <span v-else class="sans-serif f3 fw5">
                                    {{ title }}
                                </span>
                            </template>
                            
                            <input v-else v-bind:value="title" :class="['.bn', titleSaving && 'bg-light-yellow']" @click.stop  @input="editTitle($event.target.value)"/>
                            <!-- </button> -->
                            <!-- </router-link> -->
                        </div>
                    </div>
                    <div class="fl w-100 w-third-ns">
                        <div v-if="!editSong" class="flex items-center center flex-column">
                            <span v-for="(composer, i) in composerFullNames" :key="i" class="f5 db black-70">{{ composer }}</span>
                        </div>
                        <div v-else class="flex items-center center flex-column">
                            <div v-for="(composer, i) in composerFullNames" :key="i" class="cf">
                            <font-awesome-icon v-if="composerFullNames.length > 1" icon="times-circle" size="lg" style="color:Tomato" @click="deleteComposer(i)" />
                            <input class="f5 w-80" v-bind:value="composerFullNames[i]"  @click.stop @input="editComposer($event, i)">
                            </div>
                            <div><button class="f6 link dim ph3 pv2 mb2 dib white bg-black" @click.stop="addComposer()">add a composer</button></div>    
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <template v-if="isExpanded && song">
        <ul class="list pl0 mt0 center">
            <template v-for="file in song.files" :key="file.id">
                <li v-if="filterTagList.length==0||file.filetypes.filter(t=>filterTagList.includes(t.type)).length>0" class="ph3 pv0 bb b--light-silver">
                    <SongFiles :file="file" :editSong="editSong" @update:file="updateFile($event)" @delete:file="deleteFile($event)" :tagList="filterTagList" />
                </li>
            </template>
            <li v-if="editSong" class="flex items-center lh-copy pa3 ph0-l bb b--black-10">
                <div class="fl w-20" style="text-align: right;">
                    <font-awesome-icon icon="file-upload" size="2x" />
                </div>
                <div class="fl w-20">&nbsp;</div>
                <div class="fl w-60" style="text-align:left">
                    <input type="file" :id="uploadId" @change="doUpload" :disabled="uploadDisabled.value" hidden />

                    <span v-if="!uploadDisabled.value" style="width:110px"><label class="uploadStyled" :for="uploadId" :disabled="uploadDisabled.value">
                            upload a new file
                        </label>
                    </span>
                    <span v-else style="width:150px">
                        <font-awesome-icon icon="spinner" style="width:110px" pulse />
                    </span>
                </div>
            </li>
        </ul>
    </template>
    <button v-if="editSong" @click="doDelete">Delete song?</button>
    <!--ul><li v-for="tag in tags">{{ tag.tag_name }}</li></ul-->
    <ConfirmDialog v-if="confirm" :callback="doConfirm" :cancelDialog="doCancel" message="this is a box" />
</div>
</template>

<script>

import ConfirmDialog from './ConfirmDialog.vue'
import SongFiles from './SongFiles.vue'
import {
    reactive,
    ref
} from 'vue'
import { client } from '../utils/fetch_utils.js'
export default {
    name: 'SongDetail',
    props: {
        songId: [String, Number],
        expanded: {
            type: Boolean,
            default: true,
        },
        focused: {
            type: Boolean,
            default: true,
        },
        initTitle: {
            type: String,
            default: null,
        },
        initComposers: {
            type: Array,
            default: [],
        },
        inDialog: {
          type: Boolean,
          default: false,
        },
        tagList: {
            type: Array,
            default: null,
        },
        filterTagList:{
            type: Array,
            default: [],
        }
        //editSong: Boolean,
        //prefix: String,
        //id: Number,
        //first_line: String,
        //composers: Array,
        //files: Array,
    },
    data() {
        if (this.debug) {
            console.log("initial expanded: ", this.expanded)
        }
        return {
            paramId: this.$route.params.songId,
            confirm: false,
            newFileType: '',
            editSong: false,
            uploadDisabled: reactive({
                value: false
            }),
            isExpanded: this.expanded,
            titleDelayId: 0,
            composersDelayId: 0,
        }
    },
    emits: ['select', 'update:expanded', 'update:tagList'],
    created: function () {
        if (!this.$store.getters.loggedIn) {
            if (this.debug) {
                console.log("trying to login (SongDetail)")
            }
            this.$router.push('/')
        }
        console.log("inmount")
        if (this.isExpanded){
            console.log("yes")
            this.getSong()
            if (this.editSong) {
                this.getTags();
            }
        }
    },
    computed: {
        uploadId: function () {
            return "upload" + this.songId
        },
        allTags(){
            return this.$store.state.tags
        },
        title(){
            console.log("Title for: ", this.songId)
            const storeTitle = this.$store.getters.getSongTitle(this.songId);
            return storeTitle? storeTitle : this.initTitle
        },
        song(){
            console.log("Song: ", this.songId)
            return this.$store.getters.getSong(this.songId);
        },
        composers(){
            const composers = this.$store.getters.getSongComposers(this.songId);
            return composers? composers : this.initComposers
        },
        composerFullNames(){
            const composers = this.$store.getters.getSongComposerFullNames(this.songId);
            console.log("composer fullnames = ", composers)
            return composers? composers : this.initComposers.map(c => [c.first_name, c.last_name].join(' '))
        },
        canEditSong(){
            return this.$store.state.songEditor;
        },
        titleSaving(){
            return this.$store.state.songTitleProcess? true : false;
        },
        composersSaving(){
            return this.$store.state.songComposersProcess? true : false;
        },
    },
    watch: {
        songId() {
            this.isExpanded = false;
        },
        expanded() {
            this.isExpanded = this.expanded;
            this.updateExpanded();
        },
        song: {
            deep: true,
            handler(){
                 console.log("update song fired")
                if (this.song && this.song.files){
                    console.log(this.song.id, this.song.files)
                    this.$emit('update:tagList', this.song.files.map(file=>file.filetypes).flat())
                    console.log("updating! ", this.song.files.map(file=>file.filetypes).flat())
                } else {
                    console.log("no files")
                }
            }
        },
    },
    updated: function () {
        console.log("updated...")
    },
    methods: {
        editTitle(newTitle){
            console.log("new title:", newTitle)
            this.$store.dispatch('updateSongTitle', {songId: this.songId, newTitle: newTitle})
        },
        addComposer(){
          this.$store.commit('addComposer', this.songId)
        },
        deleteComposer(i){
          this.composerFullNames.splice(i, 1);
        },
        goBack() {
            this.$router.go(-1);
        },
        toggleExpanded: function () {
            if (this.debug) {
                console.log("Toggle fired")
            }
            this.isExpanded = !this.isExpanded;
            this.$emit('update:expanded', this.isExpanded)
            this.updateExpanded();
        },
        updateExpanded(){
            if (this.isExpanded && !this.song) {
                if (this.debug) {
                    console.log("song loading...")
                }
                if (!isNaN(this.songId)) {
                    this.getSong().then(()=>{
                    if (this.editSong) {
                        this.getTags();
                    }})
                }
            }
        },
        caretClass: function () {
            if (this.debug) {
                console.log(this.isExpanded);
            }
            return this.isExpanded ? "caret-square-down" : "caret-square-up";
        },
        songLoaded() {
            if (this.debug) {
                console.log(this.song)
                console.log(this.song != null)
            }
            return (this.song != null);
        },
        toggleEdit() {
            this.editSong = !this.editSong
            this.isExpanded = this.isExpanded | this.editSong
        },
        getTags() {
            this.$store.dispatch('loadTags')
        },
        doDelete() {
            this.confirm = true;
        },
        doConfirm() {
            if (this.debug) {
                console.log("TODO: actually delete the song");
            }
            this.confirm = false;
        },
        doCancel() {
            if (this.debug) {
                console.log("no");
            }
            this.confirm = false;
        },
        updateTags() {
            this.song.files[0].filetypes.push({
                type: this.newFileType
            })
        },
        async doUpload() {
            this.uploadDisabled.value = true;
            var file = document.getElementById(this.uploadId);
            const filename = file.value.split('\\').pop();
            var formdata = new FormData();
            formdata.set('song', Number(this.songId));
            formdata.set('file', file.files[0]);
            var promise = client('songs/api/upload/', {body: formdata, method: 'POST', headers: {'content-type': 'multipart/form-data',}}, this.prefix.value, true, false)
                .then(result => {
                    if (this.debug) {
                        console.log("Success:", result);
                    }
                    return result;
                })
                .then(result => {
                    this.song.files.push(result);
                    return result;
                })
                .then(this.uploadDisabled.value = false)
                .catch(error => {
                    console.error('Error: ', error) /// TODO: error to output
                });
            if (this.debug) {
                console.log("DONE");
            }
            return promise
        },
        async getSong() {
            if (!this.songId){
                return;
            }
            return this.$store.dispatch('loadSong', {songId: this.songId})
        },
        updateFile(newFile) {
            this.$store.commit('updateSongFile', newFile)
        },
        select(){
          this.getSong().then(
            song=>this.$emit('select', song)
          ).catch(e=>console.log("could not retrieve song data: ", e))
        },
        editComposer(event, index) {
              if (!this.editSong){
                return;
              }
              console.log("composers are saving")
                let composers = []
                for(let i = 0; i < this.composerFullNames.length; i++){
                    let c = i===index? event.target.value : this.composerFullNames[i];
                    let words = c.split(" ")
                    let last = words.pop();
                    let first = words.join(' ');  
                    composers.push({first_name: first, last_name: last})                  
                }
                this.$store.dispatch('updateSongComposers', {songId: this.songId, newComposers: composers})
            },
    },
    components: {
        ConfirmDialog,
        SongFiles,
    },
    inject: ['hash', 'prefix', 'debug'],
}
</script>

<style scoped>

.uploadStyled {
    background-color: #e0b700;
    color: white;
    padding: 0.5rem;
    font-family: sans-serif;
    border-radius: 0.3rem;
    cursor: pointer;
    margin-top: 1rem;
}

.uploadStyled:hover {
    background-color: #ffda33;
}

.button-colors:hover {
    background-color: #ffda33;
}

.button-colors {
    background-color: #e0b700;
}

.uploadStyled[disabled=true] {
    background-color: gray;
    color: lightgray;
    padding: 0.5rem;
    font-family: sans-serif;
    border-radius: 0.3rem;
    cursor: pointer;
    margin-top: 1rem;
}

svg[highlight="true"] {
    color: white;
}

.files-background {
    /* background-color: #6ab6dc; */
    background-color: #EEEEEE;
}
</style>
