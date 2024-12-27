(function () {
    // Default options (customize as needed)
    const options = {
        offset: document.getElementById("navigation-bar").getBoundingClientRect().height,
        activeClass: 'active',
        sectionClass: 'scrollspy-section',
        navClass: 'scrollspy-nav',
        linkSelector: 'a',
    };

    // Utility function to get the current scroll position
    function getScrollPosition() {
        return window.pageYOffset || document.documentElement.scrollTop;
    }

    // Function to get the position of an element relative to the viewport
    function getElementOffset(el) {
        const rect = el.getBoundingClientRect();
        return rect.top + window.scrollY;
    }

    // Function to check if an element is in the viewport
    function isInViewport(el, offset = 0) {
        const rect = el.getBoundingClientRect();
        return rect.top <= window.innerHeight - offset && rect.bottom >= offset;
    }

    // Update the active link in the navigation based on the scroll position
    function updateScrollspy() {
        const scrollPos = getScrollPosition();
        const sections = document.querySelectorAll(`.${options.sectionClass}`);
        const navLinks = document.querySelectorAll(`.${options.navClass} ${options.linkSelector}`);

        let activeLinks = []; // Store all active links (both main section and subsection)

        // Loop through each section and check if it's in the viewport
        sections.forEach(section => {
            const sectionOffset = getElementOffset(section);
            const sectionHeight = section.offsetHeight;

            // If the scroll position is within the section's bounds, mark it as active
            if (scrollPos >= sectionOffset - options.offset && scrollPos < sectionOffset + sectionHeight + 17 - options.offset) {
                // Main section link
                const mainSectionLink = document.querySelector(`${options.linkSelector}[href="#${section.id}"]`);
                if (mainSectionLink) {
                    activeLinks.push(mainSectionLink); // Add main section link
                }

                // Subsections links (if any)
                const subsections = section.querySelectorAll('.subsection'); // Assuming subsections are inside the section
                subsections.forEach(subsection => {
                    const subsectionLink = document.querySelector(`${options.linkSelector}[href="#${subsection.id}"]`);
                    if (subsectionLink) {
                        activeLinks.push(subsectionLink); // Add subsection link
                    }
                });
            }
        });

        // Remove active class from all nav links
        navLinks.forEach(link => link.classList.remove(options.activeClass));

        // Add active class to all active links (both main section and subsections)
        activeLinks.forEach(link => {
            link.classList.add(options.activeClass);
        });
    }

    // Event listener for scroll event
    window.addEventListener('scroll', updateScrollspy);
    window.addEventListener('resize', updateScrollspy); // Update on resize

    // Initial update
    updateScrollspy();
})();
