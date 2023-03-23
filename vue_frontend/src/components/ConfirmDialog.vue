<template>
<teleport to="body">
    <div v-if="open" class="modal">
        <div class="w3-display-container" style="width:80%; height:80%">
            <div class="w3-display-middle" style="width:80%;">
                <slot>{{ message }}</slot>
            </div>
            <div class="w3-display-bottomright" style="height:auto;width:auto;">
                <button @click="cancel">close</button><button v-if="callback" @click="confirm">confirm</button>
                <button v-if="custom" @click="doCustom">{{ custom.text }}</button>
            </div>
        </div>
    </div>
</teleport>
</template>

<script>
function customValidator(value){
  return (value instanceof Object) 
    && value.hasOwnProperty('callback') && value.callback instanceof String && value.callback !== ''
    && value.hasOwnProperty('text') && value.text instanceof String && value.callback !== ''
}

export default {
    name: 'ConfirmDialog',
    props: {
        message: {
            type: String,
            default: '',
        },
        callback: {
            type: Function,
            default: null,
        },
        cancelDialog: {
            type: Function,
            default: null,
        },
        custom: {
          type: Object,
          default: null,
          validator: customValidator,
        },
        open: false,
    },
    data() {
        return {};
    },
    emits: ['update:open', 'confirm'],
    methods: {
        confirm() {
            this.$emit('update:open', false);
            if (this.callback) {
                this.callback();
            }
        },
        cancel() {
            this.$emit('update:open', false);
            if (this.cancelDialog) {
                this.cancelDialog;
            }
        },
        doCustom(){
            this.$emit(this.custom.callback);
        }
    }
}
</script>

<style scoped>
.modal {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: rgba(0, 0, 0, .5);
    display: flex;
    /* flex-direction: column; */
    align-items: center;
    justify-content: center;
}

.modal div {
    /* display: flex; */
    /* flex-direction: column; */
    align-items: center;
    justify-content: center;
    background-color: white;
    width: 90%;
    height: 90%;
    padding: 5px;
}
</style>
