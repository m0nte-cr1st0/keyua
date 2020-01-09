// start dashboard app
new Vue({
    el: '#resetPassword',
    data: {
        password: '',
        repeatPassword: '',
        errors: []
    },
    methods: {
        sendForm: function () {
        	var data =  {
                password: this.password,
                password_repeat: this.repeatPassword,
                key: RESET_REQUEST_KEY
            };

            var instance = axios.create();
            instance.post(RESET_PASSWORD_URL, data)
                .then(function (response) {
                    var answer = response.data;
                    if ('errors' in answer) {
                        console.log(answer.errors);
                    } else {
                        location.href = NEXT_URL;
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },
    computed: {
        passwordErrors: function () {
            var passwordRules = {
                'password': [
                    ['mandatory'],
                ]
            }
            var passwordValidator = new Validator(passwordRules);
            return passwordValidator.validate(this.password);
        },
        repeatPasswordErrors: function () {
            var repeatPasswordRules = {
                'repeatPassword': [
                    ['mandatory']
                ]
            }
            var repeatPasswordValidator = new Validator(repeatPasswordRules);
            return repeatPasswordValidator.validate(this.repeatPassword);
        },
        isFormValid: function () {
            return this.passwordErrors[0] && this.repeatPasswordErrors[0];
        }
    }
})