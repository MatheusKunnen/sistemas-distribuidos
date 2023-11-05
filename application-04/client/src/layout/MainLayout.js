import React from 'react'
import Menu from '../components/Menu';
import './styles.css';
import { Paper } from '@material-ui/core'

const MainLayout = ({children}) => {
    return(
        <div className='layout'>
            <Paper elevation={10} style={{minWidth: 300}}>
                <Menu/>
            </Paper>
            <div style={{padding: 48, minHeight: '100vh'}}>{children}</div>
        </div>
    )
}

export default MainLayout