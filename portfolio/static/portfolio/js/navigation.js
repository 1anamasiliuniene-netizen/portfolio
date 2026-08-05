document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.querySelector(".pf-nav-toggle");
    const navMenu = document.querySelector(".pf-nav-menu");
    const dropdown = document.querySelector(".pf-nav-item--dropdown");
    const dropdownToggle = document.querySelector(
    ".pf-nav-dropdown-toggle"
);

    const closeDropdown = () => {
    if (!dropdown || !dropdownToggle) {
        return;
    }

        dropdown.classList.remove("is-open");
        dropdownToggle.setAttribute("aria-expanded", "false");
    };

    const closeNavigation = () => {
        if (!navToggle || !navMenu) {
            return;
        }

        navMenu.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.setAttribute("aria-label", "Open navigation");

        closeDropdown();
    };

    navToggle?.addEventListener("click", () => {
        const isOpen = navMenu.classList.toggle("is-open");

        navToggle.setAttribute("aria-expanded", String(isOpen));
        navToggle.setAttribute(
            "aria-label",
            isOpen ? "Close navigation" : "Open navigation"
        );

        if (!isOpen) {
            closeDropdown();
        }
    });

    dropdownToggle?.addEventListener("click", (event) => {
        if (window.innerWidth > 1024) {
            return;
        }
        event.preventDefault();

        const isOpen = dropdown.classList.toggle("is-open");

        dropdownToggle.setAttribute(
            "aria-expanded",
            String(isOpen)
        );
    });

    navMenu
    ?.querySelectorAll("a:not(.pf-nav-dropdown-toggle)")
    .forEach((link) => {
        link.addEventListener("click", closeNavigation);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeNavigation();
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 1024) {
            closeNavigation();
        }
    });

    document
        .querySelectorAll(".pf-timeline-details")
        .forEach((details) => {
            const label = details.querySelector(
                ".pf-timeline-label"
            );

            if (!label) {
                return;
            }

            const updateLabel = () => {
                label.textContent = details.open
                    ? "Hide"
                    : "Expand";
            };

            updateLabel();
            details.addEventListener("toggle", updateLabel);
        });
});
