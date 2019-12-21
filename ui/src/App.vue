<template>
  <div id="container" class="flex one three-fourth center grow">
    <nav>
      <router-link v-bind:to="{name: 'home'}" class="brand">Microblog</router-link>
      <input id="cmenug" type="checkbox" class="show">
      <label for="cmenug" class="burger pseudo button">&#8801;</label>
      <div class="menu">
        <router-link v-bind:to="{name: 'register'}">Register</router-link>
      </div>
    </nav>
    <div>
      <router-view/>
    </div>
  </div>
</template>
