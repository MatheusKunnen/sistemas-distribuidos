import api from './api';
import { Buffer } from 'buffer';
class UserService {
  async createAccount(email, password) {
    try {
      const response = await api.post('/user', {
        name: email,
        password: password,
      });
      api.defaults.headers.common['Authorization'] = `Basic ${Buffer.from(
        `${email}:${password}`
      ).toString('base64')}`;
      return response.data;
    } catch (error) {
      api.defaults.headers.common['Authorization'] = null;
      console.log('Failed to create user account', error);
      return undefined;
    }
  }

  async login(email, password) {
    try {
      const token = `Basic ${Buffer.from(`${email}:${password}`).toString(
        'base64'
      )}`;
      console.log(token);
      api.defaults.headers.common['Authorization'] = token;
      const response = await api.post('/login', {
        name: email,
        password: password,
      });

      return response.data;
    } catch (error) {
      api.defaults.headers.common['Authorization'] = null;
      console.log('Failed to login user', error);
      return undefined;
    }
  }
}

// Create an instance of UserService
const newInstance = new UserService();

// Export the instance as the default module export
export default newInstance;
