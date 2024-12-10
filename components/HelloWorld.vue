<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
  msg2: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h2 class="subtitle">{{ msg2 }}</h2>
  </div>
</template>

<style scoped>
@font-face {
  font-family: 'MyCustomFont';
  src: url('fonts/MyCustomFont.TTF') format('truetype');
}


h1 {
  font-family: 'MyCustomFont', sans-serif;
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: 180px;
  margin-left: 95px;
}

h2{
  font-family: 'MyCustomFont', sans-serif;
  margin-left: 155px;
  margin-top: 80px;
}

h3 {
  font-size: 1.2rem;

}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
