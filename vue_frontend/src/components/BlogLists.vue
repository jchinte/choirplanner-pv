<template>
    
    <!-- <a href="{% routablepageurl page "latest_posts" %}">View Latest Posts Only</a> -->

    <!-- <h2>
        Categories:
        <small>
            {% for cat in categories %}
                <a href="{% routablepageurl page "category_view" cat.slug %}">
                    {{ cat.name }}
                </a>{% if not forloop.last %}, {% endif %}
            {% endfor %}
        </small>
    </h2> -->
    <section class="mw7 center avenir">
        <article v-for="(post, i) in posts" :key="i" class="bt bb b--black-10">
            <router-link :to="{ name: 'blog-post', params: { slug: post.slug }}" class="db pv4 ph3 ph0-l no-underline black dim">
            <!-- <div class="mw9 center pa2 ph5-l sans-serif"> -->
                <!-- {% for post in posts %}
                    {% cache 604800 blog_post_preview post.id %} -->
                        <div class="flex flex-column flex-row-ns">
                            <div class="pr3-ns mb4 mb0-ns w-100 w-40-ns">
                                <!-- {% image post.banner_image fill-250x250 as blog_img %} -->
                                <!-- <a href="{{ post.url }}"> -->
                                    <img :src="post.banner.url" :alt="post.banner.alt" class="db">
                                <!-- </a> -->
                            </div>
                            <div class="w-100 w-60-ns pl3-ns">
                                    <h1 class="f3 fw1 baskerville mt0 lh-title">{{ post.title }}</h1>

                                        <p v-if="post.subtitle" class="f6 f5-l lh-copy">{{ post.subtitle }}</p>


                                    <!-- {# @todo add a summary field to BlogDetailPage; make it a RichTextField with only Bold and Italic enabled. #} -->
                                    <!-- <a href="{{ post.url }}" class="btn btn-primary mt-4">Read More</a> -->
                            </div>
                        </div>
                    <!-- {% endcache %}
                {% endfor %} -->
            <!-- </div> -->
            </router-link>
        </article>
    </section>
    <!-- {# Only show pagination if there is more than one page to click through #}
    {% if posts.paginator.num_pages > 1 %}
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <div class="pagination">
                        {% if posts.has_previous %}
                            <li class="page-item">
                                <a href="?page={{ posts.previous_page_number }}" class="page-link">
                                    <span>&laquo;</span>
                                </a>
                            </li>
                        {% endif %}

                        {% for page_num in posts.paginator.page_range %}
                            <li class="page-item {% if page_num == posts.number %} active{% endif %}">
                                <a href="?page={{ page_num }}" class="page-link">
                                    {{ page_num }}
                                </a>
                            </li>
                        {% endfor %}

                        {% if posts.has_next %}
                            <li class="page-item">
                                <a href="?page={{ posts.next_page_number }}" class="page-link">
                                    <span>&raquo;</span>
                                </a>
                            </li>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    {% endif %} -->


</template>

<script>
import { client } from '../utils/fetch_utils.js'
export default {
    inject: ['hash', 'prefix', 'debug'],
    data: function(){
        return {
            posts: [],
            title: '',
            meta: null,
        }
    },
    created(){
        this.getBlogs();
    },
    methods: {
        getBlogs(){
            client('api/v2/pages/praising-voices-blog/', ({}), this.prefix.value)
                .then(data => {
                    this.posts = data.posts;
                    this.title = data.title;
                    this.meta = data.meta;
                })
                .catch(e => console.log(e));
        }
    }
}
</script>

<style scoped>

</style>