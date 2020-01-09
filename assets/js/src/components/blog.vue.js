Vue.component('blog-carousel', {
	template: `
		<div v-if="currentItems">
	        <div class="blog-content">
	            <div class="row">
	            	<transition-group name="fade">
		                <div
		                	v-for="(article, index) in currentItems"
		                	:key="index"
		                	class="col-md-6"
		                >
		                    <div class="post-big">
		                        <a :href="article.url">
		                            <img :src="'/media/' + article.small_image" alt="" />
		                        </a>
		                        <div class="info">
		                            <a :href="article.url" class="title">{{ article.title }}</a>
		                            <div class="name">{{ article.author }}</div>
		                            <div class="date">{{ article.date }}</div>
		                        </div>
		                    </div>
		                </div>
		            </transition-group>
	            </div>
	        </div> <!-- .blog-content -->

	        <div v-if="pagesList.length > 1" class="page-pagination">
	            <div class="container-fluid">
	                <div class="row">
	                    <div class="col-md-12">
	                        <div class="pages pull-left">
	                            <a
	                            	href="#"
	                            	v-for="(page, index) in pagesList"
	                            	:key="index"
	                            	:class="page === currentPage ? 'active' : ''"
	                            	@click.prevent="showPage(page)"
	                            >{{ page }}</a>
	                        </div>
	                        <div class="buttons pull-left">
	                            <a href="#" @click.prevent="changePage('prev')" class="prev"></a>
	                            <a href="#" @click.prevent="changePage('next')" class="next"></a>
	                        </div>
	                    </div>
	                </div>
	            </div>
	        </div> <!-- .page-pagination -->
	    </div>
	`,
	created: function () {
		var self = this;

		axios.get(API_URL, {
		    params: {
		      	component: 'blog',
		      	category: CURRENT_CATEGORY
		    }
		}).then(function (response) {
    		self.items = response.data;
  		})
	},
	data: function () {
		return {
			currentPage: 1,
			showCarousel: true,
			itemsOnPage: 10,
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
		 * @param {Number}  page
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
        /**
         * Shows the page for carousel.
         *
         * @method
         * @instance
		 * @param {Number} page
         * @returns {Number}
         */
		showPage: function (page) {
			var self = this;
			self.showCarousel = false;

			setTimeout(function () {
				self.showCarousel = true;
			}, 300);

			self.currentPage = page;
			return self.currentPage;
		}
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