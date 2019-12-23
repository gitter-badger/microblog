<template>
  <div>
    <h1>Register as na author on Microblog</h1>
    <p>Enter your name below and start publishing!</p>
    <form>
      <div>
        <label for="input-name">Name</label>
        <input type="text" id="input-name" v-model="authorName" @change="checkNameAvailable">
        <p class="error-message" v-show="!nameAvailable">
          This name is already taken
        </p>
        <button type="submit" class="primary" @click="registerAuthor" v-show="nameAvailable">
          Register
        </button>
      </div>
    </form>
  </div>
</template>


<script>
import slugify from 'slugify';

export default {
  name: 'Register',
  data() {
    return {
      authorName: '',
      nameAvailable: true,
    };
  },
  methods: {
    async registerAuthor(e) {
      e.preventDefault();
      const url = '/api/authors';
      const data = { name: this.authorName };
      const resp = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      if (resp.status === 201) {
        console.log('author created');
      }
    },
    async checkNameAvailable() {
      const slug = slugify(this.authorName.toLowerCase());
      const url = `/api/author/${slug}`;
      const resp = await fetch(url, {
        method: 'HEAD',
      });
      this.nameAvailable = (resp.status === 404);
    },
  },
};
</script>
