// Simple mobile menu enhancement + form validation feedback
document.addEventListener('DOMContentLoaded', () => {
    console.log('%c✅ DevInfotech website loaded successfully!', 'color: #0d6efd; font-weight: bold');
    
    // Bootstrap validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});