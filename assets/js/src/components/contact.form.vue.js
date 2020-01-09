Vue.component('contact-form', {
	template: `
        <div class="row">
            <div class="col-sm-12">
                <div class="col-md-6">
                    <div class="input-wrapper">
                        <input
                            v-model="form.name"
                            type="text"
                            placeholder="Your name"
                            :class="errors.name ? 'error' : ''"
                        />
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="input-wrapper">
                        <input
                            v-model="form.email"
                            type="email"
                            placeholder="Your email"
                            :class="errors.email ? 'error' : ''"
                         />
                    </div>
                </div>
            </div>
            <div class="col-sm-12">
                <div>
                  <input type="range" id="cowbell" name="cowbell"
                         min="0" max="1500" value="1000" step="250" style="margin: .4rem;">
                </div>
            </div>
            <div class="col-sm-12">
                <div class="input-wrapper">
                    <textarea
                        v-model="form.text"
                        placeholder="About your project"
                        :class="errors.text ? 'error' : ''"
                    ></textarea>
                </div>
            </div>
            <div class="col-sm-12">
                <div class="col-md-6">
                    <div class="row">
                        <div class="input-wrapper">
                            <div class="">
                                <div class="custom-checkbox">
                                    <input v-model="form.nda" type="checkbox" id="checkbox1" />
                                    <label for="checkbox1">Send me an NDA</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                <div class="input-wrapper">
                    <img v-show="isProcessingRequest" src="/static/images/loader.svg" height="65" alt="Loading..." />
                    <input
                        v-show="!isProcessingRequest"
                        @click.prevent="sendForm()"
                        class="green-button"
                        type="submit"
                        value="Send"
                    />
                </div>
                </div>
            </div>
        </div>
	`,
	data: function () {
		return {
            isProcessingRequest: false,
			form: {
                name: '',
                email: '',
                phone: '',
                nda: false,
                text: ''
            },
            errors: {
                name: false,
                email: false,
                text: false
            },
		}
	},
    methods: {
        sendForm: function () {
            var self = this;
            self.isProcessingRequest = true;
            var form = self.form;

            self.errors = {
                name: false,
                email: false,
                text: false
            };

            if (form.name && form.email && form.text) {
                axios.post(API_URL, form)
                    .then(function (response) {
                        self.isProcessingRequest = false;

                        var answer = response.data;
                        if (answer.success) {
                            self.form = {
                                name: '',
                                email: '',
                                phone: '',
                                nda: false,
                                text: ''
                            }
                            window.location.href = '/';
                        } else {
                            var serverErrors = answer.errors;

                            var errorsText = '';
                            for (var key in serverErrors) {
                                self.errors[key] = true;
                                errorsText += `${serverErrors[key][0]}\n` + 'end';
                            }
                            alert(errorsText);
                        }
                    })
            } else {
                self.isProcessingRequest = false;
            }
        }
    }
})