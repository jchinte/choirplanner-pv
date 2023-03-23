<template>
<div class="fs-normal sans-serif f5">

    <div class="pv2 center tc">
        <button class="tc f6 link dim ph2 pv2 mb2 dib white bg-blue-1" @click="createOpen = true">Create Song</button>
    </div>
    <div class="tc pv2">
        <label for="songlist-query">Search </label>
        <input id="songlist-query" v-model="_query">
    </div>
    <div class="ph3 tc">
        <button class="f6 link dim ph2 pv2 mb2 dib white bg-blue-1" @click="goPreviousPage()">&#10094;</button>
        <template v-for="(pageInfo, index) in pageNumbers" :key="index">
            <button :class="[].concat('f6 link dim ph2 pv2 mb2 white dn'.split(' '), 
                [pageInfo.current && 'current-page', 
                pageInfo.smDisplay && 'dib',
                pageInfo.medDisplay && 'dib-m', 
                pageInfo.lgDisplay && 'dib-l',
                pageInfo.current && 'bg-indigo-4',
                !pageInfo.current && 'bg-blue-1',
                ])" @click.stop="goToPage(pageInfo.page)">
                {{ pageInfo.page }}
            </button>
        </template>
        <button class="f6 link dim ph2 pv2 mb2 dib white bg-blue-1" @click="goNextPage()">&#10095;</button>
    </div>
    <div v-if="currentPage">
        <!-- <ul class="w3-ul"> -->
        <div v-for="(song, index) in currentPage" :key="index" class="bb bt">
            <SongDetail :songId="song.id" :initTitle="song.title" :initComposers="song.composers" 
                        :expanded="false" :focused="false" :inDialog="inDialog" 
                        @select="select($event)" />
        </div>
        <!-- </ul> -->
    </div>
</div>

    <Modal v-model="createOpen" max-width="700px">
        <div class="center mw6 ba mv4 ph3 bg-white pv4">
            
            <h1 class="f4 bg-near-black white mv0 pv2 ph3">Add Song</h1>
            <div class="f6 f5-ns lh-copy measure mv0">
                <span>Create a song:</span>
                <div>
                    <label for="song-title">Title:</label>
                    <input v-model="newSongTitle" id="song-title" />
                </div>
                <div>
                    <label for="song-Lyrics">Lyrics:</label>
                    <textarea v-model="newSongLyrics" id="song-lyrics" />
                </div>
                <button class="mr3 f6 link dim ph3 pv2 mb2 dib white bg-red" @click="createSong()">Confirm</button>
                <button class="mr3 f6 link dim ph3 pv2 mb2 dib white bg-black" @click="createOpen = false">Cancel</button>
            </div>
            
        </div>
    </Modal>
</template>

<script>
import SongDetail from './SongDetail.vue'
import { Modal } from 'vue-neat-modal'
import {
    positiveNumber
} from '../utils/validators.js'

export default {
    name: 'SongList',
    components: {
        SongDetail,
        Modal,
    },
    inject: ['hash', 'prefix', 'debug'],
    props: {
        pageNum: {
            type: [Number, String],
            default: 1,
            validator: positiveNumber,
        },
        pageSize: {
            type: [Number, String],
            default: 10,
            validator: positiveNumber,
        },
        title: {
            type: String,
            default: '',
        },
        composer: {
            type: String,
            default: '',
        },
        query: {
            type: String,
            default: '',
        },
        inDialog: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['update:query', 'update:composer', 'update:title', 'update:pageNum', 'select'],
    data: function () {
        return {
            _columns: ['title', 'composers', 'url'],
            songList: null,
            _pageNum: Number(this.pageNum),
            _pageSize: Number(this.pageSize),
            _query: this.query ? this.query : '',
            createOpen: false,
            newSongTitle:'',
            newSongLyrics:'',
            //filteredSongList: [],
        }
    },
    computed: {
        pageNumbers() {
            if (this.filteredSongList) {
                var pages = [];
                const min = 1;
                const max = Math.floor(this.filteredSongList.length / this._pageSize) + 1;
                const smallWidth = 8;
                const lgWidth = 12;
                const midWidth = 8;
                var smallMin, smallMax;
                var midMin, midMax;
                var lgMin, lgMax;

                //adjust page to stay in range
                this._pageNum = Math.max(min, Math.min(max, this._pageNum));

                if (this._pageNum <= smallWidth / 2) {
                    smallMin = 1;
                    smallMax = Math.min(smallWidth, max);
                } else if (this.pageNum >= (max - smallWidth / 2 + 1)) {
                    smallMin = Math.max(1, max - smallWidth + 1);
                    smallMax = max;
                } else {
                    smallMin = this._pageNum - Math.floor(smallWidth / 2) + 1;
                    smallMax = this._pageNum + Math.floor(smallWidth / 2);
                }
                if (this._pageNum <= midWidth / 2) {
                    midMin = 1;
                    midMax = Math.min(midWidth, max);
                } else if (this._pageNum >= (max - midWidth / 2 + 1)) {
                    midMin = Math.max(1, max - midWidth + 1);
                    midMax = max;
                } else {
                    midMin = this._pageNum - Math.floor(midWidth / 2) + 1;
                    midMax = this._pageNum + Math.floor(midWidth / 2);
                }
                if (this._pageNum <= lgWidth / 2) {
                    lgMin = 1;
                    lgMax = Math.min(lgWidth, max);
                } else if (this._pageNum >= (max - lgWidth / 2 + 1)) {
                    lgMin = Math.max(1, max - lgWidth + 1);
                    lgMax = max;
                } else {
                    lgMin = this._pageNum - Math.floor(lgWidth / 2) + 1;
                    lgMax = this._pageNum + Math.floor(lgWidth / 2);
                }
                for (var i = Math.min(smallMin, midMin, lgMin); i <= Math.max(smallMax, midMax, lgMax); i++) {
                    pages.push({
                        page: i,
                        pageSize: this.pageSize,
                        lgDisplay: (i >= lgMin && i <= lgMax),
                        medDisplay: (i >= midMin && i <= midMax),
                        smDisplay: (i >= smallMin && i <= smallMax),
                        current: (i == this._pageNum),
                    })
                }
                return pages;
            }
            return [{
                page: 1,
                pageSize: this._pageSize,
                medDisplay: true,
                smDisplay: true,
                current: true,
            }];
        },
        currentPage() {
            const start = (this._pageNum - 1) * this._pageSize
            return this.filteredSongList.length ? this.filteredSongList.slice(start, start + this._pageSize) : []
        },
        filteredSongList(){
            return this.$store.getters.getSongsFiltered(this._query.split(/\s+/).map(w => w.toLocaleLowerCase()))
        },
        songCreator(){
            return this.$store.state.songCreator;
        },
    },
    watch: {
        // _query() {
        //     this.setFilteredSongList();
        // }
    },
    created() {
        this.getSongList();
    },
    methods: {
        getSongList() {
            this.$store.dispatch('loadSongs');
        },
        goNextPage() {
            this.$emit('update:pageNum', this.pageNum + 1);
            this._pageNum++;
        },
        goPreviousPage() {
            this.$emit('update:pageNum', this.pageNum > 1 ? this.pageNum - 1 : 1);
            this._pageNum = this._pageNum>1? this._pageNum - 1 : 1;
        },
        goToPage(page) {
            this.$emit('update:pageNum', page);
            this._pageNum = page;
        },
        select(e){
            this.$emit('select', e);
        },
        createSong(){
            if (!this.newSongTitle || !this.newSongLyrics){
                //error
            } else {
                this.$store.dispatch('createSong', {title: this.newSongTitle, first_line: this.newSongLyrics})
                .then(data=>{
                    if (this.inDialog){
                        this.$emit('select', data);
                    } else {
                        this.$router.push({name: 'song-detail', params: {songId: data.id}})
                    }
                })
            }
        }
    },
}
</script>

<style scoped>
.bg-off-white {
    background-color: #dddddd;
}
</style>
