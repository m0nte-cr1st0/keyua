(function($) {
    var methods = {

        /**
         * Initialization method.
         * @method
         * @instance
        */
        onInit: function(options) {
            var self = this;
                self.options = options;

            /** Create title bar and give archor h2h3 and tag a */
            methods.titleBarArchor.apply(self, arguments);

            var linkWrapper = this.options.linkWrapper;

            /**************/
            /*** Events ***/
            /**************/

            $(window).on('scroll', function() {
                methods.titleBarHighlighting.apply(self, arguments);
                methods.titleBarChangePosition.apply(self, arguments);
                methods.titleBarReactionToFooter.apply(self, arguments);
            });

            $(linkWrapper).on('click', 'li a', function (event) {
                event.preventDefault();

                var id = $(this).attr('href');
                $(window).scrollTop($(id).offset().top);
            });

        },

        /**
         * Create title bar and give archor h2h3 and tag a.
         * @method
         * @instance
         */
        titleBarArchor: function() {
            var count = 0;
            var contentArea = this.options.contentArea,
                linkWrapper = this.options.linkWrapper;

            $(contentArea + ' h2, ' + contentArea +' h3').each(function() {
                count++;
                $(this).attr('id', count);

                var tagName = $(this).prop("tagName");
                var classLink = tagName === 'H2' ? '' : 'subparagraph';

                $(linkWrapper + ' ul')
                    .append('<li id="step'+ count +'" class="'+ classLink +'"><a href="#'+count+'">'+ $(this).text() +'</a></li>');
            });
        },

        /**
         * Title bar highlighting with scrolling.
         * @method
         * @instance
         */
        titleBarHighlighting: function() {
            var linkWrapper = this.options.linkWrapper;
            var windowScroll = $(window).scrollTop();
            var contentArea = this.options.contentArea;
            var containerLinkWrapper = this.options.containerLinkWrapper;

            var lastElement = 0;
            
            $(contentArea + ' h2, ' + contentArea +' h3').each(function(i) {
                if ($(this).offset().top <= windowScroll + 10) {
                    lastElement = $(this).attr('id');
                }
            });

            if (lastElement > 0) {
                var ID = lastElement,
                    elemID = ID - 1,
                    hID = '#' + ID,
                    liID = '#step' + ID;

                var howMuchScroll = 0;
                $(linkWrapper + ' a').parent('li').slice(0, elemID).each(function (index) {
                    howMuchScroll += $(this).outerHeight();
                });

                $('.content.hidden-block').scrollTop(howMuchScroll);

                $(linkWrapper + ' a').parent('li').removeClass('active');
                $(linkWrapper + ' a[href="'+ hID +'"]').parent('li').addClass('active');
            }
        },

        /**
         * Title bar change position.
         * @method
         * @instance
         */
        titleBarChangePosition: function() {
            var header = this.options.header,
                container = this.options.containerLinkWrapper,
                windowWidth = window.window.innerWidth;

            var linkWrapper = this.options.linkWrapper;

            var windowScroll = $(window).scrollTop(),
                hHeader = $(header).height(),
                containerPnl = $(container);

            if (windowWidth > 991) {
                if (windowScroll > hHeader) {
                    // calculate the height
                    var minusHeight = 130; // 90px of header + 40px of padding bottom
                    var calculatedHeight = $(window).height() - minusHeight;
                    containerPnl.parent('.content').css('height', calculatedHeight);
                    containerPnl.parent('.content').addClass('fixed-menu');
                } else {
                    containerPnl.parent('.content').css('height', 'auto');
                    containerPnl.parent('.content').removeClass('fixed-menu');
                    $(linkWrapper + ' a').parent('li').removeClass('active');
                }
            }
        }, 

        /**
         * Side panel reaction to footer.
         * @method
         * @instance
         */
        titleBarReactionToFooter: function() {
            var header = this.options.header,
                mainContainer = this.options.mainContainer,
                container = this.options.containerLinkWrapper;

            var hHeader = $(header).height(),
                hMainConteiner = $('.js-article-content').height() - $(window).height(),
                windowScroll = $(window).scrollTop(),
                containerPnl = $(container);

            if (windowScroll >= hMainConteiner) {
                containerPnl.parent('.content').removeClass('fixed-menu');
            }
        }
    };
    $.fn.articleMenu = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || ! method) {
            return methods.onInit.apply(this, arguments);
        } else {
            $.error('No method');
        }
    }
}(jQuery));

/** Initialization plugin on landing page. */
$("body").articleMenu({
    header: '.keyua-screen',
    containerLinkWrapper: '.js-table-content',
    linkWrapper: '.js-table-content',
    mainContainer: '.js-article-content',
    contentArea: '.js-article-content'
});