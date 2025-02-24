import React, { useEffect, useState, useContext } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Topbar from "./scenes/global/Topbar";
import CustomSidebar from "./scenes/global/CustomSidebar";
import Dashboard from "./scenes/dashboard";
import Team from "./scenes/team";
import Invoices from "./scenes/invoices";
import Clusters from "./scenes/clusters";
import SignIn from "./scenes/authentification/sign-in";
import SignUp from "./scenes/authentification/sign-up";
import Line from "./scenes/line";
import Contacts from "./scenes/contacts";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "./theme";
import { UserContext } from "./scenes/authentification/UserContext";// 🔥 Importer UserContext

function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const { user } = useContext(UserContext); // 🔥 Récupérer l'utilisateur connecté

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <CustomSidebar isSidebar={isSidebar} />
          <main className="content">
            <Topbar setIsSidebar={setIsSidebar} />
            <Routes>
              {/* Route par défaut vers signin */}
              <Route path="/" element={<Navigate to="/signin" replace />} />
              
              <Route path="/dashboard" element={<Dashboard />} />

              {/* 🔒 Restriction : Seulement pour SuperAdmins */}
              <Route 
                path="/team" 
                element={user?.role === "superadmin" ? <Team /> : <Navigate to="/dashboard" replace />}
              />
              <Route path="/contacts" element={<Contacts />} />
              <Route path="/clusters" element={<Clusters />} />
              <Route path="/invoices" element={<Invoices />} />
              <Route path="/line" element={<Line />} />
              <Route path="/signin" element={<SignIn />} />
              <Route path="/signup" element={<SignUp />} />
              
              {/* Route pour gérer les pages inexistantes */}
              <Route path="*" element={<Navigate to="/signin" replace />} />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
