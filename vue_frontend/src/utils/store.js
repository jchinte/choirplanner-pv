import { client, prefix } from './fetch_utils.js'
import { createStore } from 'vuex'
const store = createStore({
    state: {
        username: null,
        token: null,
        events: [], //event list for list view
        songs: [],  //song list for list view
        tags: [],  //tag list
        tagLoading: false,
        eventDetails: {},
        songDetails: {},
        songTitleProcess: null,
        songComposersProcess: null,
        fileDetails: {},
        songEditor: false,
        songCreator: false,
        eventEditor: false,
        
    },
    getters: {
        loggedIn(state){
            return state.token != null;
        },
        getSongsFiltered: (state) => (items) => {
            if (!state.songs) {
                return [];
            }
            if (!items){
                return state.songs;
            }
            const joinComposers = function (song) {
                return song.composers.reduce((s, next) => s += ' ' + next.first_name + ' ' + next.last_name, '').trim()
            }
            const joinTags = function (song) {
                return song.tags.reduce((s, next) => s += ' ' + next.tag_name, '').trim()
            }

            function titleFilter(item) {
                return song => song.title.toLocaleLowerCase().includes(item);
                //return songList.filter(song => song.title.toLocaleLowerCase().includes(item))
            }

            function composerFilter(item) {
                return song => joinComposers(song).toLocaleLowerCase().includes(item);
                //return items.reduce((songLst, q) => songLst.filter(song => joinComposers(song).toLocaleLowerCase().includes(q)), songList)
            }

            function tagFilter(item) {
                return song => joinTags(song).toLocaleLowerCase().includes(item)
                //return items.reduce((songLst, q) => songLst.filter(song => joinTags(song).toLocaleLowerCase().includes(q)), songList)
            }

            var filterSet = state.songs.reduce((s, song) => s.add(song), new Set())
            for (let q of items) {
                var collectSet = new Set()
                const filterArray = [...filterSet]

                //perform the query on each category separately
                collectSet = filterArray.filter(titleFilter(q)).reduce((collSet, next) => collSet.add(next), collectSet) //Set.from(filterArray.filter(titleFilter(q)));
                collectSet = filterArray.filter(composerFilter(q)).reduce((collSet, next) => collSet.add(next), collectSet)
                collectSet = filterArray.filter(tagFilter(q)).reduce((collSet, next) => collSet.add(next), collectSet)

                //collect into a sorted set
                filterSet = ([...collectSet]).reduce((buildSet, item) => filterSet.has(item) ? buildSet.add(item) : buildSet, new Set())

            }
            return Array.from(filterSet).sort((a, b) => a.title.localeCompare(b.title));
        },
        getSongTitle:(state)=>(songId)=>{
            if (!state.songDetails[songId]){
                return null;
            }
            return state.songDetails[songId].title;
        },
        getSongComposers:(state)=>(songId)=>{
            if (!state.songDetails[songId]){
                return null;
            }
            return state.songDetails[songId].composers;
        },
        getSongComposerFullNames:(state)=>(songId)=>{
            if (!state.songDetails[songId]){
                return null;
            }
            return state.songDetails[songId].composers.map(c => [c.first_name, c.last_name].join(' '));
        },
        getSong: (state) => (songId) => {
            return state.songDetails[songId];
        },
    },
    mutations: {
        setTagList(state, tagList) {
            state.tags = tagList;
        },
        setSongList(state, songList) {
            state.songs = songList
        },
        login(state, {username, token}){
            state.username = username
            state.token = token
        },
        logout(state){
            state.username = null;
            state.token = '';
        },
        setSongDetail(state, songObj){
            state.songDetails[songObj.id] = songObj;
            state.songEditor = (songObj.can_delete_song)
        },
        removeSongFile(state, file){
            state.songDetails[file.song].files = state.songDetails[file.song].files.filter(f=>f.id != file.id)
        },
        updateSongFile(state, file){
            state.songDetails[file.song].files = state.songDetails[file.song].files.map(f=>f.id==file.id? file : f)
        },
        startTagLoading(state){
            state.tagLoading = true;
        },
        stopTagLoading(state){
            state.tagLoading = false;
        },
        setSongTitle(state, {songId, newTitle}){
            state.songDetails[songId].title = newTitle;
        },
        setSongTitleProcess(state, pid){
            state.songTitleProcess = pid;
        },
        clearSongTitleProcess(state){
            state.songTitleProcess = null;
        },
        setSongComposers(state, {songId, newComposers}){
            state.songDetails[songId].composers = newComposers;
        },
        setSongComposersProcess(state, pid){
            state.songComposersProcess = pid;
        },
        clearSongComposersProcess(state){
            state.songComposersProcess = null;
        },
        addComposer(state, songId){
            state.songDetails[songId].composers.push("");
        },
        setSongCreator(state, isCreator){
            state.songCreator = isCreator;
        },
    },
    actions: {
        loadTags({ state, commit }) {
            if (state.tagLoading){
                console.log('loading in progress')
                return
            }
            commit('startTagLoading')
            console.log('start tag loading')
            if (!state.tags.length)
                client('songs/api/filetypes/', ({}), prefix)
                    .then(data=>Array.isArray(data)? data.map(entry=>entry.type) : [])
                    .then(tagList=>{
                        commit('stopTagLoading')
                        console.log("loaded list: ", tagList)
                        commit('setTagList', tagList)
                        return tagList;
                    }).catch(response=>{
                        console.log("Caught in store: ", response)
                        commit('stopTagLoading')
                    }
                )
        },
        loadSongs({ state, commit }) {
            if (!state.songs.length){
                client('songs/api/songs/', ({}), prefix)
                .then(data => {
                    const songList = (('detail' in data) ? [] : ('results' in data ? data.results : data))
                    commit('setSongList', songList)
                    commit('setSongCreator', data.can_create_song)
                    return songList;
                })
            } else {
                console.log("not loading because ", state.songs)
            }
        },
        loadSong({ state, commit }, { songId }) {
            if (!state.songDetails[songId]){
                return client('songs/api/songs/'+songId, ({}), prefix)
                    .then(data => {
                        const song = (('detail' in data) ? null : data)
                        commit('setSongDetail', song)
                        return song;
                    })
            }
        },
        createSong({ state, commit }, { title, first_line }) {

            return client('songs/api/songs/', ({method: 'POST', body: {title, first_line}}), prefix)
                .then(data => {
                    console.log('created ', data)
                    const song = (('detail' in data) ? null : data)
                    commit('setSongDetail', song)
                    return song;
                })
        
        },
        async deleteSongFile({state, commit}, { file }){
            console.log("deleting songfile")
            let song = state.songDetails[file.song]
            return client('songs/api/upload/'+file.id+"/", ({body: file, method: 'DELETE'}), prefix, false)
                .then(response=>{
                    if (response.status==204){
                        commit('removeSongFile', file)
                    }
                    return response
                })
        },
        async updateSongFile({commit}, { file, update }){
            return client('songs/api/upload/'+file.id+"/", ({body: update, method: 'PATCH'}), prefix)
                .then(response=>{
                    commit('updateSongFile', response)
                    return response;
                })
                .catch(error=>console.log(error))
        },
        updateSongTitle({state, commit}, {songId, newTitle}){
            commit('setSongTitle', {songId: songId, newTitle: newTitle})
            if (state.songTitleProcess){
                clearTimeout(state.songTitleProcess)
                commit('clearSongTitleProcess')
            }
                const process = setTimeout(()=>{
                client('songs/api/songs/'+songId+'/', {body: {title: newTitle, id: songId}, method: 'PATCH'}, prefix, false)
                .then(res=>{
                    commit('clearSongTitleProcess')
                    return res;
                })
                .catch(error => console.log("Did not update :", error));
            }, 4000);
            commit('setSongTitleProcess', process)
        },
        updateSongComposers({state, commit}, {songId, newComposers}){
            commit('setSongComposers', {songId: songId, newComposers: newComposers})
            if (state.songComposersProcess){
                clearTimeout(state.songComposersProcess)
                commit('clearSongComposersProcess')
            }
                const process = setTimeout(()=>{
                client('songs/api/songs/'+songId+'/', {body: {composers: newComposers.filter(c=>c.first_name && c.last_name), id: songId}, method: 'PATCH'}, prefix, false)
                    .then(res=>{
                        commit('clearSongComposersProcess')
                        return res
                    })
                .catch(error => console.log("Did not update :", error));
            }, 4000);
            commit('setSongComposersProcess', process)
        },
    }
})

export { store }
