import React, { useState, useContext } from "react";
import { Box, IconButton, Menu, MenuItem, useTheme, Typography } from "@mui/material";
import { ColorModeContext, tokens } from "../../theme";
import InputBase from "@mui/material/InputBase";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import SearchIcon from "@mui/icons-material/Search";
import { useNavigate, useLocation } from "react-router-dom";
import { UserContext } from "../authentification/UserContext";

const Topbar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const colorMode = useContext(ColorModeContext);
  const { user, logout } = useContext(UserContext);
  
  const [anchorEl, setAnchorEl] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  const sidebarItems = {
    "dashboard": "/",
    "administration": "/team",
    "informations": "/contacts",
    "clusters": "/clusters",
    "autres": "/invoices",
    "line chart": "/line"
  };

  // Vérifie si on est sur la page de connexion ou d'inscription
  if (location.pathname === "/signin" || location.pathname === "/signup") {
    return null;
  }

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate("/signin"); // Redirection vers la page de connexion après déconnexion
  };

  const handleSearch = () => {
    const searchKey = searchTerm.toLowerCase();
    if (sidebarItems[searchKey]) {
      navigate(sidebarItems[searchKey]);
    } else {
      alert("Aucun résultat trouvé");
    }
  };

  return (
    <Box display="flex" justifyContent="space-between" p={2}>
      {/* Barre de recherche */}
      <Box display="flex" backgroundColor={colors.primary[400]} borderRadius="3px">
        <InputBase
          sx={{ ml: 2, flex: 1 }}
          placeholder="Rechercher..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <IconButton type="button" sx={{ p: 1 }} onClick={handleSearch}>
          <SearchIcon />
        </IconButton>
      </Box>

      {/* Icônes et menu utilisateur */}
      <Box display="flex">
        <IconButton onClick={colorMode.toggleColorMode}>
          {theme.palette.mode === "dark" ? <DarkModeOutlinedIcon /> : <LightModeOutlinedIcon />}
        </IconButton>
        <IconButton onClick={handleMenuOpen}>
          <PersonOutlinedIcon />
        </IconButton>
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          transformOrigin={{ vertical: "top", horizontal: "right" }}
        >
          <MenuItem disabled>
            <Typography variant="body1">
              {user ? user.email : "Utilisateur non connecté"}
            </Typography>
          </MenuItem>
          {user && (
            <MenuItem onClick={handleLogout}>Déconnexion</MenuItem>
          )}
        </Menu>
      </Box>
    </Box>
  );
};

export default Topbar;
