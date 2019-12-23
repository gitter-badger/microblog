<template>
  <div id="app">
    <h1>Recent posts</h1>
    <div v-for="post in posts" :key="post.title">
      <post-headline v-bind:post=post></post-headline>
    </div>
  </div>
</template>

<script>
import PostHeadline from '@/components/PostHeadline.vue';

export default {
  name: 'Home',
  data() {
    return {
      posts: [],
    };
  },
  components: { PostHeadline },
  methods: {
    async fetchRecent() {
      const url = '/api/posts/recent';
      const resp = await fetch(url);
      const rv = await resp.json();
      this.posts = rv;
    },
  },
  created() {
    this.fetchRecent();
  },
};
</script>
