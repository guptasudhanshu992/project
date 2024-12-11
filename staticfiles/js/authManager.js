class authManager {
    constructor(apiBaseUrl) {
        this.apiBaseUrl = apiBaseUrl;

        this.access_token = localStorage.getItem("access_token");
        this.refresh_token = localStorage.getItem("refresh_token");

        if (this.access_token){
            this.isUserAuthenticated = true;
        }else{
            this.isUserAuthenticated = false;
        }
    }

    async register(first_name, last_name, email, password, password_confirm, registerButton) {
        try {
            registerButton.disabled = true;
            registerButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating a new account for you...';

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            console.log("first_name: ", first_name);
            console.log("last_name: ", last_name);
            console.log("email: ", email);
            console.log("password: ", password);
            console.log("password_confirm: ", password_confirm);
            console.log("csrfToken: ", csrfToken);


            const response = await fetch(`${this.apiBaseUrl}api/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    first_name,
                    last_name,
                    email,
                    password,
                    password_confirm,
                }),
            });
            registerButton.innerHTML = 'Sign Up';
            registerButton.disabled = false;

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Server responded with an error");
            }
            const data = await response.json();
            console.log(data.message);

            window.location.href="http://127.0.0.1:8000/";
        } catch (error) {
            console.log("Error occurred:", error.message);
        }
    }

    async login(email, password, loginButton) {
        try {
            loginButton.disabled = true;
            loginButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging you in...';

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            const response = await fetch(`${this.apiBaseUrl}api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    email,
                    password,
                }),
            });

            loginButton.innerHTML = 'Login';
            loginButton.disabled = false;

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Server responded with an error");
            }else{
                const responseData = await response.json();
                console.log(responseData);
                const access_token = responseData.access_token;
                const refresh_token = responseData.refresh_token;
                localStorage.setItem("access_token", access_token);
                localStorage.setItem("refresh_token", refresh_token);
                console.log("Login Successful from javascript!");
                window.location.href="http://127.0.0.1:8000/";
            }
        } catch (error) {
            console.log("Error occurred:", error.message);
        }
    }

    decodeJWT(token) {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        return JSON.parse(jsonPayload);
    }

    isAccessTokenValid() {
        if (!this.access_token) {
            console.log("Access token is not present.");
            return false;
        }

        try {
            const decodedToken = this.decodeJWT(this.access_token);

            const currentTime = Math.floor(Date.now() / 1000);

            if (decodedToken.exp < currentTime) {
                console.log("Access token has expired.");
                return false;
            }

            console.log("Access token is valid.");
            return true;
        } catch (error) {
            console.error("Error decoding the access token:", error);
            return false;
        }
    }

    isRefreshTokenValid() {
        if (!this.refresh_token) {
            return false;
        }

        try {
            const decodedToken = this.decodeJWT(this.refresh_token);

            const currentTime = Math.floor(Date.now() / 1000);

            if (decodedToken.exp < currentTime) {
                console.log("Refresh token has expired.");
                return false;
            }

            console.log("Refresh token is valid.");
            return true;
        } catch (error) {
            console.error("Error decoding the refresh token:", error);
            return false;
        }
    }

    async refreshAccessToken() {
        if (!this.refresh_token) {
            console.log("No refresh token available.");
            return false;
        }

        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            const response = await fetch(`${this.apiBaseUrl}token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    refresh_token: refresh_token
                })
            });

            if (!response.ok) {
                throw new Error('Failed to refresh access token');
            }

            const data = await response.json();

            // If new tokens are returned, update them in local storage
            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                // Optional: Update the refresh token if it's provided in the response
                if (data.refresh_token) {
                    localStorage.setItem('refresh_token', data.refresh_token);
                }
                console.log("Access token refreshed successfully.");
                return true;
            } else {
                console.error("No new access token received.");
                return false;
            }
        } catch (error) {
            console.error("Error refreshing access token:", error);
            return false;
        }
    }

    async isUserAuthenticated(){
        try{
            if (this.isAccessTokenValid()){
                return true;
            }else if (!this.isAccessTokenValid() && this.isRefreshTokenValid()){
                return refreshAccessToken();
            }else{
                return false;
            }
        }catch(error){
            console.error(error);
            return false;
        }
    }

    async logout(logout_btn) {
        try {
            logout_btn.disabled = true;
            logout_btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            console.log("You have been logged out.");

            //logout_btn.innerHTML = 'Sign Out';
            logout_btn.disabled = false;

            location.reload();
        } catch (error) {
            console.error("Logout failed:", error);
            alert("An error occurred during logout.");
        }
    }

    async makeProtectedRequest(url, data) {
        try {
            let access_token = localStorage.getItem("access_token");

            const response = await axios.post(url, data, {
                headers: { Authorization: `Bearer ${access_token}` },
            });

            return response.data;

        } catch (error) {
            if (error.response && error.response.status === 401 && error.response.data.code === "token_not_valid") {
                console.log("Access token expired, attempting to refresh...");

                try {
                    const refresh_token = localStorage.getItem("refresh_token");

                    if (!refresh_token) {
                        alert("Session expired. Please log in again.");
                        window.location.href = "/login.html";
                        return;
                    }

                    const refreshResponse = await axios.post(`${this.apiBaseUrl}token/refresh/`, {
                        refresh: refresh_token,
                    });

                    const newAccessToken = refreshResponse.data.access;

                    localStorage.setItem("access_token", newAccessToken);

                    const retryResponse = await axios.post(url, data, {
                        headers: { Authorization: `Bearer ${newAccessToken}` },
                    });

                    return retryResponse.data;

                } catch (refreshError) {
                    console.error("Failed to refresh access token:", refreshError);
                    alert("Session expired. Please log in again.");
                    window.location.href = "/login.html";
                    return;
                }
            } else {
                console.error("Request failed:", error);
                throw error;
            }
        }
    }
}
