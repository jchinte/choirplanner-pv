<template>
<div class="mw9 w-100 ph3-ns">
    <div class="cf ph2-ns">
        <div class="fl w-25 w-20-ns pa2">
            <!-- <font-awesome-layers class="fa-fw" v-if="editSong">
                <font-awesome-icon icon="circle" style="color:Tomato" />
                <font-awesome-icon icon="times" inverse transform="shrink-3" />
            </font-awesome-layers> -->
            <font-awesome-icon icon="times-circle" style="color:Tomato" size="2x" v-if="editSong"  @click="doDelete" />
            <a :href="file.file">
                <img v-if="file.thumbnail" width="240" class="shadow-3" :src="prefix.value + file.thumbnail" />
                <font-awesome-icon v-else :icon="getIcon(file.file)" size="2x" />
                <!-- <button class="f5 no-underline black bg-animate hover-bg-black hover-white inline-flex items-center pa3 ba border-box button-colors ">download</button> -->
            </a>
        </div>
        <div class="fl w-75 w-80-m w-40-l tl">
            <template v-if="editSong">
                <span v-for="(t, i) in myTypes" :key="i" :class="getClasses(t)" @click="confirmDeleteTag(i)" >{{ t.type }}</span>
                <select v-if="editSong" @change="addTag" v-model="newFileType">
                    <option disabled value="">Add a tag...</option>
                    <option v-for="tag in allTags" :key="tag.id" :value="tag">{{ tag }}</option>
                </select>
            </template>
            <template v-else>
                <span v-for="t in filteredTags" :key="t.type" :class="getClasses(t)">{{ t.type }}</span>
            </template>
        </div>
        <div v-if="file.file.split('.').pop()==='mp3'" class="fl w-100 w-40-l">
            <audio  controls :src="file.file" class="w-100" />
        </div>
    </div>
    
</div>
<Modal v-model="deleteTagOpen" max-width="500px">
    <div class="bg-white">
    <div>Do you want to delete {{ deleteTagName }}?</div>
    <button class="f6 grow no-underline br-pill ph3 pv2 mb2 dib white bg-washed-red" @click="deleteTagCallback">Delete</button>
    <button class="f6 grow no-underline br-pill ph3 pv2 mb2 dib white bg-black" @click="deleteTagOpen=false">Cancel</button>
    </div>
</Modal>
<Modal v-model="confirm" max-width="500px">
    <div class="bg-white">
    <div>Are you sure want to delete this file? You can't undo this.</div>
    <button class="f6 grow no-underline br-pill ph3 pv2 mb2 dib white bg-washed-red" @click="doConfirm">Delete</button>
    <button class="f6 grow no-underline br-pill ph3 pv2 mb2 dib white bg-black" @click="doCancel">Cancel</button>
    </div>
</Modal>
</template>

<script>

import ConfirmDialog from './ConfirmDialog.vue'
import { Modal } from 'vue-neat-modal'
import { getClasses } from './tagStyles.js'
export default {
    name: 'SongFiles',
    props: {
        file: Object,
        editSong: Boolean,
        tagList: {
            type:Array,
            default:null,
        },
        //id: Number,
        //first_line: String,
        //composers: Array,
        //files: Array,
    },
    emits: ['delete:file', 'update:file'],
    data() {

        return {
            confirm: false,
            //allTags: [],
            newFileType: '',
            myTypes: [...this.file.filetypes],

            deleteTagOpen: false,
            deleteTagCallback: null,
            deleteTagName: '',
        }
    },
    created: function () {
        this.getTags()
    },
    computed: {
        filteredTags(){
            if (this.tagList && this.tagList.length>0){
                return this.myTypes.filter(tag=>this.tagList.includes(tag.type));
            }
            return this.myTypes;
        },
        allTags(){
            return this.$store.state.tags;
        }
    },
    methods: {
        getIcon(filename) {
            if (this.debug){
            console.log(filename);
            }
            const type = filename.split('.').pop().split('?')[0]
            if (this.debug){
            console.log(type);
            }
            switch (type) {
                case "mp3":
                    return "file-audio";
                case "ppt":
                case "pptx":
                    return "file-powerpoint";
                default:
                    return "file-download";
            }
            return "file-download";
        },
        getClasses(t) {
            return getClasses(t);
        },
        getTags() {
            this.$store.dispatch('loadTags')
        },
        doDelete() {
            this.confirm = true;
        },
        doConfirm() {
            this.$store.dispatch('deleteSongFile', {file: this.file})
                .then(res=>{
                    this.confirm=false;
                    return res;
                })
                .catch(error => {
                    console.error('Error: ', error) //TODO: output to page
                });
        },
        doCancel() {
            if (this.debug){
            console.log("no");
            }
            this.confirm = false;
        },
        addTag(){
            this.myTypes.push({
                type: this.newFileType
            });
            this.updateTags()
        },
        updateTags() {

            let unique = [...new Set(this.myTypes.map(t => t.type))];
            var uniquemap = [...unique.map(type => ({
                type
            }))]
            const o = {
                filetypes: uniquemap
            };
            this.$store.dispatch('updateSongFile', {file: this.file, update: o})
        },
        deleteTag(i){
            this.myTypes.splice(i, 1)
            this.updateTags();
            this.deleteTagCallback = null;
            this.deleteTagName = '';
            this.deleteTagOpen = false;
        },
        confirmDeleteTag(i){
            this.deleteTagName = this.myTypes.type;
            this.deleteTagCallback = ()=>{
                this.deleteTag(i);
            }
            this.deleteTagOpen = true;
        },
    },
    components: {
        ConfirmDialog,
        Modal,
    },
    inject: ['hash', 'prefix', 'debug'],
}
</script>

<style scoped>

</style>
