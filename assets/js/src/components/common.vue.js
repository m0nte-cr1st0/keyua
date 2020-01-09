Vue.component('server-errors', {
	props: {
		errors: {
			type: Array,
			required: true,
		},
	},
	template: `
		<div class="server-errors" v-if="errors.length">
			<ul>
				<li v-for="(error, index) in errors" :key="index">
					<span>{{ Object.keys(error)[0] }}:</span> {{ Object.values(error)[0] }}
				</li>
			</ul>
		</div>
	`,
})


Vue.component('switch-languages', {
	props: {
		languages: {
			type: Array,
			required: true,
		},
		language: {
			type: String,
			required: true,
		}
	},
	template: `
		<div>
	        <select ref="input" v-on:input="setLanguage($event.target.value)" :value="language">
	            <option v-for="(lang, index) in languages" :key="index" :value="lang">
	            	{{ lang }}
	            </option>
	        </select>
	    </div>
	`,
	methods: {
        /**
         * Switches language.
         *
         * @method
         * @instance
         */
	    setLanguage: function(lang) {
	    	var url = PROJECT_URLS.languages.setLanguage + '?test=test';

	    	var instance = axios.create();
	    	instance.defaults.headers.common['X-CSRFToken'] = CSRF_TOKEN;
	    	instance.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
            

			var params = new URLSearchParams();
			params.append('language', lang);
			params.append('next', PROJECT_URLS.landing.index);

            instance.post(url, params)
                .then(function (response) {
                    location.href = PROJECT_URLS.landing.index;
                })
                .catch(function (error) {
                    console.log(error);
                });
	    },
	}
})