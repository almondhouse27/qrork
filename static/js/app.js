document.addEventListener("DOMContentLoaded", function () {

// URL and file name input validation --------------------------- //
    const urlInput = document.getElementById("url");
    const fileInput = document.getElementById("file_name") || document.getElementById("filename");
    const button = document.querySelector(".btn button");
    const prefix = "https://";

    if (!urlInput || !fileInput || !button) return;

    urlInput.value = prefix;
    button.disabled = true;

    urlInput.addEventListener("input", function () {
        if (!urlInput.value.startsWith(prefix)) {
            const cursorPos = urlInput.selectionStart;
            const withoutPrefix = urlInput.value.replace(/^https?:\/\//, "");
            urlInput.value = prefix + withoutPrefix;

            if (cursorPos < prefix.length) {
                urlInput.setSelectionRange(prefix.length, prefix.length);
            }
        }
        validate();
    });

    urlInput.addEventListener("keydown", function (e) {
        const start = urlInput.selectionStart;
        if (start <= prefix.length) {
            if (e.key === "Backspace" || e.key === "ArrowLeft") {
                e.preventDefault();
                urlInput.setSelectionRange(prefix.length, prefix.length);
            }
        }
    });

    fileInput.addEventListener("input", validate);



// Button enable/disable logic --------------------------- //
    function isValidUrl(url) {
        if (url === prefix) return false;
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    function validate() {
        const url = urlInput.value.trim();
        const file = fileInput.value.trim();
        button.disabled = !(isValidUrl(url) && file);
    }



// Radio button watcher --------------------------- //
    const fileFormatRadios = document.querySelectorAll('input[name="file_format"]');
    const themeRadios = document.querySelectorAll('input[name="theme"]');
    const defaultTheme = document.querySelector('input[name="theme"][value="default"]');

    function updateThemeRadios() {
        const svgSelected = document.querySelector('input[name="file_format"][value="svg"]').checked;
        if (svgSelected) {
            themeRadios.forEach(radio => {
                if (radio.value !== "default") {
                    radio.disabled = true;
                } else {
                    radio.disabled = false;
                    radio.checked = true;
                }
            });
        } else {
            themeRadios.forEach(radio => {
                radio.disabled = false;
            });
        }
    }

    fileFormatRadios.forEach(radio => {
        radio.addEventListener('change', updateThemeRadios);
    });

    updateThemeRadios();



// Modal help logic --------------------------- //
    const helpBtn = document.querySelector('.fa-question');
    const modal = document.getElementById('help-modal');
    const closeBtn = document.getElementById('close-help');

    if (helpBtn && modal && closeBtn) {
        helpBtn.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex';
        });
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
        window.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
});
