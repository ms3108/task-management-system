// Client-side validation and form enhancements
document.addEventListener('DOMContentLoaded', function () {

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            let isValid = true;

            // Check required fields
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;

                    // Add error message if not exists
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'This field is required.';
                        field.parentNode.insertBefore(errorDiv, field.nextSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            // Email validation
            const emailFields = form.querySelectorAll('input[type="email"]');
            emailFields.forEach(field => {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (field.value && !emailPattern.test(field.value)) {
                    field.classList.add('is-invalid');
                    isValid = false;

                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'Please enter a valid email address.';
                        field.parentNode.insertBefore(errorDiv, field.nextSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            // Password confirmation validation
            const passwordField = form.querySelector('input[name="password"]');
            const confirmField = form.querySelector('input[name="confirm_password"]');
            if (passwordField && confirmField) {
                if (passwordField.value !== confirmField.value) {
                    confirmField.classList.add('is-invalid');
                    isValid = false;

                    if (!confirmField.nextElementSibling || !confirmField.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'Passwords do not match.';
                        confirmField.parentNode.insertBefore(errorDiv, confirmField.nextSibling);
                    }
                } else {
                    confirmField.classList.remove('is-invalid');
                }
            }

            if (!isValid) {
                e.preventDefault();
                e.stopPropagation();
            }
        });

        // Real-time validation feedback
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function () {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });

            input.addEventListener('input', function () {
                if (this.classList.contains('is-invalid') && this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.classList.remove('show');
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 150);
            }
        }, 5000);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('button[onclick*="confirm"], input[onclick*="confirm"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
                return false;
            }
        });
    });
});
