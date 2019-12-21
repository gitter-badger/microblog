<template>
  <div>
    <h1>Register as na author on Microblog</h1>
    <p>Enter your name below and start publishing!</p>
    <form>
      <div>
        <label for="input-name">Name</label>
        <input type="text" id="input-name" v-bind="authorName" value="">
        <button type="submit" class="primary" @click="registerAuthor">Register</button>
      </div>
    </form>
  </div>
</template>


<script>
export default {
  name: 'Register',
  data() {
    return {
      authorName: '',
    };
  },
  methods: {
    registerAuthor(e) {
      e.preventDefault();
    },
  },
};
</script>
