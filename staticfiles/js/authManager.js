class authManager {
    constructor(apiBaseUrl) {
        this.apiBaseUrl = apiBaseUrl;
        this.baseAppUrl = "http://127.0.0.1:8000"; // Avoid hardcoding in multiple places
        console.log("initialized");
    }

    async register(first_name, last_name, email, password, password_confirm, registerButton) {
        try {
            registerButton.disabled = true;
            registerButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating a new account for you...';

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            if (!csrfToken) throw new Error("CSRF token is missing");

            const response = await fetch(`${this.apiBaseUrl}register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ first_name, last_name, email, password, password_confirm }),
            });

            const data = await response.json();

            registerButton.innerHTML = 'Sign Up';
            registerButton.disabled = false;

            if (!response.ok) {
                throw new Error(data.error || "Server responded with an error");
            }

            window.location.href = this.baseAppUrl + data.redirect_url;
        } catch (error) {
            console.error("Error occurred:", error.message);
            document.getElementById('error-message').textContent = error.message;
            registerButton.disabled = false;
            registerButton.innerHTML = 'Sign Up';
        }
    }

    async login(email, password, loginButton) {
        try {
            loginButton.disabled = true;
            loginButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging you in...';

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            if (!csrfToken) throw new Error("CSRF token is missing");

            const response = await fetch(`${this.apiBaseUrl}login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            loginButton.innerHTML = 'Login';
            loginButton.disabled = false;

            if (!response.ok) {
                throw new Error(data.error || "Server responded with an error");
            }

            window.location.href = this.baseAppUrl + data.redirect_url;
        } catch (error) {
            console.error("Error occurred:", error.message);
            document.getElementById('error-message').textContent = error.message;
            loginButton.disabled = false;
            loginButton.innerHTML = 'Login';
        }
    }

    async logout(logoutButton) {
        try {
            logoutButton.disabled = true;
            logoutButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            if (!csrfToken) throw new Error("CSRF token is missing");

            const response = await fetch(`${this.apiBaseUrl}logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            });

            const data = await response.json();

            logoutButton.disabled = false;
            logoutButton.innerHTML = 'Sign Out';

            if (!response.ok) {
                throw new Error(data.error || "Server responded with an error");
            }

            window.location.href = this.baseAppUrl + data.redirect_url;
        } catch (error) {
            console.error("Logout failed:", error);
            alert("An error occurred during logout.");
            logoutButton.disabled = false;
            logoutButton.innerHTML = 'Sign Out';
        }
    }
}
