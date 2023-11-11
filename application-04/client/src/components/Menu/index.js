import * as React from 'react';
import ListSubheader from '@mui/material/ListSubheader';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import AssessmentIcon from '@mui/icons-material/Assessment';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';
import InventoryIcon from '@mui/icons-material/Inventory';
import DoNotDisturbIcon from '@mui/icons-material/DoNotDisturb';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { Link } from 'react-router-dom';

export default function NestedList() {
  const [openReports, setOpenReports] = React.useState(true);
  const [openProducts, setopenProducts] = React.useState(true);

  return (
    <>
      <List
        sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}
        component="nav"
        aria-labelledby="nested-list-subheader"
        subheader={
          <ListSubheader component="div" id="nested-list-subheader">
            Menu
          </ListSubheader>
        }
      >
        <Link to="/home" style={{ textDecoration: 'none', color: '#000000DE' }}>
          <ListItemButton>
            <ListItemIcon>
              <HomeIcon />
            </ListItemIcon>
            <ListItemText primary="Home" />
          </ListItemButton>
        </Link>
        <ListItemButton onClick={() => setopenProducts(!openProducts)}>
          <ListItemIcon>
            <FormatListBulletedIcon />
          </ListItemIcon>
          <ListItemText primary="Products" />
          {openProducts ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openProducts} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <Link
              to="/product/create"
              style={{ textDecoration: 'none', color: '#000000DE' }}
            >
              <ListItemButton sx={{ pl: 4 }}>
                <ListItemIcon>
                  <AddCircleOutlineIcon />
                </ListItemIcon>
                <ListItemText primary="Create" />
              </ListItemButton>
            </Link>
            <Link
              to="/product/movement"
              style={{ textDecoration: 'none', color: '#000000DE' }}
            >
              <ListItemButton sx={{ pl: 4 }}>
                <ListItemIcon>
                  <TrendingFlatIcon />
                </ListItemIcon>
                <ListItemText primary="Movement" />
              </ListItemButton>
            </Link>
          </List>
        </Collapse>
        <ListItemButton onClick={() => setOpenReports(!openReports)}>
          <ListItemIcon>
            <AssessmentIcon />
          </ListItemIcon>
          <ListItemText primary="Reports" />
          {openReports ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openReports} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <Link
              to="/reports/stock"
              style={{ textDecoration: 'none', color: '#000000DE' }}
            >
              <ListItemButton sx={{ pl: 4 }}>
                <ListItemIcon>
                  <InventoryIcon />
                </ListItemIcon>
                <ListItemText primary="Products in stock" />
              </ListItemButton>
            </Link>
            <Link
              to="/reports/movements"
              style={{ textDecoration: 'none', color: '#000000DE' }}
            >
              <ListItemButton sx={{ pl: 4 }}>
                <ListItemIcon>
                  <TrendingFlatIcon />
                </ListItemIcon>
                <ListItemText primary="Product movements" />
              </ListItemButton>
            </Link>
            <Link
              to="/reports/without-output"
              style={{ textDecoration: 'none', color: '#000000DE' }}
            >
              <ListItemButton sx={{ pl: 4 }}>
                <ListItemIcon>
                  <DoNotDisturbIcon />
                </ListItemIcon>
                <ListItemText primary="Products without ouput" />
              </ListItemButton>
            </Link>
          </List>
        </Collapse>
        <ListItemButton>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItemButton>
      </List>
    </>
  );
}
