<template>
  <nav aria-label="Page navigation example">
    <div class="d-flex flex-row">
      <div class="d-flex align-items-start flex-grow-1">
        <p class="">Total: {{ pagination.total }}</p>
      </div>
      <div class="d-flex align-items-end">
        <ul class="pagination" v-if="totalPage">
          <li class="page-item" @click="previousClick">
            <a class="page-link" :class="{'disabled-link' : !pagination.has_prev}" href="javascript:;" tabindex="-1">
              <i class="fa fa-angle-left"></i>
              <span class="sr-only">Previous</span>
            </a>
          </li>
          <li v-for="page in totalPage" :key="page" class="page-item" :class="{'active':page === pagination.page}"
              @click="emit('updatePageNumber',page)">
            <a class="page-link" href="javascript:;">{{ page }}</a>
          </li>
          <li class="page-item" @click="nextClick">
            <a class="page-link" :class="{'disabled-link' : !pagination.has_next}" href="javascript:;" tabindex="-1">
              <i class="fa fa-angle-right"></i>
              <span class="sr-only">Next</span>
            </a>
          </li>
        </ul>
      </div>
    </div>

  </nav>
</template>

<script setup>
    import { computed, onMounted, ref } from "vue";
    const emit=defineEmits(['updatePageNumber'])
    const props = defineProps({
      pagination: {
        has_next: Boolean,
        has_previous: Boolean,
        limit: Number,
        page: Number,
        total: Number
      }
    });
    const totalPage = computed(() => {return Math.ceil(props.pagination.total / props.pagination.limit)});
    const previous = computed(() => {
        let page = (props.pagination.page)-1 ;
        if(page>=1) {
            return page;
        } else {
            return 1;
        }
    });
    const next = computed(() => {
        let page = (props.pagination.page)+1 ;
        if(page < totalPage) {
            return page;
        } else {
            return props.pagination.page;
        }
    });

    function nextClick() {
      if (props.pagination.page < totalPage.value) {
        console.log(props.pagination.page, totalPage)
        emit('updatePageNumber',props.pagination.page + 1)
      }
    }
    function previousClick(){
      if (props.pagination.page > 1) {
        emit('updatePageNumber',props.pagination.page - 1)
      }
    }
</script>

<style scoped>
  .disabled-link {
    cursor: not-allowed;
    opacity: 0.4;
  }

  .active a {
    color: #fff !important;
  }
</style>