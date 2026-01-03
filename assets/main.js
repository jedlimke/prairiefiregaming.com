// Accessible hamburger menu toggle
document.addEventListener('DOMContentLoaded', function() {
	const hamburger = document.querySelector('.hamburger');
	const nav = document.querySelector('.header-area--nav');
	
	if (hamburger && nav) {
		hamburger.addEventListener('click', function() {
			const isExpanded = this.getAttribute('aria-expanded') === 'true';
			this.setAttribute('aria-expanded', !isExpanded);
			this.classList.toggle('is-active');
			nav.classList.toggle('is-active');
		});
		
		// Close menu when clicking outside
		document.addEventListener('click', function(event) {
			if (!hamburger.contains(event.target) && !nav.contains(event.target)) {
				hamburger.setAttribute('aria-expanded', 'false');
				hamburger.classList.remove('is-active');
				nav.classList.remove('is-active');
			}
		});
		
		// Close menu on ESC key
		document.addEventListener('keydown', function(event) {
			if (event.key === 'Escape') {
				hamburger.setAttribute('aria-expanded', 'false');
				hamburger.classList.remove('is-active');
				nav.classList.remove('is-active');
			}
		});
	}
});
