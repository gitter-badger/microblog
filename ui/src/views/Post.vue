<template>
  <div class="post">
    <h2>{{ post.title }}</h2>
    <h3>Published on {{ post.date }} by {{ post.author }}</h3>
    {{ post.text_html }}
  </div>
</template>

<script>
export default {
  name: 'Post',
  data() {
    return { post: {} };
  },
  methods: {
    fetchPost() {

    },
  },
};
</script>
