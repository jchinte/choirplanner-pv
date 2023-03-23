<template>
<article v-if="article" class="tl center">
    <!-- <div class="pa3 pa5-ns">
        <h1 class="f3 f2-m f1-l">{{article.title}}</h1>
        <h3 class="f6 f5-m f3-l">{{article.description}}</h3>
        <hr />
        <div class="pa4 ph7-l mw9-l center tl">
            <div v-for="(block, i) in article.body" :key="i" >
                <div 
                    v-if="block.type==='paragraph'" 
                    v-html="block.value" 
                    class="f7 f6-ns lh-copy measure mb4"> </div>
                <div v-else-if="block.type==='heading'" class="f3 fw4">{{ block.value }}</div>
            </div>
        </div>
    </div> -->
    <img :src="article.banner.url" :alt="article.banner.alt" style='width: 100%; height: auto;'>

    <div class="mw9 center pa2 ph5-l sans-serif">
        <div>
            <h3 class="f3 f2-ns measure-narrow lh-title mv0">
               <span class="lh-copy black pa2 tracked-tight">
                {{ article.title }}
               </span>
            </h3>
            <div v-for="(author, i) in article.blog_authors" :key="i" class="flex flex-center">
                    <div>
                        <img :src="author.sm_image.url" class="br-100 h3 ba b--black-10 h3 w3" :alt="author.author_name">
                    </div>
                    <span class="f4">
                    <a v-if="author.website" :href="author.author_website">
                        {{ author.author_name }}
                    </a>
                    <span v-else>{{ author.author_name }}</span>
                    </span>
            </div>
        </div>
        <div class="mw9 center ph3-ns f5">
            <div class="cf">
                <template v-for="(block, i) in article.content" :key="i">
                    <div class="fl w-100 pa2">
                            <div v-if="block.type==='full_richtext'" v-html="block.value"> </div>
                            <div v-else-if="block.type==='simple_richtext'" v-html="block.value"> </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
    <div v-if="article.categories" class="ph3">
        <template v-for="(cat, i) in article.categories" :key="i">
            <a  :href="`?category={cat.slug}`">
                {{ cat.name }}
            </a><span v-if="i<article.categories.length-1">, </span>
        </template>
    </div>
</article>
</template>

<script>
import { client } from '../utils/fetch_utils.js'
export default {
    inject: ['hash', 'prefix', 'debug'],
    props:{
        slug:{
            type: [String, Number],
            default:0,
        }
    },
    data: function(){
        return {
            article: null,
        }
    },
    created(){
        if (this.slug){
            this.getBlog();
        }
    },
    methods: {
        getBlog(){
            client('api/v2/pages/'+this.slug+'/', ({}), this.prefix.value)
                .then(data => {
                    this.article = data;
                    console.log("article: ",this.article);
                })
                .catch(e => console.log(e));
        }
    }
}
</script>

<style scoped>
/* .blog-page {
    text-align: left;
    max-width: 800px;
    padding-left:8rem;
    padding-right:8rem;
} */
</style>