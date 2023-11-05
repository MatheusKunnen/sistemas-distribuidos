import React from 'react'
import { Grid, Typography } from '@material-ui/core'
import MainLayout from '../../layout/MainLayout';

const Home = () => {
    return(
      <MainLayout>
        <Grid>
          <Typography>
            Application 4 - Distributed systems - REST and SSE
          </Typography>
        </Grid>
      </MainLayout>
    )
}

export default Home