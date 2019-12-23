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
        <label for="input-password">Password</label>
        <input type="password" id="input-password" v-model="password">
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
      password: '',
      nameAvailable: true,
    };
  },
  methods: {
    async registerAuthor(e) {
      e.preventDefault();
      const url = '/api/accounts';
      const data = {
        name: this.authorName,
        password: this.password,
      };
      const resp = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      if (resp.status === 201) {
        const result = await resp.json();
        console.log('author created');
        const storage = window.localStorage;
        storage.setItem('access_token', result.access_token);
        storage.setItem('refresh_token', result.refresh_token);
      }
    },
    async checkNameAvailable() {
      const slug = slugify(this.authorName.toLowerCase());
      const url = `/api/account/${slug}`;
      const resp = await fetch(url, {
        method: 'HEAD',
      });
      this.nameAvailable = (resp.status === 404);
    },
  },
};
</script>
