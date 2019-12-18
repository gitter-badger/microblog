<template>
  <div id="app">
    <h1>Recent posts</h1>
    <div v-for="post in posts" :key="post.title">
      <post-headline v-bind:post=post></post-headline>
    </div>
  </div>
</template>

<script>
import PostHeadline from '../components/PostHeadline.vue';

export default {
  name: 'Home',
  data() {
    return {
      posts: [
        {
          title: 'title 1',
          author: 'author1',
          date: 'yesterday',
          slug: 'title-1',
          summary: 'post 1 summary',
        },
        {
          title: 'title 2',
          author: 'author2',
          date: 'today morning',
          slug: 'title-2',
          summary: 'post 2 summary',
        },
      ],
    };
  },
  components: { PostHeadline },
};
</script>
