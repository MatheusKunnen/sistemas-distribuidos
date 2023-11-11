import React, { useEffect } from 'react';
import Menu from '../components/Menu';
import './styles.css';
import { Paper } from '@material-ui/core';
import NotificationPanel from '../components/NotificationPanel';

const MainLayout = ({ children }) => {
  useEffect(() => {}, []);
  return (
    <div className="layout">
      <NotificationPanel />
      <Paper elevation={10} style={{ minWidth: 300 }}>
        <Menu />
      </Paper>
      <div style={{ padding: 48, minHeight: '100vh', width: '100%' }}>
        {children}
      </div>
    </div>
  );
};

export default MainLayout;
