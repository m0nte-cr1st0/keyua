var isEmpty = function (val) {
    return (val === undefined ||
        val === null ||
        val === '' ||
        val === []);
};

var isObjectEmpty = function (obj) {
	return Object.keys(obj).length === 0;
}

// Validation rules format for fields
// {
// 	'name': [
//      ['mandatory'],
//      ['min', 6],
//      ['max', 8],
//      ['repeat', list],
//      ['equal', value]
// 	]
// }

var Validator = (function () {

    function Validator(paramSettings) {
        this.paramSettings = paramSettings;
    	this.errors = [];
    	this.errorFields = [];
    }

    Validator.prototype = {
    	mapping: {
    		'mandatory': 'validateMandatory',
    		'email': 'validateEmail',
    		'url': 'validateUrl',
            'short': 'validateShortText',
            'min': 'validateMinLength',
            'max': 'validateMaxLength',
            'equal': 'validateEqual',
    	},
        /**
         * Adds error for specific key in errors array.
         *
        **/
	    addError: function (key, error) {
	    	if (this.errorFields.indexOf(key) === -1) {
	    		this.errorFields.push(key);
	    		this.errors.push([key, error]);
	    	}
	    },
        /**
         * Removes error for specific key and specific error text from errors array.
         *
        **/
	    removeError: function (key, error) {
	    	if (this.errorFields.indexOf(key) > -1) {
	    		for (var i=0; i < this.errors.length; i++) {
	    			if (this.errors[i][0] === key && this.errors[i][1] === error) {
	    				this.errors.splice(i, 1);
	    				this.errorFields.splice(this.errorFields.indexOf(key), 1);
	    			}
	    		}
	    	}
	    },
        /**
         * Validates given value, based on a specific regex object.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {Object} re - The regex object.
         * @returns {Boolean} - Boolean value of validation result.
         */
        _validateRegex: function (value, re) {
            return re.test(value) ? true : false;
        },
        /**
         * Validates given value, checking whether it is empty or not.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @returns {Boolean} - Boolean value of validation result.
         */
	    validateMandatory: function (value, key, validParam) {
	    	var error = gettext('Field is required');
	    	if (isEmpty(value)) {
	    		this.addError(key, error);
	    	} else {
	    		this.removeError(key, error);
	    	}
	    	return isEmpty(value);
	    },
        /**
         * Validates given value, as Email.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @returns {Boolean} - Boolean value of validation result.
         */
	    validateEmail: function (value, key, validParam) {
	    	var valid = this._validateRegex(value, /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
	    	var error = gettext('Enter a valid email');
	    	if (!isEmpty(value) && !valid) {
	    		this.addError(key, error);
	    	} else {
	    		this.removeError(key, error);
	    	}
	    	return !isEmpty(value) && !valid;
	    },
        /**
         * Validates given value, as URL.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @returns {Boolean} - Boolean value of validation result.
         */
        validateUrl: function (value, key, validParam) {
            var valid = this._validateRegex(value, /(http|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/);
            var error = gettext('Enter a valid URL address');
            if (!isEmpty(value) && !valid) {
                this.addError(key, error);
            } else {
            	this.removeError(key, error);
            }
            return !isEmpty(value) && !valid;
        },
        /**
         * Validates given value with minimum length.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @returns {Boolean} - Boolean value of validation result.
         */
        validateShortText: function (value, key, validParam) {
            var MIN_LENGTH = 3;
            var error = gettext('The value is too short');
            var valid = value.length < MIN_LENGTH;

            if (!isEmpty(value) && valid) {
                this.addError(key, error);
            } else {
                this.removeError(key, error);
            }
            return !isEmpty(value) && !valid;
        },
        /**
         * Validates given value with minimum length.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @param {Integer} validParam - The additional param for validation.
         * @returns {Boolean} - Boolean value of validation result.
         */
        validateMinLength: function (value, key, validParam) {
            var minLength = validParam;

            var fmts = ngettext('The minimun length is %s',
                                'The minimun length is %s',
                                minLength),
                error = interpolate(fmts, [minLength]);
            var valid =  value.length < minLength;

            if (!isEmpty(value) && valid) {
                this.addError(key, error);
            } else {
                this.removeError(key, error);
            }
            return !isEmpty(value) && !valid;
        },
        /**
         * Validates given value with maximum length.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @param {Integer} validParam - The additional param for validation.
         * @returns {Boolean} - Boolean value of validation result.
         */
        validateMaxLength: function (value, key, validParam) {
            var maxLength = validParam;

            var fmts = ngettext('The maximum length is %s',
                                'The maximum length is %s',
                                maxLength),
                error = interpolate(fmts, [maxLength]);
            var valid =  value.length > maxLength;

            if (!isEmpty(value) && valid) {
                this.addError(key, error);
            } else {
                this.removeError(key, error);
            }
            return !isEmpty(value) && !valid;
        },
        /**
         * Validates given value equal with other value.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @param {Integer} validParam - The additional param for validation.
         * @returns {Boolean} - Boolean value of validation result.
         */
        validateEqual: function (value, key, validParam) {
            var equalValue = validParam;
            var error = gettext('The value is not equal');

            var valid = value === equalValue;

            if (!isEmpty(value) && valid) {
                this.addError(key, error);
            } else {
                this.removeError(key, error);
            }
            return !isEmpty(value) && !valid;
        },
        /**
         * Validates given value repeats in given array.
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @param {Integer} validParam - The additional param for validation.
         * @returns {Boolean} - Boolean value of validation result.
         */
        validateRepeat: function (value, key, validParam) {
            var arrayOfValues = validParam;
            var error = gettext('The value has already added.');

            var valid = arrayOfValues.indexOf(value) === -1;

            if (!isEmpty(value) && valid) {
                this.addError(key, error);
            } else {
                this.removeError(key, error);
            }
            return !isEmpty(value) && !valid;
        },
        /**
         * Searches related validation function and runs it for current value.
         *
         * @param {String} value - The current value.
         * @param {String} key - The key pointing to the value to be validated.
         * @param {String} validator - The current key of validation.
         * @returns {function} - Validation function for current validation key.
        **/
	    getHandler: function (value, key, validator) {
	    	var self = this;
            var validatorKey = validator[0];
            var validatorValue = validator.length > 1 ? validator[1] : false;
	    	return this[this.mapping[validatorKey]].call(self, value, key, validatorValue);
	    },
        /**
         * Runs all validation rules for value. Returned actual result of checking
         *
         * @method
         * @instance
         * @param {String} value - The current value.
         * @returns {Array} - Array of checking result,
         					  which holds boolean of validation result as first value in array
         					  and array of errors if any.
         */
	    validate: function (value) {
	    	for (key in this.paramSettings) {
	    		var validators = this.paramSettings[key];
	    		for (var i=0; i < validators.length; i++) {
	    			this.getHandler(value, key, validators[i]);
	    		}
	    	}
	    	return [this.errorFields.length === 0, this.errors]
	    }
	};

    return Validator;

}());