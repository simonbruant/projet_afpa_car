<template>
  <div class="relative" v-on-clickaway="() => { isOpen ? cancel() : null }">
    <div ref="input" class="block w-full border px-3 py-2 bg-white rounded focus:outline-0 focus:shadow-focus" :class="{ 'shadow-focus': isOpen }" @click="open" tabindex="0" @keydown.up.prevent="open" @keydown.down.prevent="open" @keydown.space.prevent="open">
      <span v-if="value !== null">{{ value }}</span>
      <span v-else class="text-grey-dark">{{ holder }}</span>
    </div>
    <div v-show="isOpen" class="mt-1 absolute pin-x bg-grey-darkest p-2 rounded shadow z-50">
      <input :value="search" @input="e => { $emit('search', e.target.value) }" ref="search" type="text" class="block mb-2 w-full px-3 py-2 bg-grey-darker text-white rounded" style="outline: 0;" @keydown.up="highlightPrev" @keydown.down="highlightNext" @keydown.enter.prevent="commitSelection" @keydown.esc="cancel" @keydown.tab.prevent>
      <ul ref="options" v-show="options.length > 0" class="list-reset relative overflow-y-auto scrolling-touch" style="max-height: 200px;">
        <li ref="option" v-for="(option, i) in options" :key="option" class="px-3 py-2 text-white cursor-pointer rounded" :class="[i === highlightedIndex ? 'bg-blue' : 'hover:bg-grey-darker']" @click="select(i)">{{ option }}</li>
      </ul>
      <div v-if="!search & (options.length === 0)" class="px-3 py-2 text-grey">Entrez une ville ou un code postal</div>
      <div v-else-if="(options.length === 0)" class="px-3 py-2 text-grey">...</div>
    </div>
  </div>
</template>

<script>
import { mixin as clickaway } from "vue-clickaway";

export default {
  mixins: [clickaway],
  props: ["value", "search", "options", "holder", "id"],
  data() {
    return {
      isOpen: false,
      highlightedItem: null,
      highlightedIndex: 0
    };
  },
  watch: {
    search() {
      var index = this.options.indexOf(this.highlightedItem);
      this.highlightedIndex = index;
    }
  },
  methods: {
    open() {
      this.isOpen = true;
      this.$nextTick(() => {
        this.$refs.search.focus();
      });
    },
    close() {
      this.isOpen = false;
      this.$nextTick(() => {
        this.$refs.input.focus();
      });
    },
    cancel() {
      this.close();
    },
    commitSelection() {
      this.$emit("input", this.options[this.highlightedIndex]);
      this.$emit("search", "");
      this.close();
    },
    select(index) {
      this.highlightedIndex = index;
      this.highlightedItem = this.options[index];
      this.commitSelection();
    },
    highlight(index) {
      this.open();
      this.highlightedIndex = index;
      this.$nextTick(() => {
        this.$refs.options.children[index].scrollIntoView({ block: "nearest" });
      });
    },
    highlightPrev() {
      this.highlight(
        this.highlightedIndex - 1 < 0
          ? this.options.length - 1
          : this.highlightedIndex - 1
      );
    },
    highlightNext() {
      this.highlight(
        this.highlightedIndex + 1 >= this.options.length
          ? 0
          : this.highlightedIndex + 1
      );
    }
  }
};
</script>
