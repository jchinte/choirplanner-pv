<template>
    <div class="custom-select-wrapper" @click.stop="setOpen()">
    <div :class="['custom-select', open && 'open']">
        <div class="custom-select__trigger">
             <div class="arrow" @click.stop="open = !open"></div>
             <template v-if="getSelectedTags().length==0 && !open">
                <span v-if="getSelectedTags().length==0" class="fl pa2">Filter by song type...</span>
             </template>
             <template v-else>
                <span v-for="selected in getSelectedTags()" :key="selected.index" :class="getClasses(selected.name)" @click.stop="select(selected.index)">{{ selected.name }}
                    <span class="pl1">&times;</span>
                </span>
             </template>
             <input v-if="open"  
                    ref="tagInput" 
                    v-model="autocomplete" 
                    :class="[...'bn b--transparent hover-bg-transparent:focus outline-transparent outline-0'.split(' '), getSelectedTags()?'w-20':'w-auto']"
                    :placeholder="getSelectedTags().length>0?'':'Filter by song type...'"
                    @click.stop/>
        </div>
        <div class="custom-options">
            <span  v-for="(item, i) in items" :key="i" @click.stop="select(i)" :class="[filtered.includes(item)?'custom-option':'custom-option-hidden', selections[i] && 'selected',]"><span :class="getClasses(item)">{{ item }}</span></span>
        </div>
    </div>
</div>
</template>
<script>
import { getClasses } from './tagStyles.js'
import { ref, onMounted } from 'vue'
export default {
    name: 'SelectTagStyled',
    components: {
        
    },
    inject: ['hash', 'prefix', 'debug'],
    props: {
        items: Array,
        modelValue: {
            type:Array,
            default:[],
        },
    },
    data: function(){
        return {
            open:false,
            selections:this.items.map(item=>false),
            autocomplete:'',
            // filtered:this.items,
        }
    },
    computed: {
    },
    watch: {
        // autocomplete(oldVal, newVal){
        //     console.log(this.autocomplete)
        //     this.filtered = this.autocomplete?this.items.filter(item=>item.includes(this.autocomplete)) : this.items;
        // },
    },
    computed: {
        filtered(){
            return this.autocomplete?this.items.filter(item=>item.includes(this.autocomplete)) : this.items;
        }
    },
    setup(){
        const tagInput = ref(null)

        onMounted(()=> {
            console.log(tagInput.value)
        })
        return {
            tagInput
        }
    },
    created(){
        window.addEventListener('click', this.close);
    },
    unmounted(){
        window.removeEventListener('click', this.close);
    },
    methods:{
        getSelectedTags(){
            if (!this.selections)
                return this.items
            var currSelections = []
            for(let i = 0; i < this.selections.length; i++){
                if (this.selections[i]){
                    currSelections.push({name:this.items[i], index:i});
                }
            }
            return currSelections;
        },
        select(i){
            this.selections[i] = !this.selections[i];
            var currSelections = []
            for(let i = 0; i < this.selections.length; i++){
                if (this.selections[i]){
                    currSelections.push(this.items[i]);
                }
            }
            this.autocomplete = '';
            this.$emit("update:modelValue", currSelections);
        },
        close(){
            this.open = false;
        },
        getClasses(item){
            return getClasses(item)
        },
        setOpen(){
            this.open = true;
            console.log(this.tagInput)
            setTimeout(()=>{
                if (this.open){
                    if (this.tagInput)
                        this.tagInput.focus()
                }
            }, 100)
        }
    },
}
</script>

<style scoped>
 /* html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
     margin: 0;
     padding: 0;
     border: 0;
     font-size: 100%;
     font: inherit;
     vertical-align: baseline;
} */
/* HTML5 display-role reset for older browsers */
 /* article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
     display: block;
} */
 /* body {
     line-height: 1;
} */
 /* ol, ul {
     list-style: none;
}
 blockquote, q {
     quotes: none;
}
 blockquote:before, blockquote:after, q:before, q:after {
     content: '';
     content: none;
} */
/* table {
     border-collapse: collapse;
     border-spacing: 0;
}
*, *:after, *:before {
     box-sizing: border-box;
} */
.custom-select-wrapper {
     position: relative;
     user-select: none;
     width: 100%;
}
 .custom-select {
     position: relative;
     display: flex;
     flex-direction: column;
     border-width: 0 2px 0 2px;
     border-style: solid;
     border-color: #394a6d;
}
 .custom-select__trigger {
     position: relative;
     display: flex;
     align-items: left;
     vertical-align: middle;
     justify-content: none;
     padding: 0 9px;
     font-size: 1rem;
     font-weight: 300;
     color: #3b3b3b;
     height: 2rem;
     /* line-height: 24px; */
     background: #ffffff;
     cursor: pointer;
     border-width: 2px 0 2px 0;
     border-style: solid;
     border-color: #394a6d;
     white-space: nowrap;
     overflow-x: auto;
}
 .custom-options {
     position: absolute;
     display: block;
     top: 100%;
     left: 0;
     right: 0;
     border: 2px solid #394a6d;
     border-top: 0;
     background: #fff;
     transition: all 0.5s;
     opacity: 0;
     visibility: hidden;
     pointer-events: none;
     z-index: 2;
}
 .custom-select.open .custom-options {
     opacity: 1;
     visibility: visible;
     pointer-events: all;
}
 .custom-option {
     position: relative;
     display: block;
     padding: 0 9px 0 9px;
     font-size: 1rem;
     font-weight: 300;
     color: #3b3b3b;
     /* line-height: 26px; */
     cursor: pointer;
     transition: all 0.5s;
}
 .custom-option-hidden {
     position: relative;
     display: none;
     padding: 0 9px 0 9px;
     font-size: 2rem;
     font-weight: 300;
     color: #3b3b3b;
     /* line-height: 26px; */
     cursor: pointer;
     transition: all 0.5s;
}
 .custom-option:hover {
     cursor: pointer;
     background-color: #b2b2b2;
}
 .custom-option.selected {
     color: #ffffff;
     background-color: #305c91;
}
.arrow {
     position: relative;
     height: 15px;
     width: 15px;
}
 .arrow::before, .arrow::after {
     content: "";
     position: absolute;
     bottom: 0px;
     width: 0.15rem;
     height: 100%;
     transition: all 0.5s;
}
 .arrow::before {
     left: -5px;
     transform: rotate(45deg);
     background-color: #394a6d;
}
 .arrow::after {
     left: 5px;
     transform: rotate(-45deg);
     background-color: #394a6d;
}
 .open .arrow::before {
     left: -5px;
     transform: rotate(-45deg);
}
 .open .arrow::after {
     left: 5px;
     transform: rotate(45deg);
}
</style>