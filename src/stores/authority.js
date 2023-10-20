import { ref } from "vue";
import { defineStore } from "pinia";

export const useAuthorityStore = defineStore("authority", () => { 
    const authority = 0
    const setAuthority = (_authority) => {
        authority = _authority
    }
    return { authority, setAuthority }
})