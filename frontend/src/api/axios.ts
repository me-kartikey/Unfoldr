import axios from "axios";

// Edited on 13-08-2026: Add withCredentials: true to automatically pass HTTP-only session cookies and handle 401 unauthorized responses globally
const api = axios.create({
    baseURL: "http://localhost:8000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Dispatch custom event to trigger logout/auth-state clear and redirect on frontend
            window.dispatchEvent(new CustomEvent("unauthorized"));
        }
        return Promise.reject(error);
    }
);

export default api;