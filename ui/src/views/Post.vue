<template>
  <div class="post">
    <h2>{{ title }}</h2>
    <h3>Published on {{ date }} by {{ author }}</h3>
    {{ text_html }}
  </div>
</template>

<script>
export default {
  name: 'Post',
  data() {
    return {};
  },
  methods: {
    fetchPost() {

    },
  },
};
</script>
