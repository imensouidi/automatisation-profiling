import { DataGrid, GridToolbarContainer, GridToolbarColumnsButton, GridToolbarDensitySelector } from "@mui/x-data-grid";
import Header from "../../components/Header";
import DownloadOutlinedIcon from '@mui/icons-material/DownloadOutlined';
import { saveAs } from 'file-saver';
import { Box, useTheme, Button } from "@mui/material";
import { tokens } from "../../theme";

import React, { useState, useEffect } from "react";
import dataframe from "../../data/dataframe.json";

const Contacts = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    // Extract columns from the first row of the dataframe
    const firstRow = dataframe[0];
    const formattedColumns = Object.keys(firstRow).map((key) => {
      return {
        field: key,
        headerName: key,
        flex: 1,
      };
    });
    setColumns(formattedColumns);

    // Assign a unique id to each row and format the rows
    const formattedRows = dataframe.map((row, index) => ({
      id: index + 1,
      ...row,
    }));
    setRows(formattedRows);
  }, []);

  const handleDownload = () => {
    const csvData = convertToCSV(dataframe);
    const blob = new Blob([csvData], { type: "text/csv;charset=utf-8" });
    saveAs(blob, "informations.csv");
  };

  const convertToCSV = (data) => {
    const header = Object.keys(data[0]).join(",");
    const rows = data.map((row) => Object.values(row).join(","));
    return [header, ...rows].join("\n");
  };

  const CustomToolbar = () => {
    return (
      <GridToolbarContainer>
        <GridToolbarColumnsButton />
        <GridToolbarDensitySelector />
      </GridToolbarContainer>
    );
  };

  return (
    <Box m="20px">
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="INFORMATIONS" subtitle="Les informations générales " />
        <Button
          sx={{
            backgroundColor: "blue",
            color: "white",
            fontSize: "14px",
            fontWeight: "bold",
            padding: "10px 20px",
          }}
          onClick={handleDownload}
        >
          <DownloadOutlinedIcon sx={{ marginRight: "10px" }} />
          Télécharger
        </Button>
      </Box>
      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
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
          columns={columns}
          components={{
            Toolbar: CustomToolbar,
          }}
        />
      </Box>
    </Box>
  );
};

export default Contacts;
