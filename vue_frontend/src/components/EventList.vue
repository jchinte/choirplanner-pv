<template>
<div class="">
    <label for="eventlist-query">Search </label>
    <input id="eventlist-query" v-model="_title" />
    <label for="eventlist-start">Start date </label>
    <input id="eventlist-start" type="date" v-model="_startDate" />
    <label for="eventlist-end">End date </label>
    <input id="eventlist-end" type="date" v-model="_endDate" />
    <button v-if="canCreateTemplate" class="f6 link dim ph2 pv2 mb2 dib white bg-blue-1" @click="newOpen = true">Create a new template</button>
    <div class="ph3">
        <button class="f6 link dim ph2 pv2 mb2 dib white bg-blue-1" @click="goPreviousPage()">&#10094;</button>
        <template v-for="(pageInfo, index) in pageNumbers" :key="index">
            <button :class="[].concat('f6 link dim ph2 pv2 mb2 white dn'.split(' '), 
                [pageInfo.current && 'current-page', 
                pageInfo.smDisplay && 'dib',
                pageInfo.medDisplay && 'dib-m', 
                pageInfo.lgDisplay && 'dib-l',
                pageInfo.current && 'bg-indigo-4',
                !pageInfo.current && 'bg-blue-2',
                ])" @click.stop="goToPage(pageInfo.page)">
                {{ pageInfo.page }}
            </button>
        </template>
        <button class="f6 link dim ph2 pv2 mt2 mb2 dib white bg-blue-1" @click="goNextPage()">&#10095;</button>
    </div>
    <div v-if="eventList && currentPage">
        <!-- <ul class="w3-ul"> -->
        <div v-for="(event, index) in currentPage" :key="index" class="pv3 bt bb">
            <router-link 
                    :to="{name: 'event-detail', params: {eventId: event.id} }" 
                    class="f5 link dim black">
                {{ event.title }} {{ getDate(event.date) }} {{ getTime(event.date) }}
            </router-link>
            <!-- <SongDetail :eventId="song.id" :initTitle="song.title" :initComposers="song.composers" 
                        :expanded="false" :focused="false" :inDialog="inDialog" 
                        @select="select($event)" /> -->
        </div>
        <!-- </ul> -->
    </div>
</div>
<Modal v-model="newOpen" min-height="400px" max-width="600px">
 
    <div class="center bg-white pv3 ph3">
           <h3>New event...</h3>
        <div class="w90 pv3 ph3">
            <label for="newtitle">Title </label>
            <input id="newtitle" v-model="newTitle" />
        </div>
        <div class="w90 pv3 ph3">
        <label for="newdate">Date: </label>
        <input id="newdate" type="datetime-local" v-model="newDate" />
        </div>
        <div class="w90 pv3 ph3">
        <label for="newis-template">is a template</label>
        <input id="newis-template" type="checkbox" v-model="newIsTemplate" />
        </div>
        <select v-model="selectedTemplate">
            <option value="blank">new empty event</option>
            <option v-for="t in templates" v-bind:value="t.id" :key="t.id">{{ t.title }}</option>
        </select>
        <div>
            <button class="f6 link dim ph2 pv2 mb2 dib white bg-navy" @click="createEvent()">Create a new template</button>
            <button class="f6 link dim ph2 pv2 mb2 dib white bg-navy" @click="newOpen=false">Close</button>
        </div>
    </div>
</Modal>
</template>

<script>
// import SongDetail from './SongDetail.vue'
import {
    positiveNumber
} from '../utils/validators.js'
import { Modal } from 'vue-neat-modal'
import { client, isLoggedIn } from '../utils/fetch_utils.js'
export default {
    name: 'EventList',
    components: {
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
            default: 20,
            validator: positiveNumber,
        },
        title: {
            type: String,
            default: '',
        },
        startDate: {
            type: [String, Date],
            default: '',
        },
        endDate: {
            type: [String, Date],
            default: '',
        },
        inDialog: {
            type: Boolean,
            default: false,
        },
    },
    emits: ['update:title', 'update:startDate', 'update:endDate', 'update:pageNum', 'select'],
    data: function () {
        return {
            eventList: null,
            _pageNum: Number(this.pageNum),
            _pageSize: Number(this.pageSize),
            _title: this.title ? this.title : '',
            _startDate: this.startDate? (this.startDate instanceof Date? this.startDate :  new Date(this.StartDate)) : new Date(Date.now()),
            _endDate: this.endDate? new Date(this.endDate) : '',
            filteredEventList: [],
            newOpen: false,
            includeTemplates: false,
            newTitle: '',
            newDate: null,
            newIsTemplate: false,
            selectedTemplate: "blank",
            canCreateTemplate: false,
        }
    },
    computed: {
        pageNumbers() {
            if (this.filteredEventList) {
                var pages = [];
                const min = 1;
                const max = Math.floor(this.filteredEventList.length / this._pageSize) + 1;
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
                    smallMin = Math.max(min, this._pageNum - Math.floor(smallWidth / 2) + 1);
                    smallMax = Math.min(max, this._pageNum + Math.floor(smallWidth / 2));
                }
                if (this._pageNum <= midWidth / 2) {
                    midMin = 1;
                    midMax = Math.min(midWidth, max);
                } else if (this._pageNum >= (max - midWidth / 2 + 1)) {
                    midMin = Math.max(1, max - midWidth + 1);
                    midMax = max;
                } else {
                    midMin = Math.max(min, this._pageNum - Math.floor(midWidth / 2) + 1);
                    midMax = Math.min(max, this._pageNum + Math.floor(midWidth / 2));
                }
                if (this._pageNum <= lgWidth / 2) {
                    lgMin = 1;
                    lgMax = Math.min(lgWidth, max);
                } else if (this._pageNum >= (max - lgWidth / 2 + 1)) {
                    lgMin = Math.max(1, max - lgWidth + 1);
                    lgMax = max;
                } else {
                    lgMin = Math.max(min, this._pageNum - Math.floor(lgWidth / 2) + 1);
                    lgMax = Math.min(max, this._pageNum + Math.floor(lgWidth / 2));
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
            return this.filteredEventList ? this.filteredEventList.slice(start, start + this._pageSize) : []
        },
        templates(){
            if (!this.eventList) {
                return [];
            }
            var es =this.eventList.filter(event=>event.is_template)
            es.sort((a, b)=>a.date<b.date?1:-1)
            return es
        }
    },
    watch: {
        _title() {
            this.setFilteredEventList();
        },
        _startDate() {
            this.setFilteredEventList();
        },
        _endDate() {
            this.setFilteredEventList();
        },

    },
    created() {
        if (!isLoggedIn()){
            console.log("logging out due to no localstorage")
            this.$router.push({name: 'root'})
        }
        this.getEventList();
    },
    methods: {
        setFilteredEventList() {
            if (!this.eventList) {
                return [];
            }

            function titleFilter(item) {
                return event => event.title.toLocaleLowerCase().includes(item);
                //return songList.filter(song => song.title.toLocaleLowerCase().includes(item))
            }

            const beforeDateFilter = (item)=>{
                return this._endDate? new Date(item.date) <= new Date(this._endDate) : true
            }

            const afterDateFilter = (item)=>{
                return this._startDate? new Date(item.date) >= new Date(this._startDate) : true
            }
            const templateFilter = (item)=>this.includeTemplates || (!item.is_template)
            //const items = title.split(/\s+/).map(w => w.toLocaleLowerCase());
            var filtered = this.eventList.filter(beforeDateFilter)
                                         .filter(afterDateFilter)
                                         .filter(templateFilter)
            if (this._title) {
                const items = this._title.split(/\s+/).map(w => w.toLocaleLowerCase());
                for (let q of items) {
                    filtered = filtered.filter(titleFilter(q))
                }
            }
            filtered.sort((a, b)=>a.date<b.date?1:-1)
            this.filteredEventList = filtered
            return this.filteredEventList
        },
        getEventList() {
            client('events/api/events', {}, this.prefix.value)
                .then(data => {
                    this.eventList = (('detail' in data) ? [] : ('results' in data ? data.results : data.values))
                    this.canCreateTemplate = ('can_create_template' in data) && data.can_create_template
                    return this.eventList;
                })
                .then(() => this.setFilteredEventList())
                //.then(() => this.setPageNumbers())
                .catch(e => console.log(e));
            //return this.songsList.value
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
            console.log(e);
            this.$emit('select', e);
        },
        getDate(d){
            return new Date(d).toLocaleDateString();
        },
        getTime(d){
            return new Date(d).toLocaleTimeString();
        },
        createEvent(){
            let newEvent = {
                title: this.newTitle,
                date: this.newDate,
                is_template: this.newIsTemplate,
            }
            if (this.selectedTemplate !=="blank"){
                newEvent['template'] = this.selectedTemplate
            }
            client('events/api/events/',{body: newEvent}, this.prefix.value)
                    .then(data => {
                        this.$router.push({name: 'event-detail', params: {eventId: data.id}})
                    })
                    .catch(e => console.log(e));
                //return this.songsList.value
        },
    },
}
</script>

<style scoped>
.bg-off-white {
    background-color: #dddddd;
}
</style>
