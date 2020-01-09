Vue.component('reviews-carousel', {
	template: `
        <div class="feedback-block">

            <div
                v-for="(review, index) in currentItems"
                class="info-block"
                :style="'background-color:' + review.background_color"
            >
                <div class="row">
                    <div class="col-md-8 col-md-offset-2">
                        <div class="customer-name">
                            {{ review.name }}
                        </div>
                        <div class="feedback-text">
                            {{ review.text }}
                        </div>
                        <img v-if="review.photo" :src="review.photo" class="customer-photo" />
                        <div class="customer-post">
                            {{ review.position }}
                        </div>
                    </div>
                </div>
            </div>

            <div v-show="pagesList.length > 1" class="row">
                <div class="col-md-12">
                    <div class="buttons-feedback">
                        <button @click="changePage('next', true)" type="button" class="left"></button>
                        <button @click="changePage('prev', true)" type="button" class="right"></button>
                    </div>
                </div>
            </div>

        </div>
	`,
	created: function () {
		var self = this;
		var windowWidth = window.window.innerWidth;

		// Defaul value
		self.itemsOnPage = 1;

		axios.get(API_URL, {
		    params: {
		      	component: 'reviews',
		      	page: CURRENT_PAGE
		    }
		}).then(function (response) {
    		self.items = response.data;
            self.initNextSlideInterval();
  		})

	},
	data: function () {
		return {
			currentPage: 1,
			showCarousel: true,
			items: [],
            SECONDS_DELAY: 8,
            nextSlideInterval: false
		}
	},
	methods: {
        /**
         * Init auto slides.
         *
         * @method
         * @instance
         */
        initNextSlideInterval: function() {
            var self = this;

            if (self.nextSlideInterval) {
                clearInterval(self.nextSlideInterval);
            }

            self.nextSlideInterval = setInterval(function() {
                self.changePage('next', false);
            }, self.SECONDS_DELAY * 1000);
        },
        /**
         * Returns maximum pages count for carousel.
         *
         * @method
         * @instance
         * @returns {Number}
         */
		getPagesCount: function () {
			return Math.ceil(this.items.length/this.itemsOnPage);
		},
        /**
         * Returns end index for items array for given page.
         *
         * @method
         * @instance
		 * @param {Number}  page
         * @returns {Number}
         */
		getEndIndex: function (page) {
			return page*this.itemsOnPage;
		},
        /**
         * Returns start index for items array for given page.
         *
         * @method
         * @instance
		 * @param {Number}  page
         * @returns {Number}
         */
		getStartIndex: function (page) {
			return this.getEndIndex(page)-this.itemsOnPage;
		},
        /**
         * Returns array of items for given page.
         *
         * @method
         * @instance
		 * @param {Number}  page
		 * @param {Array} items
         * @returns {Array}
         */
		getItemsForPage: function (page, items) {
			var endItemIndex = this.getEndIndex(page);
			var startItemIndex = this.getStartIndex(page);

			return items.slice(startItemIndex, endItemIndex);
		},
        /**
         * Changes the page for carousel.
         *
         * @method
         * @instance
		 * @param {String} target
         * @returns {Number}
         */
		changePage: function (target, clearInterval) {
			var self = this;
			self.showCarousel = false;

            if (clearInterval) {
                self.initNextSlideInterval();
            }

			setTimeout(function () {
				self.showCarousel = true;
			}, 300);

			var pages = self.pagesList;
			var currentPageIndex = pages.indexOf(self.currentPage);
			var nextPageIndex = target === 'next' ? currentPageIndex + 1 : currentPageIndex - 1;

			if (pages[nextPageIndex] === undefined) {
				nextPageIndex = target === 'next' ? 0 : pages.length-1;
			}

			self.currentPage = pages[nextPageIndex];
			return self.currentPage;
		},
	},
	computed: {
        /**
         * Returns array of indexes for slider pages.
         *
         * @method
         * @instance
         * @returns {Array}
         */
		pagesList: function () {
			var pages = [];
			var pagesCount = this.getPagesCount();

			for (var i=1; i<=pagesCount; i++) {
				pages.push(i);
			}
			return pages;
		},
        /**
         * Returns the main items array for current page.
         *
         * @method
         * @instance
         * @returns {Array}
         */
		currentItems: function () {
			return this.getItemsForPage(this.currentPage, this.items);
		},
	}
})

Vue.component('achivements-carousel', {
    template: `
        <div>
            <transition-group name="fade">
                <div
                    v-if="showCarousel"
                    v-for="(text, index) in currentItems"
                    :key="index" class="text"
                >{{ text }}</div>
            </transition-group>
            <div class="carusel">
                <span
                    v-for="(page, index) in pagesList"
                    :key="index"
                    :class="page === currentPage ? 'active' : ''"
                    @click="changePage(page, true)"
                ></span>
            </div>
        </div>
    `,
    created: function () {
        var self = this;

        // Defaul value
        self.itemsOnPage = 1;

        var input = document.getElementById("achievements").value;
        self.items = input.split(',');
        self.initNextSlideInterval();
    },
    data: function () {
        return {
            currentPage: 1,
            showCarousel: true,
            items: [],
            SECONDS_DELAY: 4,
            nextSlideInterval: false
        }
    },
    methods: {
        /**
         * Init auto slides.
         *
         * @method
         * @instance
         */
        initNextSlideInterval: function() {
            var self = this;

            if (self.nextSlideInterval) {
                clearInterval(self.nextSlideInterval);
            }

            self.nextSlideInterval = setInterval(function() {
                self.nextPage('next', false);
            }, self.SECONDS_DELAY * 1000);
        },
        /**
         * Returns maximum pages count for carousel.
         *
         * @method
         * @instance
         * @returns {Number}
         */
        getPagesCount: function () {
            return Math.round(this.items.length/this.itemsOnPage);
        },
        /**
         * Returns end index for items array for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @returns {Number}
         */
        getEndIndex: function (page) {
            return page*this.itemsOnPage;
        },
        /**
         * Returns start index for items array for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @returns {Number}
         */
        getStartIndex: function (page) {
            return this.getEndIndex(page)-this.itemsOnPage;
        },
        /**
         * Returns array of items for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @param {Array} items
         * @returns {Array}
         */
        getItemsForPage: function (page, items) {
            var endItemIndex = this.getEndIndex(page);
            var startItemIndex = this.getStartIndex(page);

            return items.slice(startItemIndex, endItemIndex);
        },
        /**
         * Changes the page for carousel.
         *
         * @method
         * @instance
         * @param {String} target
         * @returns {Number}
         */
        nextPage: function (target, clearInterval) {
            var self = this;
            self.showCarousel = false;

            setTimeout(function () {
                self.showCarousel = true;
            }, 300);

            if (clearInterval) {
                self.initNextSlideInterval();
            }

            var pages = self.pagesList;
            var currentPageIndex = pages.indexOf(self.currentPage);
            var nextPageIndex = target === 'next' ? currentPageIndex + 1 : currentPageIndex - 1;

            if (pages[nextPageIndex] === undefined) {
                nextPageIndex = target === 'next' ? 0 : pages.length-1;
            }

            self.currentPage = pages[nextPageIndex];
            return self.currentPage;
        },
        /**
         * Changes the page for carousel.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @returns {Number}
         */
        changePage: function (page, clearInterval) {
            var self = this;
            self.showCarousel = false;

            if (clearInterval) {
                self.initNextSlideInterval();
            }

            setTimeout(function () {
                self.showCarousel = true;
            }, 300);

            self.currentPage = page;
            return self.currentPage;
        },
    },
    computed: {
        /**
         * Returns array of indexes for slider pages.
         *
         * @method
         * @instance
         * @returns {Array}
         */
        pagesList: function () {
            var pages = [];
            var pagesCount = this.getPagesCount();

            for (var i=1; i<=pagesCount; i++) {
                pages.push(i);
            }
            return pages;
        },
        /**
         * Returns the main items array for current page.
         *
         * @method
         * @instance
         * @returns {Array}
         */
        currentItems: function () {
            return this.getItemsForPage(this.currentPage, this.items);
        },
    }
})

Vue.component('gallery-carousel', {
    template: `
        <div
            v-if="currentItems"
            class="slider"
            @touchstart="startDrag"
            @touchend="stopDrag"
        >
            <!--div v-if="pagesList.length > 1" class="s-pagination">
                <a href="#" @click.prevent="changePage('prev', true)" class="prev"></a>
                <a href="#" @click.prevent="changePage('next', true)" class="next"></a>
            </div-->
            <div class="row">
                <div class="col-md-6">
                    <div class="info">
                        <transition name="fade">
                            <div v-if="showCarousel" class="cell">
                                <div class="title">{{ currentItems.title }}</div>
                                <div class="text">{{ currentItems.description }}</div>
                            </div>
                        </transition>
                    </div>
                </div>
                <transition name="fade">
                    <div v-if="showCarousel" class="col-md-6">
                        <img :src="'/media/' + currentItems.background" />
                    </div>
                </transition>
            </div>

            <div
                v-if="pagesList.length > 1"
                class="line-pagination"
                :style="marginLeftValue"
            >
                <a
                    href="#"
                    v-for="(page, index) in pagesList"
                    :class="page === currentPage ? 'active' : ''"
                    :key="index"
                    @click.prevent="showPage(page, true)"
                ></a>
            </div>
        </div>
    `,
    created: function () {
        var self = this;
        var windowWidth = window.window.innerWidth;

        axios.get(API_URL, {
            params: {
                component: 'gallery',
                page: CURRENT_PAGE
            }
        }).then(function (response) {
            self.items = response.data;
            self.preload(self.items);
            if (windowWidth > 768) {
                self.initNextSlideInterval();
            }
        });
    },
    data: function () {
        return {
            currentPage: 1,
            showCarousel: true,
            itemsOnPage: 1,
            items: [],
            SECONDS_DELAY: 10,
            nextSlideInterval: false,
            loadedImages: [],
            // record drag start point
            start: { x: 0, y: 0 },
            stop: { x: 0, y: 0 },
        }
    },
    methods: {
        startDrag: function (e) {
            e = e.changedTouches ? e.changedTouches[0] : e;
            this.start.x = e.pageX;
            this.start.y = e.pageY;
        },
        stopDrag: function (e) {
            e = e.changedTouches ? e.changedTouches[0] : e;
            this.stop.x = e.pageX;
            this.stop.y = e.pageY;

            if (this.stop.x < this.start.x && (this.start.x - this.stop.x) > 50) {
                this.changePage('next');
            }
            if (this.stop.x > this.start.x && (this.stop.x - this.start.x > 50)) {
                this.changePage('prev');
            }
        },
        /**
         * Preload all images to optimize gallery loading.
         *
         * @method
         * @instance
         */
        preload: function(imageArray, index) {
            let self = this;

            index = index || 0;
            if (imageArray && imageArray.length > index) {
                var img = new Image ();
                img.onload = function() {
                    self.loadedImages.push(img);
                    self.preload(imageArray, index + 1);
                }
                img.src = '/media/' + self.items[index].background;
            }
        },
        /**
         * Init auto slides.
         *
         * @method
         * @instance
         */
        initNextSlideInterval: function() {
            var self = this;

            if (self.nextSlideInterval) {
                clearInterval(self.nextSlideInterval);
            }

            self.nextSlideInterval = setInterval(function() {
                self.changePage('next', false);
            }, self.SECONDS_DELAY * 1000);
        },
        /**
         * Returns maximum pages count for carousel.
         *
         * @method
         * @instance
         * @returns {Number}
         */
        getPagesCount: function () {
            return Math.round(this.items.length/this.itemsOnPage);
        },
        /**
         * Returns end index for items array for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @returns {Number}
         */
        getEndIndex: function (page) {
            return page*this.itemsOnPage;
        },
        /**
         * Returns start index for items array for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @returns {Number}
         */
        getStartIndex: function (page) {
            return this.getEndIndex(page)-this.itemsOnPage;
        },
        /**
         * Returns array of items for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @param {Array} items
         * @returns {Array}
         */
        getItemsForPage: function (page, items) {
            var endItemIndex = this.getEndIndex(page);
            var startItemIndex = this.getStartIndex(page);

            return items.slice(startItemIndex, endItemIndex)[0];
        },
        /**
         * Shows the page for carousel.
         *
         * @method
         * @instance
         * @param {Number} page
         * @param {Boolean} clearInterval
         * @returns {Number}
         */
        showPage: function (page, clearInterval) {
            var self = this;
            self.showCarousel = false;
            var windowWidth = window.window.innerWidth;

            if (clearInterval && windowWidth > 768) {
                self.initNextSlideInterval();
            }

            setTimeout(function () {
                self.showCarousel = true;
            }, 300);

            self.currentPage = page;
            return self.currentPage;
        },
        /**
         * Changes the page for carousel.
         *
         * @method
         * @instance
         * @param {String} target
         * @param {Boolean} clearInterval
         * @returns {Number}
         */
        changePage: function (target, clearInterval) {
            var self = this;
            self.showCarousel = false;
            var windowWidth = window.window.innerWidth;

            if (clearInterval && windowWidth > 768) {
                self.initNextSlideInterval();
            }

            setTimeout(function () {
                self.showCarousel = true;
            }, 300);

            var pages = self.pagesList;
            var currentPageIndex = pages.indexOf(self.currentPage);
            var nextPageIndex = target === 'next' ? currentPageIndex + 1 : currentPageIndex - 1;

            if (pages[nextPageIndex] === undefined) {
                nextPageIndex = target === 'next' ? 0 : pages.length-1;
            }

            self.currentPage = pages[nextPageIndex];
            return self.currentPage;
        },
    },
    computed: {
        /**
         * Returns array of indexes for slider pages.
         *
         * @method
         * @instance
         * @returns {Array}
         */
        pagesList: function () {
            var pages = [];
            var pagesCount = this.getPagesCount();

            for (var i=1; i<=pagesCount; i++) {
                pages.push(i);
            }
            return pages;
        },
        /**
         * Returns the main items array for current page.
         *
         * @method
         * @instance
         * @returns {Array}
         */
        currentItems: function () {
            return this.getItemsForPage(this.currentPage, this.items);
        },
        /**
         * Returns the value for margin-left and width for pagination block.
         *
         * @method
         * @instance
         * @returns {String}
         */
        marginLeftValue: function() {
            let linkMargin = 7;
            let buttonWidth = 24 + linkMargin;

            let blockWidth = this.pagesList.length * buttonWidth;
            let margin = blockWidth / 2;
            return `margin-left: -${margin}px;width: ${blockWidth}px;`;
        }
    }
})

Vue.component('logo-carousel', {
    template: `
        <div v-if="currentItems" class="partner-logos">
            <a v-show="pagesList.length > 1" href="#" @click.prevent="changePage('prev')" class="link prev"></a>
            <a v-show="pagesList.length > 1" href="#" class="link next" @click.prevent="changePage('next')"></a>
            <div class="row">
                <transition-group name="fade">
                    <div
                        v-if="showCarousel"
                        v-for="(logo, index) in currentItems"
                        :key="index"
                        class="col-md-3 col-sm-6 col-xs-12"
                    >
                        <a :href="logo.url" class="logo" target="_blank" rel="nofollow">
                            <img :src="'/media/' + logo.logo" alt="" />
                        </a>
                    </div>
                </transition-group>
            </div>
        </div>
    `,
    created: function () {
        var self = this;
        var windowWidth = window.window.innerWidth;

        // Defaul value
        self.itemsOnPage = 4;

        if (windowWidth <= 992) {
            self.itemsOnPage = 2;
        }
        if (windowWidth <= 768) {
            self.itemsOnPage = 1;
        }

        axios.get(API_URL, {
            params: {
                component: 'logo',
                page: CURRENT_PAGE
            }
        }).then(function (response) {
            self.items = response.data;
        })
    },
    data: function () {
        return {
            currentPage: 1,
            showCarousel: true,
            items: []
        }
    },
    methods: {
        /**
         * Returns maximum pages count for carousel.
         *
         * @method
         * @instance
         * @returns {Number}
         */
        getPagesCount: function () {
            return Math.ceil(this.items.length/this.itemsOnPage);
        },
        /**
         * Returns end index for items array for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @returns {Number}
         */
        getEndIndex: function (page) {
            return page*this.itemsOnPage;
        },
        /**
         * Returns start index for items array for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @returns {Number}
         */
        getStartIndex: function (page) {
            return this.getEndIndex(page)-this.itemsOnPage;
        },
        /**
         * Returns array of items for given page.
         *
         * @method
         * @instance
         * @param {Number}  page
         * @param {Array} items
         * @returns {Array}
         */
        getItemsForPage: function (page, items) {
            var endItemIndex = this.getEndIndex(page);
            var startItemIndex = this.getStartIndex(page);

            return items.slice(startItemIndex, endItemIndex);
        },
        /**
         * Changes the page for carousel.
         *
         * @method
         * @instance
         * @param {String} target
         * @returns {Number}
         */
        changePage: function (target) {
            var self = this;
            self.showCarousel = false;

            setTimeout(function () {
                self.showCarousel = true;
            }, 300);

            var pages = self.pagesList;
            var currentPageIndex = pages.indexOf(self.currentPage);
            var nextPageIndex = target === 'next' ? currentPageIndex + 1 : currentPageIndex - 1;

            if (pages[nextPageIndex] === undefined) {
                nextPageIndex = target === 'next' ? 0 : pages.length-1;
            }

            self.currentPage = pages[nextPageIndex];
            return self.currentPage;
        },
    },
    computed: {
        /**
         * Returns array of indexes for slider pages.
         *
         * @method
         * @instance
         * @returns {Array}
         */
        pagesList: function () {
            var pages = [];
            var pagesCount = this.getPagesCount();

            for (var i=1; i<=pagesCount; i++) {
                pages.push(i);
            }
            return pages;
        },
        /**
         * Returns the main items array for current page.
         *
         * @method
         * @instance
         * @returns {Array}
         */
        currentItems: function () {
            return this.getItemsForPage(this.currentPage, this.items);
        },
    }
})
