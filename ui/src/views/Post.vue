<template>
  <div class="post">
    <h2>{{ post.title }}</h2>
    <h3>Published on {{ new Date(post.date).toLocaleString() }} by {{ post.author.name }}</h3>
    <div v-html="post.text_html"></div>
  </div>
</template>

<script>
export default {
  name: 'Post',
  props: [
    'post',
  ],
  data() {
    return {};
  },
  methods: {
    async fetchPost() {
      const url = `/api/post/${this.authorSlug}/${this.postSlug}`;
      const resp = await fetch(url);
      const rv = await resp.json();
      this.post = rv;
    },
  },
  created() {
    this.authorSlug = this.$route.params.author;
    this.postSlug = this.$route.params.slug;
    this.fetchPost();
  },
};
</script>
