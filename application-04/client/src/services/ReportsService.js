import api from './api';

class ReportsService {
  async productsInStock() {
    try {
      const response = await api.get('/product');
      return response.data;
    } catch (error) {
      console.log('Failed to get products in stock', error);
      return undefined;
    }
  }

  async productsMovements(startTime, endTime) {
    try {
      const response = await api.get('/product/movement', {
        params: {
          startTime,
          endTime,
        },
      });
      return response.data;
    } catch (error) {
      console.log('Failed to get product movements', error);
      return undefined;
    }
  }

  async productsWithoutOutput(startTime, endTime) {
    try {
      const response = await api.get('/product/without-output', {
        params: {
          startTime,
          endTime,
        },
      });
      return response.data;
    } catch (error) {
      console.log('Failed to get product without output', error);
      return undefined;
    }
  }
}

// Create an instance of ReportsService
const newInstance = new ReportsService();

// Export the instance as the default module export
export default newInstance;
