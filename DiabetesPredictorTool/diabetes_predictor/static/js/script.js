document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                const closeBtn = message.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                } else {
                    message.style.display = 'none';
                }
            }, 5000); 
        });
    }
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            let isValid = true;
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            
            document.querySelectorAll('.is-invalid').forEach(el => {
                el.classList.remove('is-invalid');
            });
            if (!email.value.trim() || !isValidEmail(email.value.trim())) {
                email.classList.add('is-invalid');
                isValid = false;
            }
            
            if (!password.value.trim()) {
                password.classList.add('is-invalid');
                isValid = false;
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            let isValid = true;
            const username = document.getElementById('username');
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            const confirmPassword = document.getElementById('confirm_password');
            document.querySelectorAll('.is-invalid').forEach(el => {
                el.classList.remove('is-invalid');
            });
            if (!username.value.trim()) {
                username.classList.add('is-invalid');
                isValid = false;
            }
            if (!email.value.trim() || !isValidEmail(email.value.trim())) {
                email.classList.add('is-invalid');
                isValid = false;
            }
            if (!password.value.trim() || !isStrongPassword(password.value.trim())) {
                password.classList.add('is-invalid');
                isValid = false;
            }
            if (password.value.trim() !== confirmPassword.value.trim()) {
                confirmPassword.classList.add('is-invalid');
                isValid = false;
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
        const passwordInput = document.getElementById('password');
        const strengthMeter = document.getElementById('password-strength-meter');
        
        if (passwordInput && strengthMeter) {
            passwordInput.addEventListener('input', function() {
                const strength = calculatePasswordStrength(passwordInput.value);
                updatePasswordStrengthMeter(strength, strengthMeter);
            });
        }
    }
    const predictionForm = document.getElementById('prediction-form');
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredFields = [
                'glucose', 'blood_pressure', 'bmi', 'age'
            ];
            document.querySelectorAll('.is-invalid').forEach(el => {
                el.classList.remove('is-invalid');
            });
            requiredFields.forEach(field => {
                const input = document.getElementById(field);
                if (!input.value.trim() || isNaN(input.value.trim())) {
                    input.classList.add('is-invalid');
                    isValid = false;
                }
            });
            const ageInput = document.getElementById('age');
            if (ageInput && ageInput.value.trim() && parseInt(ageInput.value) < 18) {
                ageInput.classList.add('is-invalid');
                ageInput.nextElementSibling.textContent = 'Age must be at least 18';
                isValid = false;
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    function isValidEmail(email) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(email);
    }
    
    function isStrongPassword(password) {
        return password.length >= 8 && 
               /[A-Z]/.test(password) && 
               /[a-z]/.test(password) && 
               /[0-9]/.test(password);
    }
    function calculatePasswordStrength(password) {
        if (!password) return 0;
        let strength = 0;
        
        const lengthFactor = Math.min(password.length / 12, 1);
        strength += lengthFactor * 30;
        
        if (/[A-Z]/.test(password)) strength += 15;  
        if (/[a-z]/.test(password)) strength += 15;  
        if (/[0-9]/.test(password)) strength += 15;  
        if (/[^A-Za-z0-9]/.test(password)) strength += 15;  
        let typesCount = 0;
        if (/[A-Z]/.test(password)) typesCount++;
        if (/[a-z]/.test(password)) typesCount++;
        if (/[0-9]/.test(password)) typesCount++;
        if (/[^A-Za-z0-9]/.test(password)) typesCount++;
        
        strength += (typesCount - 1) * 5;  
        
        return Math.min(Math.round(strength), 100);
    }
    
    function updatePasswordStrengthMeter(strength, meter) {
        meter.style.width = strength + '%';
        
        if (strength < 30) {
            meter.className = 'progress-bar bg-danger';
            meter.textContent = 'Weak';
        } else if (strength < 70) {
            meter.className = 'progress-bar bg-warning';
            meter.textContent = 'Medium';
        } else {
            meter.className = 'progress-bar bg-success';
            meter.textContent = 'Strong';
        }
    }
});
