/**
 * The base Vue instance for project.
 */
new Vue({
    el: '#vue-app',
    data: {
        languagesList: [],
        currentLanguage: '',
    },
    created: function () {
        this.languagesList = LANGUAGES;
        this.currentLanguage = CURRENT_LANGUAGE;
    },
})