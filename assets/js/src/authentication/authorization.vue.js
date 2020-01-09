/**
 * Vue component for authorization modal form.
 */
Vue.component('authorization-modal', {
    template: `
      <transition name="modal">
        <div class="modal-mask">
          <div class="modal-wrapper">
            <div class="modal-container mini">
                <div class="modal-header">
                    <h3>{{ actionTitle }}</h3>
                    <a href="#" class="close" @click.prevent="$emit('close')">&nbsp;</a>
                </div>
                <div class="modal-body">
                    <div v-if="action === 'registration'">
                        <label>{{ texts.firstName }}</label>
                        <div v-if="!nameErrors[0]" class="form-hint">
                            <transition-group name="fade">
                                <span v-for="(error, index) in nameErrors[1]" :key="index">
                                    {{ error[1] }}
                                </span>
                            </transition-group>
                        </div>
                        <div class="input-wrapper">
                            <input v-model="form.firstName" class="grey" type="text" />
                            <i v-show="nameErrors[0]" class="valid-input"></i>
                        </div>
                    </div>
                    <div>
                        <label class="m-top">{{ texts.email }}</label>
                        <div v-if="!emailErrors[0]" class="form-hint">
                            <transition-group name="fade">
                                <span v-for="(error, index) in emailErrors[1]" :key="index">
                                    {{ error[1] }}
                                </span>
                            </transition-group>
                        </div>
                        <div class="input-wrapper">
                            <input v-model="form.email" class="grey" type="email" />
                            <i v-show="emailErrors[0]" class="valid-input"></i>
                        </div>
                    </div>
                    <div v-if="action !== 'restore password'">
                        <label class="m-top">{{ texts.password }}</label>
                        <div v-if="!passwordErrors[0]" class="form-hint">
                            <transition-group name="fade">
                                <span v-for="(error, index) in passwordErrors[1]" :key="index">
                                    {{ error[1] }}
                                </span>
                            </transition-group>
                        </div>
                        <div class="input-wrapper">
                            <input v-model="form.password" class="grey" type="password" />
                            <i v-show="passwordErrors[0]" class="valid-input"></i>
                        </div>
                    </div>
                    <div v-if="action !== 'registration'" class="link">
                        <a v-if="action === 'login'" href="#" @click.prevent="changeType('restore password')">{{ texts.forgotPassword }}?</a>
                        <a v-if="action !== 'login'" href="#" @click.prevent="changeType('login')">{{ texts.login }}</a>
                    </div>
                </div>
                <div class="modal-footer">
                    <button
                        :disabled="!isFormValid"
                        @click="sendFormData"
                    >{{ texts.send }}</button>
                </div>
                <server-errors :errors="errs"></server-errors>
            </div>
          </div>
        </div>
      </transition>
    `,
    props: {
        action: {
            type: String,
            required: true
        },
        errs: {
            type: Array,
            required: true
        }
    },
    data: function () {
        return {
            texts: JS_TEXTS.components.authorization,
            form: {
                firstName: '',
                email: '',
                password: '',
            },
            errors: [],
        }
    },
    methods: {
        /**
         * Calls changing for modal form type.
         *
         * @method
         * @instance
         * @param {String} type - Selected type of modal form.
         */
        changeType: function(type) {
            this.$emit('change-type', type);
        },
        /**
         * Calls sending method for current modal form type.
         *
         * @method
         * @instance
         */
        sendFormData: function () {
            var data = this.form;
            this.$emit('send-form', data);
        },
    },
    computed: {
        /**
         * Returns title of current modal form type.
         *
         * @method
         * @instance
         * returns {String}
         */
        actionTitle: function () {
            return {
                'login': this.texts.login,
                'registration': this.texts.registration,
                'restore password': this.texts.forgotPassword
            }[this.action];
        },
        /**
         * Returns array of errors for current Name field.
         *
         * @method
         * @instance
         * returns {Array}
         */
        nameErrors: function () {
            var nameRules = {
                'firstName': [
                    ['mandatory'],
                    ['short'],
                ],
            }
            var nameValidator = new Validator(nameRules);
            return nameValidator.validate(this.form.firstName);
        },
        /**
         * Returns array of errors for current Email field.
         *
         * @method
         * @instance
         * returns {Array}
         */
        emailErrors: function () {
            var emailRules = {
                'email': [
                    ['mandatory'],
                    ['email'],
                ]
            }
            var emailValidator = new Validator(emailRules);
            return emailValidator.validate(this.form.email);
        },
        /**
         * Returns array of errors for current Password field.
         *
         * @method
         * @instance
         * returns {Array}
         */
        passwordErrors: function () {
            var passwordRules = {
                'password': [
                    ['mandatory'],
                    ['min', 6]
                ]
            }
            var passwordValidator = new Validator(passwordRules);
            return passwordValidator.validate(this.form.password);
        },
        /**
         * Returns status of form validation.
         *
         * @method
         * @instance
         * returns {Boolean}
         */
        isFormValid: function () {
            if (this.action === 'login') {
                return this.emailErrors[0] && this.passwordErrors[0];
            } else if (this.action === 'registration') {
                return this.emailErrors[0] && this.passwordErrors[0] && this.nameErrors[0];
            } else {
                return this.emailErrors[0];
            }
        }
    }
})

/**
 * The base Vue instance for authorization application.
 */
new Vue({
    el: '#authorization',
    data: {
        texts: JS_TEXTS.applications.authorization,
        consts: JS_CONSTS,
        reviews: reviewListTest,
        showAuthModal: false,
        loginType: 'login',
        registrationType: 'registration',
        restorePasswordType: 'restore password',
        currentAction: 'login',
        serverErrors: [],
        languagesList: [],
        currentLanguage: '',
    },
    created: function () {
        this.languagesList = LANGUAGES;
        this.currentLanguage = CURRENT_LANGUAGE;
    },
    methods: {
        /**
         * Changes modal type for: login, registration, forgot password.
         *
         * @method
         * @instance
         * @param {String} type - Selected type of modal form.
         */
        changeModalType: function (type) {
            this.currentAction = type;
            this.showAuthModal = true;
        },
        /**
         * Sends form for current modal type.
         *
         * @method
         * @instance
         * @param {Object} - An associative array of form data.
         */
        sendForm: function (data) {
            var self = this;
            var url = {
                'login': PROJECT_URLS.authentication.login,
                'registration': PROJECT_URLS.authentication.registration,
                'restore password': PROJECT_URLS.authentication.restorePassword
            }[self.currentAction];

            self.serverErrors = [];

            var instance = axios.create();
            instance.post(url, data)
                .then(function (response) {
                    var answer = response.data;
                    if ('errors' in answer) {
                        self.serverErrors = answer.errors;
                    } else {
                        location.href = PROJECT_URLS.landing.index;
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
    }
})