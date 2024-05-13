<template>
    <div id="snackbar">{{ snackBarStore.snackbarMessage }}</div>
</template>
<script setup>
import { watch } from 'vue';
import {snackBarStore} from '../../store';
   watch(snackBarStore, (newValue, oldValue) => {
    if(snackBarStore.snackbarMessage !== '') {
        setTimeout(()=>{
        console.log('executed timeout function')
        snackBarStore.snackbarMessage = ''
    },3000)
    }
   })
</script>

<style scoped>
    #snackbar {
    visibility: visible;
    max-width: 250px;
    margin-left: -125px;
    background-color: #04AA6D;
    color: #fff;
    text-align: center;
    border: 2px solid #fff;
    border-radius: 2px;
    border-style: outset;
    padding: 16px;
    position: fixed;
    z-index: 1;
    right: 1%;
    top: 10px;
    font-size: 17px;
  }
  
  #snackbar.show {
    visibility: visible;
    -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
    animation: fadein 0.5s, fadeout 0.5s 2.5s;
  }
  
  @-webkit-keyframes fadein {
    from {top: 0; opacity: 0;} 
    to {top: 30px; opacity: 1;}
  }
  
  @keyframes fadein {
    from {top: 0; opacity: 0;}
    to {top: 30px; opacity: 1;}
  }
  
  @-webkit-keyframes fadeout {
    from {top: 30px; opacity: 1;} 
    to {top: 0; opacity: 0;}
  }
  
  @keyframes fadeout {
    from {top: 30px; opacity: 1;}
    to {top: 0; opacity: 0;}
  }
</style>