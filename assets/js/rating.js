(function($) {
    var methods = {

        /**
         * Initialization method.
         * @method
         * @instance
        */
        onInit: function() {
            var self = this;
                self.VOTED = false;

            $.get(window.location.pathname, function(data) {
                self.VOTED = data.voted;
                self.VOTED_METHOD = data.voted;

                $('.average').html(data.avg_rating);
                $('.all').html(data.vote_count);
                
                if (self.VOTED) {
                    indexes = [];

                    while (self.VOTED > 0) {
                        indexes.push(self.VOTED);
                        self.VOTED--;
                    }

                    $('.stars').removeClass('active');

                    for (var i = 0; i < indexes.length; i++) {
                        $('.voting').find('[data-pk="'+indexes[i]+'"]').addClass('current-active');
                    }
                }
            });
            
            /**************/
            /*** Events ***/
            /**************/

            /** Add class active when click on stars */
            self.find('#js-voting').on('click', 'a', function() {
                methods.clickOnTheStar.apply(self, arguments);
            });

            /** Add class active when hovering */
            self.find('#js-voting').on('mouseover', 'a', function() {
                methods.mouseover.apply(self, arguments);
            });

            /** Remove class active when you leave the voting block. */
            self.find('#js-voting').on('mouseleave', function() {
                $('.stars').removeClass('active');
            });
        },

        /**
         * Add class active when click on stars.
         * @method
         * @instance
         */
        clickOnTheStar: function (e) {
            var self = this;

            if (!self.VOTED_METHOD) {
                var CURRENT_DATA_URL = window.location.pathname,
                    target = e.target,
                    rating = $(target).data('pk'),
                    indexes = [];

                var rating_data = {
                    'rating': rating,
                    'csrfmiddlewaretoken': CSRF_TOKEN
                }

                while (rating > 0) {
                    indexes.push(rating);
                    rating--;
                }

                $('.stars').removeClass('active');

                for (var i = 0; i < indexes.length; i++) {
                    $('.voting').find('[data-pk="'+indexes[i]+'"]').addClass('current-active');
                }

                $.post(CURRENT_DATA_URL, rating_data, function(data) {
                    self.VOTED_METHOD = data.voted;

                    $('.average').html(data.avg_rating);
                    $('.all').html(data.vote_count);
                });    
            }  
        },

        /**
         * Add class active when hovering.
         * @method
         * @instance
         */
        mouseover: function (e) {
            var self = this;

            if (!self.VOTED_METHOD) {
                var indexes = [],
                    target = e.target,
                    rating = $(target).data('pk');

                while (rating > 0) {
                    indexes.push(rating);
                    rating--;
                }

                $('.stars').removeClass('active');

                for (var i = 0; i < indexes.length; i++) {
                    $('.voting').find('[data-pk="'+indexes[i]+'"]').addClass('active');
                }
            }
        },
    };
    $.fn.pageRating = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.onInit.apply(this, arguments);
        } else {
            $.error('No method');
        }
    }
}(jQuery));

/** Init plugin on landing page. */
$("#js-rating").pageRating();
