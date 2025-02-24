import { useState, useContext } from "react";
import { Box, Typography, useTheme } from "@mui/material";
import { Link, useLocation } from "react-router-dom";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import ContactsOutlinedIcon from "@mui/icons-material/ContactsOutlined";
import ReceiptOutlinedIcon from "@mui/icons-material/ReceiptOutlined";
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined";
import GroupIcon from "@mui/icons-material/Group";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import AssignmentIcon from "@mui/icons-material/Assignment";
import { UserContext } from "../authentification/UserContext";
import logo from "./assets/logo.png";

const Item = ({ title, to, icon, selected, setSelected }) => {
  const theme = useTheme();
  const colors = theme.palette;

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        padding: "5px 35px 5px 20px",
        width: "200px",
        color: colors.grey[100],
        "&:hover": { color: colors.grey[500] },
        marginLeft: "10px",
      }}
      onClick={() => setSelected(title)}
    >
      {icon}
      <Link
        to={to}
        style={{
          marginLeft: "10px",
          color: colors.grey[100],
          textDecoration: "none",
        }}
      >
        {title}
      </Link>
    </Box>
  );
};

const CustomSidebar = () => {
  const theme = useTheme();
  const colors = theme.palette;
  const [selected, setSelected] = useState("Dashboard");
  const location = useLocation();
  const { user, logout } = useContext(UserContext); // 🔥 Récupérer l'utilisateur connecté
  const isSignInPage = location.pathname === "/signin" || location.pathname === "/signup";

  return (
    <Box
      sx={{
        background: colors.primary.main,
        "& a": { textDecoration: "none", color: colors.grey[100] },
        display: isSignInPage ? "none" : "block",
      }}
    >
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center">
        <img
          src={logo}
          alt="Logo"
          style={{ width: "100px", height: "100px", marginBottom: "10px" }}
        />
      </Box>

      <Box my={3}>
        <Box sx={{ background: colors.primary.dark, padding: "10px", borderRadius: "5px", marginTop: "10px", marginBottom: "10px" }}>
          <Item title="Dashboard" to="/dashboard" icon={<HomeOutlinedIcon />} selected={selected} setSelected={setSelected} />
        </Box>

        <Box textAlign="center" sx={{ background: colors.primary.dark, padding: "10px", borderRadius: "5px", marginTop: "10px", marginBottom: "10px" }}>
          <Typography my={2} variant="h6" color="textSecondary">Data</Typography>

          {/* 🔥 Affichage conditionnel : Administration visible uniquement pour les superadmin */}
          {user?.role === "superadmin" && (
            <Item title="Administration" to="/team" icon={<PeopleOutlinedIcon />} selected={selected} setSelected={setSelected} />
          )}

          <Item title="Informations" to="/contacts" icon={<ContactsOutlinedIcon />} selected={selected} setSelected={setSelected} />
          <Item title="Clusters" to="/clusters" icon={<GroupIcon />} selected={selected} setSelected={setSelected} />
          <Item title="Autres" to="/invoices" icon={<ReceiptOutlinedIcon />} selected={selected} setSelected={setSelected} />
        </Box>

        <Box textAlign="center" sx={{ background: colors.primary.dark, padding: "10px", borderRadius: "5px", marginTop: "10px", marginBottom: "10px" }}>
          <Typography my={2} variant="h6" color={colors.grey[300]} mt={2}>Charts</Typography>
          <Item title="Line Chart" to="/line" icon={<TimelineOutlinedIcon />} selected={selected} setSelected={setSelected} />
        </Box>

        <Box textAlign="center" sx={{ background: colors.primary.dark, padding: "10px", borderRadius: "5px", marginTop: "10px", marginBottom: "10px" }}>
          <Typography my={2} variant="h6" color={colors.grey[300]} mt={2}>Authentification</Typography>
          <Item title="Sign In" to="/signin" icon={<LoginIcon />} selected={selected} setSelected={setSelected} />
          <Item title="Sign Out" to="/signin" icon={<LogoutIcon />} selected={selected} setSelected={setSelected} onClick={logout} />
          <Item title="Sign Up" to="/signup" icon={<AssignmentIcon />} selected={selected} setSelected={setSelected} />
        </Box>
      </Box>
    </Box>
  );
};

export default CustomSidebar;
