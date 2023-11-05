import React, { useState } from 'react';
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

const ReportsMovements = () => {
  const [products, setProducts] = useState([]);
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');

  const getProductsMovements = async () => {
    const response = await ReportsService.productsMovements(startTime, endTime);
    if(response) {
      setProducts(response);
    } else {
      alert("Couldn't get products movements");
    }
  }

  return(
    <MainLayout>
      <Grid align='center' style={{width: '100%', margin: 'auto'}}>
        <Grid align='center' >
            <h2>Product movements (inputs and outputs)</h2>
        </Grid>
        <Grid>
          <p>Enter start time and end time for the report in the format YYYY-MM-DDTHH:MM:SS and proceed to click the Filter button</p>
          <div style={{display: 'flex', flexDirection: 'row', height: 56, marginBottom: 32, justifyContent: 'center'}}>
            <TextField 
              onChange={(e) => setStartTime(e.target.value)}
              value={startTime}
              label='Start time' 
              placeholder='YYYY-MM-DDTHH:MM:SS'
              variant="outlined"
              required 
              style={{marginBottom: 16, marginRight: 16}}
            />
            <TextField 
              onChange={(e) => setEndTime(e.target.value)}
              value={endTime}
              label='End time' 
              placeholder='YYYY-MM-DDTHH:MM:SS'
              variant="outlined"
              required 
              style={{marginBottom: 16, marginRight: 16}}
            />
            <Button color='primary' variant="contained" onClick={getProductsMovements}>Filter</Button>
          </div>
        </Grid>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell align="right">Quantity</TableCell>
                <TableCell align="right">Timestamp</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {products.sort((a,b) => a.timestamp - b.timestamp).map((product) => (
                <TableRow
                  key={product.timestamp}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {product.id}
                  </TableCell>
                  <TableCell align="right">{product.quantity}</TableCell>
                  <TableCell align="right">{product.timestamp}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </MainLayout>
  )
}

export default ReportsMovements