import api from "./api";

class UserService {
  async createAccount(email, password) {
    try {
        const response = await api.post("/user", {
            name: email,
            public_key: password,
        });
        return response.data;
    } catch (error) {
        console.log("Failed to create user account", error);
        return undefined;
    }
  }

  async login(email, password) {
    try {
        const response = await api.post("/login", {
            name: email,
            public_key: password,
        });
        return response.data;
    } catch (error) {
        console.log("Failed to login user", error);
        return undefined;
    }
  }
}

// Create an instance of UserService
const newInstance = new UserService();

// Export the instance as the default module export
export default newInstance;
