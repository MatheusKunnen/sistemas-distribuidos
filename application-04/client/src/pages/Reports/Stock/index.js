import React, { useState, useEffect } from 'react';
import { Grid, TextField, Button } from '@material-ui/core';
import MainLayout from '../../../layout/MainLayout';
import ReportsService from '../../../services/ReportsService';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const ReportsStock = () => {
  const [products, setProducts] = useState([]);

  const getProducts = async () => {
    const response = await ReportsService.productsInStock();
    if(response) setProducts(response);
  }

  useEffect(() => {
    getProducts();
  }, [])

  return(
    <MainLayout>
      <Grid align='center' style={{width: '100%', margin: 'auto'}}>
        <Grid align='center' >
            <h2>Products in stock</h2>
        </Grid>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell align="right">Name</TableCell>
                <TableCell align="right">Description</TableCell>
                <TableCell align="right">Stock</TableCell>
                <TableCell align="right">Minimum stock</TableCell>
                <TableCell align="right">Price</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {products.sort((a,b) => a.id - b.id).map((product) => (
                <TableRow
                  key={product.id}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {product.id}
                  </TableCell>
                  <TableCell align="right">{product.name}</TableCell>
                  <TableCell align="right">{product.description}</TableCell>
                  <TableCell align="right">{product.stock}</TableCell>
                  <TableCell align="right">{product.minimum_stock}</TableCell>
                  <TableCell align="right">{product.price}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </MainLayout>
  )
}

export default ReportsStock