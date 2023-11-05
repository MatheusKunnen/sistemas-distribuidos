import api from "./api";

class ProductService {
  async create(     
    id,
    name,
    description,
    stock,
    minimumStock,
    price
  ) {
    try {
        const response = await api.post("/product", {
          id: parseInt(id),
          name,
          description,
          stock: parseFloat(stock),
          minimum_stock: parseFloat(minimumStock),
          price: parseFloat(price),
        });
        return response.data;
    } catch (error) {
        console.log("Failed to create product", error);
        return undefined;
    }
  }

  async movement(id, quantity) {
    try {
        const response = await api.post("/product/movement", {
          id: parseInt(id),
          quantity: parseFloat(quantity),
        });
        return response.data;
    } catch (error) {
        console.log("Failed to create product movement", error);
        return undefined;
    }
  }
}

// Create an instance of ProductService
const newInstance = new ProductService();

// Export the instance as the default module export
export default newInstance;
