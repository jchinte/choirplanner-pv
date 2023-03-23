<template>
    <div v-if="event" class="pa3 pa5-ns">
        <h2 class="f3 fw9 tc">
            <template v-if="!editing">
            {{ title }}
            </template>
            <template v-else>
                <input class="f6 f4-m f3-l" v-model="title">
            </template>
            <button v-if="canEdit" class="f7 link dim ph2 pv2 mb2 dib white button-colors" @click.stop="toggleEdit">
                <font-awesome-icon icon="edit" :highlight="editing" />
            </button>
        </h2>
        <h4 v-if="!editing" class="f5 fw6 tc">{{ mdy }} {{ time }}</h4>
        <h4 v-else><input type="datetime-local" v-model="date" /></h4>
        <div v-if="allTags" class="mw9 center ph3-ns">
            <select-tag-styled v-model="selectedTags" :items="allTags"/>   
        </div>
        <div v-if="editing" class="mw9 ph3-ns">
            <draggable class="dragArea list-group center ph2-ns mw9 ba b--light-silver br2" v-model="segments" handle=".handle" animation="300" easing="cubic-bezier(1,0,0,1)" @change="updateOrder">
                <div v-for="(segment, i) in segments" :key="segment.order" class="list-group-item ph3 pv1 bb b--light-silver">
                    <div class="cf ph2-ns">
                        <div class="fl w-100 pa0">
                            <font-awesome-icon icon="grip-lines" v-if="editing" class="handle" size="2x" />
                        </div>
                        <div class="sans-serif fl w-100 w-25-l pa0 bb bn-l pv2">
                            <input v-model="segments[i].title">           
                        </div>
                        <div v-if="segment.song" class="fl w-100 w-75-l">
                            <SongDetail :songId="segment.song.id" v-model:expanded="segmentVars[segment.id].expanded"  :focused="false" :initTitle="segment.song.title" :initComposers="segment.song.composers" />
                        </div>
                        <div class="fl tl w-100">
                            <span class="ph3"><label :for="'segment'+segments[i].id">visible:</label><input :id="'segment'+segments[i].id" type="checkbox" v-model="segments[i].visible" /></span>
                            <span class="ph3"><a href="#" class="f6 link dim ph3 pv2 mb2 dib white bg-black" @click.stop="addSong(i)">add a song</a></span>
                            <span class="ph3"><button class="f6 link dim ph3 pv2 mb2 dib white bg-red" @click.stop="deleteSegment(i)">delete</button></span>
                        </div>
                    </div>
                </div>
                <div class="ph3 pv3 bb b--light-silver">
                    <button class="f6 link dim ph3 pv2 mb2 dib white bg-purple" @click.stop="addSegment">add a part</button>
                </div>
            </draggable>
        </div>
        <template v-else>
        <div class="mw9 center ph3-ns">
            
            <div v-for="segment in visibleSegments" :key="segment.order" class="outline ph3 pv1">
                <div class="cf ph2-ns">
                    <div class="sans-serif f5 fw8 fl w-100 w-25-l pa0 tc tl-l bb bn-l pv2"><span>{{ segment.title }}</span></div> 
                    <div v-if="segment.song" class="fl w-100 w-75-l">
                        <SongDetail :songId="segment.song.id" 
                                    v-model:expanded="segmentVars[segment.id].expanded" 
                                    v-bind:tagList="segmentVars[segment.id].tagList" 
                                    @update:tagList="updateTags($event, segment.id)" 
                                    :initTitle="segment.song.title" 
                                    :initComposers="segment.song.composers"
                                    :filterTagList="selectedTags"
                                    :focused="false"
                                     />
                    </div>
                    <div v-else class="fl w-100 w-75-l">
                        No song assigned
                    </div>
                </div>
            </div>
        </div>
        </template>
        <button @click="get_ppt">powerpoint</button>
        <!-- </table> -->
    </div>
    <div v-else>
        not loaded
    </div>
    <Modal v-model="dialogOpen"  max-width="800px" >
        <div class="bg-white">
            <song-list v-model:pageNum="pageNum" v-model:query="query" :inDialog="true" pageSize=10 @select="select($event)" @clear="clearSong($event)" />

            <button class="f6 link dim ph2 pv2 mb2 dib white bg-navy" @click="dialogOpen = false">Close</button>
            <button class="f6 link dim ph2 pv2 mb2 dib white bg-red" @click="clearSong">Remove song</button>
        </div>
    </Modal>
    <Modal v-model="confirmOpen" max-width="500px">
        <div class="center mw5 mw6-l hidden ba mv4">
            <h1 class="f4 bg-near-black white mv0 pv2 ph3">Confirm delete</h1>
            <div class="f6 f5-ns lh-copy measure mv0">
                <span v-html="confirmMessage"></span>
            </div>
            <button class="f6 link dim ph3 pv2 mb2 dib white bg-red" @click="confirmDelete">Confirm</button>
            <button class="f6 link dim ph3 pv2 mb2 dib white bg-black" @click="confirmOpen = false">Cancel</button>
        </div>
    </Modal>
</template>

<script>
import SongDetail from './SongDetail.vue'
import { VueDraggableNext } from 'vue-draggable-next'
import SongList from './SongList.vue'
import ConfirmDialog from './ConfirmDialog.vue'
import { Modal } from 'vue-neat-modal'
import { getClasses } from './tagStyles.js'
import { client, isLoggedIn } from '../utils/fetch_utils.js'
import SelectTagStyled from './SelectTagStyled.vue'
export default {
    name: 'EventDetail',
    components: {
        SongDetail,
        draggable: VueDraggableNext,
        SongList,
        ConfirmDialog,
        Modal,
        SelectTagStyled,
    },
    inject: ['hash', 'prefix', 'debug'],
    props: {
            eventId: {
                type: [String, Number],
                default: "",
            },
    },
    data: function(){
        return {
            event: null,
            title: null,
            date: null,
            segments: [],
            isTemplate: false,
            enabled: false,
            dragging: false,
            canEdit: false,
            editing: false,
            saving: false,
            updateTimeoutId: 0,
            songLoading: false,
            
            //add song dialog options
            dialogOpen: false,
            query: '',
            pageNum: 1,
            currentSegmentIndex: -1,

            //Dialog callback
            confirmMessage: '',
            confirmDelete: null,
            confirmOpen: false,

            segmentVars: {},
            allTags: [],
            selectedTags: [],
        }
    },
    computed: {
        mdy(){
            if (this.date){
                let date = new Date(this.date);
                //return (date.getMonth()+1) + "/" + (date.getDate()+1) + "/" + date.getFullYear();
                return date.toLocaleDateString();   
            }
            return "";
        },
        time(){
            if (this.date){
                let date = new Date(this.date);
                let hour = date.getHours()
                let minute = date.getMinutes();
                let hour12 = (hour % 12 === 0)? 12 : (hour % 12);
                console.log(date);
                console.log(date, hour, minute, hour12)
                return hour12 + ":" + String(minute).padStart(2, '0') + (hour>=12?' pm':' am');
            }
            return "";
        },
        visibleSegments(){
            if (this.segments){
                //return this.segments.filter(s=>true)
                return this.segments.filter(s=>s.visible)
            }
            else {
                return [];
            }
            
        },
    },
    watch: {
        eventId(){
            this.getSong();
        },
        date(){
            console.log(new Date(this.date).toUTCString())
        },
        segments: {
            deep: true,
            handler(){
                console.log(this)
                if (!this.segments){
                    return;
                }
                if (this.songLoading){
                    return;
                }
                console.log("segments changed somewhere", this.segments);
                var segmentInfo = this.segments.map(seg=>({ id:seg.id, title:seg.title, song: seg.song?(seg.song.id):null, order:seg.order, visible: seg.visible}))
                console.log("segmentInfo: ", segmentInfo)
                this.updateEvent({id: this.event.id, segments: segmentInfo});
                this.event.segments = this.segments;
            },
        }
    },
    created(){
        if (!isLoggedIn()){
            this.$router.push({name: 'root'})
        }
        else {
            this.getSong();
        }
    },
    methods: {
        toggleEdit(){
            this.editing = !this.editing;
        },
        updateOrder(e) {
            console.log("order changing:", e)
            for(let i=0; i < this.segments.length; i++){
                this.segments[i].order = i+1;
            }
            var segmentOrders = this.segments.map(seg=>({ id: seg.id, order:seg.order, }))
            console.log("segmentOrders: ", segmentOrders)
            this.updateEvent({id: this.event.id, segments: segmentOrders});
            this.event.segments = this.segments;
        },
        updateEvent(updateObject) {
            this.saving = true;
            if (this.updateTimeoutId){
                clearTimeout(this.updateTimeoutId);
                this.updateTimeoutId = 0;
            }
            this.updateTimeoutId = setTimeout(()=>{
                console.log("Committing object ", updateObject)
                client('events/api/events/'+this.event.id+'/', {body: updateObject, method: 'PATCH',}, this.prefix.value, false)
                    .then(response => {
                        this.saving = false;
                        console.log(response);
                        return response
                    })
                    .catch(error => console.log("Did not update :", error));
            }, 2000);
        },
        getSong() {
            this.songLoading = true;
            client('events/api/events/'+this.eventId+'/', {method: 'OPTIONS',}, this.prefix.value)
                .then(data => {
                    console.log(data);
                    this.canEdit = ('actions' in data && 'PUT' in data['actions'])
                })
                .catch(error=>{
                    console.log(error);
                    this.event = null;
                    this.title="";
                    this.date="";
                    this.segments=[];
                })               
            client('events/api/events/'+this.eventId+'/', ({}), this.prefix.value)
                .then(data => {
                    this.event = (('detail' in data) ? null : data)
                    return this.event;
                })
                .then(event => {
                    this.title = event.title;
                    console.log(new Date(event.date));
                    let date = new Date(event.date)
                    //"yyyy-MM-ddThh:mm"
                    this.date = (""+date.getFullYear() + "-" 
                                + String(date.getMonth()+1).padStart(2, "0") + "-" 
                                + String(date.getDate()).padStart(2, "0") + "T" 
                                + String(date.getHours()).padStart(2, "0") + ":"
                                + String(date.getMinutes()).padStart(2, "0")  
                    )
                    console.log(this.date);
                    //this.date = this.date.substring(0, this.date.length-1)
                    this.isTemplate = event.is_template;
                    this.segments = event.segments;
                    this.segmentVars = {}
                    for(let seg of this.segments){
                        this.segmentVars[seg.id]=({expanded: true, tagList: []})
                    }
                    setTimeout(()=>this.songLoading = false, 500);
                    return event;
                })
                .catch(error=>{
                    console.log(error);
                    this.title="";
                    this.date="";
                    this.segments=null;
                })
            //console.log(this.song);
            return this.event
        },
        get_ppt(){
            client('events/api/events/'+this.eventId+'/', ({responseType: 'blob', headers:{Accept:'application/vnd.openxmlformats-officedocument.presentationml.presentation'}}), this.prefix.value, false)
            .then(response=>response.blob())
            .then(blob=>
             {
                 console.log(blob)
                var fileURL = window.URL.createObjectURL(blob);
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', this.title+'.pptx');
                document.body.appendChild(fileLink);

                fileLink.click();
                return blob;
            })
            .then(res=>console.log(res))
        },
        addSegment(){
            client('events/api/songsegment/', {body: {
                order: this.segments.length + 1,
                title: "new segment",
                event: this.event.id,
            }}, this.prefix.value)
                .then(data => this.segments.push(data))
                .catch(e=>console.log(e))
        },
        deleteSegment(i){
            this.confirmDelete=function(){
                client('events/api/songsegment/'+this.segments[i].id+'/', {method: 'DELETE'}, this.prefix.value, false)
                    .then(()=>this.segments.splice(i, 1))
                    .then(()=>this.updateOrder("From deleting"))
                    .then(()=>this.confirmOpen = false)
                    .catch(e=>console.log(e))
            };
            this.confirmMessage="Are you sure you want to delete <b>" + this.segments[i].title + "</b>?";
            this.confirmOpen = true;
        },
        addSong(i){
            this.currentSegmentIndex = i;
            this.dialogOpen = true;
        },
        select(song){
            console.log("event detail song id is ", song)
            if (this.currentSegmentIndex>=0){
                this.segments[this.currentSegmentIndex].song = song;
                console.log(this.segments);
                this.currentSegment = -1;
                this.dialogOpen = false;
            }
        },
        clearSong(){
            if (this.currentSegmentIndex>=0){
                this.segments[this.currentSegmentIndex].song = null;
                this.currentSegment = -1;
                this.dialogOpen = false;
            }
        },
        expandAll(){
            console.log("expanding")
            for (let id in this.segmentVars){
                this.segmentVars[id].expanded = true;
            }
        },
        updateTags(e, segmentid){
            console.log("in updateTags: ", e, segmentid)
            this.segmentVars[segmentid].tagList = e;
            
            let tagsSet = new Set()
            for (let id in this.segmentVars){
                if (this.segmentVars[id].tagList && this.segmentVars[id].tagList instanceof Array){
                    for (let tag of this.segmentVars[id].tagList){
                        tagsSet.add(tag.type);
                    }
                }
                else {
                    console.log("no list: ", this.segmentVars[id].tagList)
                }
            }
            this.allTags = [...tagsSet]
        },
        getClasses(t){
            return getClasses(t);
        },
    }
}
</script>

<style scoped>

.button-colors:hover {
    background-color: #ffda33;
}

.button-colors {
    background-color: #e0b700;
}

svg[highlight="true"] {
    color: white;
}
.segment-list-move {
    transition: transform 0.8s ease;
}
.custom-select {
     position: relative;
     display: flex;
     flex-direction: column;
     border-width: 0 2px 0 2px;
     border-style: solid;
     border-color: #394a6d;
}
 .custom-select > option{
     position: absolute;
     display: block;
     top: 100%;
     left: 0;
     right: 0;
     border: 2px solid #394a6d;
     border-top: 0;
     /* background: #fff; */
     transition: all 0.5s;
     opacity: 0;
     visibility: hidden;
     pointer-events: none;
     z-index: 2;
}
</style>