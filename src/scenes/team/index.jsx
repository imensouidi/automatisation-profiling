import React, { useState, useEffect } from "react";
import { Box, Button, useTheme, Snackbar } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { GridToolbarContainer } from "@mui/x-data-grid";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import MuiAlert from "@mui/material/Alert";
import axios from "axios";
import { saveAs } from "file-saver";
import { tokens } from "../../theme";
import Header from "../../components/Header";

const Team = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  useEffect(() => {
    const fetchTeamData = async () => {
      try {
        const response = await axios.get("http://localhost:5001/api/get_users");
        const teamData = response.data;

        if (!teamData || teamData.length === 0) {
          console.error("Aucune donnée reçue !");
          return;
        }

        // Génération dynamique des colonnes en excluant "status"
        const formattedColumns = Object.keys(teamData[0])
          .filter((key) => key !== "status")
          .map((key) => ({
            field: key,
            headerName: key,
            flex: 1,
          }));

        setColumns(formattedColumns);

        // Ajout d'un ID unique aux lignes
        const formattedRows = teamData.map((row, index) => ({
          id: index + 1,
          ...row,
        }));

        setRows(formattedRows);
      } catch (error) {
        console.error("Erreur lors de la récupération des utilisateurs:", error);
      }
    };

    fetchTeamData();
  }, []);

  const handleToggleStatus = async (id, email, currentStatus) => {
    const newStatus = currentStatus === "Activé" ? "Désactivé" : "Activé";

    try {
      const response = await axios.post("http://localhost:5001/api/changer_statut_utilisateur", {
        email,
        status: newStatus,
      });

      if (response.data.success) {
        setRows((prevRows) =>
          prevRows.map((row) =>
            row.id === id ? { ...row, status: newStatus } : row
          )
        );
      } else {
        console.error("Erreur API:", response.data.message);
      }
    } catch (error) {
      console.error("Erreur lors du changement de statut:", error);
    }
  };

  const handleDeleteRow = (id, status) => {
    if (status === "Désactivé") {
      setRows(rows.filter((row) => row.id !== id));
    } else {
      setShowSnackbar(true);
      setSnackbarMessage("Veuillez désactiver le compte avant de le supprimer.");
    }
  };

  const columnsWithActions = [
    ...columns,
    {
      field: "status",
      headerName: "Status",
      sortable: false,
      renderCell: (params) => (
        <Button
          variant="contained"
          style={{
            backgroundColor: params.row.status === "Activé" ? "green" : "red",
            color: "white",
            fontWeight: "bold",
            minWidth: "100px",
          }}
          onClick={() => handleToggleStatus(params.row.id, params.row.email, params.row.status)}
        >
          {params.row.status ?? "Inconnu"}
        </Button>
      ),
      width: 150,
    },
   
  ];

  return (
    <Box m="20px">
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="ADMINISTRATION" subtitle="Equipe" />
      </Box>

      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": { border: "none" },
          "& .MuiDataGrid-cell": { borderBottom: "none" },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid
          rows={rows}
          columns={columnsWithActions}
          components={{ Toolbar: GridToolbarContainer }}
        />
      </Box>

      <Snackbar open={showSnackbar} autoHideDuration={6000} onClose={() => setShowSnackbar(false)}>
        <MuiAlert onClose={() => setShowSnackbar(false)} severity="warning" sx={{ width: "100%" }}>
          {snackbarMessage}
        </MuiAlert>
      </Snackbar>
    </Box>
  );
};

export default Team;
