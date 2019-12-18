<template>
  <div id="container" class="flex one four-fifth center grow">
    <nav>
      <router-link v-bind:to="{name: 'home'}" class="brand">Microblog</router-link>
      <input id="cmenug" type="checkbox" class="show">
      <label for="cmenug" class="burger pseudo button">&#8801;</label>
    </nav>
    <div>
      <router-view/>
    </div>
  </div>
</template>
