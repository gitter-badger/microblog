<template>
  <div class="post-headline">
    <h2>{{ post.title }}</h2>
    <h3>Published on {{ post.date }} by {{ post.author }}</h3>
    <p>{{ post.summary }}</p>
    <p>
      <router-link
        :to="{name: 'post', params: {author: post.author, slug: post.slug}}"
      >
        read more
      </router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'PostHeadline',
  props: [
    'post',
  ],
};
</script>
