import React, { useState } from 'react'
import { Grid, TextField, Button } from '@material-ui/core'
import MainLayout from '../../../layout/MainLayout';
import ProductService from '../../../services/ProductService';

const ProductCreate = () => {
  const [id, setId] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [stock, setStock] = useState('');
  const [minimumStock, setMinimumStock] = useState('');
  const [price, setPrice] = useState('');

  const btnstyle={margin:'8px 0'}

  const createProduct = async () => {
    const product = await ProductService.create(
      id,
      name,
      description,
      stock,
      minimumStock,
      price
    )
    
    if(product) {
      alert("Product created successfully");
      clearStates();
    } else {
      alert("Couldn't create product");
    }
  }

  const clearStates = () => {
    setId('');
    setName('');
    setDescription('');
    setStock('');
    setMinimumStock('');
    setPrice('');
  }
  
  return(
    <MainLayout>
      <Grid align='center' style={{width: '40%', margin: 'auto'}}>
        <Grid align='center' >
            <h2>Create product</h2>
        </Grid>
        <TextField 
          onChange={(e) => setId(e.target.value)}
          value={id}
          label='Id' 
          placeholder='Product id' 
          variant="outlined"
          type='number'
          fullWidth 
          required 
          style={{marginBottom: 16}}
        />
        <TextField 
          onChange={(e) => setName(e.target.value)}
          value={name}
          label='Name' 
          placeholder='Product name' 
          variant="outlined" 
          fullWidth 
          required 
          style={{marginBottom: 16}}
        />
        <TextField 
          onChange={(e) => setDescription(e.target.value)}
          value={description}
          label='Description' 
          placeholder='Product description' 
          variant="outlined" 
          fullWidth 
          required 
          style={{marginBottom: 16}}
        />
        <TextField 
          onChange={(e) => setStock(e.target.value)}
          value={stock}
          label='Stock' 
          placeholder='Product stock' 
          variant="outlined"
          type='number'
          fullWidth 
          required 
          style={{marginBottom: 16}}
        />
        <TextField 
          onChange={(e) => setMinimumStock(e.target.value)}
          value={minimumStock}
          label='Minimum stock' 
          placeholder='Minimum stock' 
          variant="outlined"
          type='number'
          fullWidth 
          required 
          style={{marginBottom: 16}}
        />
        <TextField 
          onChange={(e) => setPrice(e.target.value)}
          value={price}
          label='Price' 
          placeholder='Product price' 
          variant="outlined"
          type='number'
          fullWidth 
          required 
          style={{marginBottom: 16}}
        />
        <Button color='primary' variant="contained" style={btnstyle} fullWidth onClick={createProduct}>Create Product</Button>
      </Grid>
    </MainLayout>
  )
}

export default ProductCreate