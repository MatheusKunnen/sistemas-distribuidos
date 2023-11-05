import React, { useState } from 'react';
import { Grid, TextField, Button } from '@material-ui/core';
import MainLayout from '../../../layout/MainLayout';
import ProductService from '../../../services/ProductService';

const ProductMovement = () => {
  const [id, setId] = useState('');
  const [quantity, setQuantity] = useState('');

  const btnstyle={margin:'8px 0'}

  const createProductMovement = async () => {
    const product = await ProductService.movement(id, quantity);
    
    if(product) {
      alert("Product movement created successfully");
      clearStates();
    } else {
      alert("Couldn't create product movement");
    }
  }

  const clearStates = () => {
    setId('');
    setQuantity('');
  }
  
  return(
    <MainLayout>
      <Grid align='center' style={{width: '40%', margin: 'auto'}}>
        <Grid align='center' >
            <h2>Product entry or output</h2>
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
          onChange={(e) => setQuantity(e.target.value)}
          value={quantity}
          label='Quantity' 
          placeholder='Quantity to input or output' 
          variant="outlined"
          type='number'
          fullWidth 
          required 
          style={{marginBottom: 16}}
        />
        <Button color='primary' variant="contained" style={btnstyle} fullWidth onClick={createProductMovement}>Create Product Movement</Button>
      </Grid>
    </MainLayout>
  )
}

export default ProductMovement