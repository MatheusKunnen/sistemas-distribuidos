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
          id,
          name,
          description,
          stock,
          minimum_stock: minimumStock,
          price
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
            id,
            quantity
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
