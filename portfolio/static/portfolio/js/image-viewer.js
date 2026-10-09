(() => {
    const dialog = document.querySelector('.pf-image-viewer');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    const image = dialog.querySelector('img');
    const caption = dialog.querySelector('.pf-viewer-caption');
    const size = dialog.querySelector('.pf-viewer-size');
    const close = dialog.querySelector('.pf-viewer-close');
    const stage = dialog.querySelector('.pf-viewer-stage');
    let trigger;
    const fit = () => {
        dialog.classList.remove('is-actual');
        size.textContent = 'Actual size';
        size.setAttribute('aria-pressed', 'false');
        stage.scrollTop = stage.scrollLeft = 0;
    };
    document.querySelectorAll('a.pf-image-zoom').forEach(link => {
        const thumbnail = link.querySelector('img');
        const originalUrl = link.getAttribute('href');
        const label = `Enlarge image: ${thumbnail.alt || 'Case study image'}`;
        const stacked = window.matchMedia(link.closest('.pf-admin-case-media')
            ? '(max-width: 64rem)' : '(max-width: 48rem)');
        const updateAvailability = () => {
            link.toggleAttribute('data-zoom-disabled', stacked.matches);
            if (stacked.matches) {
                link.removeAttribute('href');
                link.removeAttribute('aria-label');
                if (dialog.open && trigger === link) dialog.close();
            } else {
                link.setAttribute('href', originalUrl);
                link.setAttribute('aria-label', label);
            }
        };
        updateAvailability();
        stacked.addEventListener('change', updateAvailability);
        link.addEventListener('click', event => {
            if (stacked.matches) return;
            if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            trigger = link;
            fit();
            image.src = link.href;
            image.alt = thumbnail.alt;
            caption.textContent = link.closest('figure')?.querySelector('figcaption')?.textContent.trim() || thumbnail.alt;
            dialog.showModal();
            document.documentElement.classList.add('pf-viewer-open');
            close.focus();
        });
    });
    size.addEventListener('click', () => {
        const actual = dialog.classList.toggle('is-actual');
        size.textContent = actual ? 'Fit to screen' : 'Actual size';
        size.setAttribute('aria-pressed', String(actual));
        stage.scrollTop = stage.scrollLeft = 0;
    });
    close.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
        const rect = dialog.getBoundingClientRect();
        if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => {
        document.documentElement.classList.remove('pf-viewer-open');
        image.removeAttribute('src');
        trigger?.focus({preventScroll: true});
    });
})();
