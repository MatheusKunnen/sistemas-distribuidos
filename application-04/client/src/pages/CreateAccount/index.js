import React, { useState } from 'react'
import { Grid,Paper, Avatar, TextField, Button, Typography,Link } from '@material-ui/core'
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import { useNavigate } from "react-router-dom";
import UserService from '../../services/UserService';

const CreateAccount = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const paperStyle={padding :20,height:'70vh',width:'40vw', margin:"10vh auto"}
    const avatarStyle={backgroundColor:'#1bbd7e'}
    const btnstyle={margin:'8px 0'}

    const handleCreateAccount = async () => {
      const user = await UserService.createAccount(email, password);
      if(user) {
        navigate("/");
      } else {
        alert("Error while creating user");
      }
    }

    return(
        <Grid>
            <Paper elevation={10} style={paperStyle}>
                <Grid align='center'>
                     <Avatar style={avatarStyle}><LockOutlinedIcon/></Avatar>
                    <h2>Sign Up</h2>
                </Grid>
                <TextField 
                  onChange={(e) => setEmail(e.target.value)}
                  value={email}
                  label='Username' 
                  placeholder='Enter username' 
                  variant="outlined" 
                  fullWidth 
                  required 
                  style={{marginBottom: 16}}
                />
                <TextField 
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                  label='Password' 
                  placeholder='Enter password' 
                  type='password' 
                  variant="outlined" 
                  fullWidth 
                  required 
                  style={{marginBottom: 16}}
                />
                <Button color='primary' variant="contained" style={btnstyle} fullWidth onClick={handleCreateAccount}>Sign up</Button>
                <Typography > Already have an account?{' '}
                     <Link href="/" >
                        Sign In 
                </Link>
                </Typography>
            </Paper>
        </Grid>
    )
}

export default CreateAccount