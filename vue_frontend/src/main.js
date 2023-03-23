import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import { library } from '@fortawesome/fontawesome-svg-core'

import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { faDownload } from '@fortawesome/free-solid-svg-icons'
import { faFileDownload } from '@fortawesome/free-solid-svg-icons'
import { faFileAudio } from '@fortawesome/free-solid-svg-icons'
import { 
    faFilePowerpoint, 
    faFileUpload, 
    faSpinner, 
    faCircle, 
    faTimes, 
    faTimesCircle, 
    faEdit, 
    faCaretSquareUp, 
    faCaretSquareDown,
    faExpand,
    faCompress,
    faGripLines
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// <i class="fas fa-spinner fa-pulse"></i>
import { createWebHistory, createRouter } from 'vue-router'
import 'vue-neat-modal/dist/vue-neat-modal.css'
import { store } from './utils/store.js'
library.add(faUserSecret);
library.add(faDownload)
library.add(faFileDownload)
library.add(faFileAudio)
library.add(faFilePowerpoint)
library.add(faFileUpload)
library.add(faSpinner, faCircle, faTimes, faTimesCircle, faEdit, faCaretSquareUp, faCaretSquareDown, faExpand, faCompress, faGripLines)
import SongList from './components/SongList.vue'
// import SongList2 from './components/SongList2.vue'
import SongDetail from './components/SongDetail.vue'
// import MassPlannerApp from './components/Planner.vue'
import EventDetail from './components/EventDetail.vue'
import EventList from './components/EventList.vue'
import Home from './components/Home.vue'
import Login from './components/Login.vue'
import BlogLists from './components/BlogLists.vue'
import BlogPost from './components/BlogPost.vue'
const history = createWebHistory();
const routes = [{
    path: '/app/songs',
    name: 'song-list',
    components:{
         default: SongList,
         nav: Login,
    },
    props: {
        default: route => ({
            initPageNum: route.query.page,
            initPageSize: route.query.pageSize,
            initTitle: route.query.title,
            initComposer: route.query.composer,
         }),
         nav: false,
    }
},
{
    path: '/app/songs/:songId',
    name: 'song-detail',
    components: {
        default: SongDetail,
        nav: Login,
    },
    props:{
        default: true,
        nav: false,
    }
},
{
    path: '/app/',
    name: 'main',
    components: {
        default: SongList,
        nav: Login,
    }
},
{
    path: '/app/events/',
    name: 'event-list',
    components: {
        default: EventList,
        nav: Login,
    }
},
{
    path: '/app/events/:eventId',
    name: 'event-detail',
    components: {
        default: EventDetail,
        nav: Login,
    },
    props: {
        default: route=> ({
            eventId: route.params.eventId,
        }),
        nav: false,
    },
},
{
    path: '/',
    name: 'root',
    components: {
        default: Home,
    }
},
{
    path: '/blog/',
    name: 'blog',
    components: {
        default: BlogLists,
        nav: Login,
    }
},
{
    path: '/blog/:slug',
    name: 'blog-post',
    components: {
        default: BlogPost,
        nav: Login,
    },
    props:{
        default: true,
        nav:false,
    }
},
// {
//     path: '/blog/posts',
//     name: 'blog-posts',
//     components: {
//         default: PageContainer,
//         nav: Login,
//     },
//     props: {
//         default: 
//     }
// },
]
  
const router = createRouter({
    history,
    routes,
})
const a = createApp(App)
a.use(router)
a.use(store)
a.component('font-awesome-icon', FontAwesomeIcon)
a.mount('#app')


//a.use(ClientTable, [options = {}], [useVuex = false], [theme = 'bootstrap3'], [template = 'default']);
