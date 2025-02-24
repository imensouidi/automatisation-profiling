import { Box, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";

import TrafficIcon from "@mui/icons-material/Traffic";
import Header from "../../components/Header";

import BarChart from "../../components/BarChart";
import StatBox from "../../components/StatBox";
import ManIcon from "@mui/icons-material/Male";

import DriveEtaIcon from "@mui/icons-material/DriveEta";

import MoneyIcon from "@mui/icons-material/Money";

import PieChart from "../../components/PieChart";

import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:5001/api/dashboard_4col"
        );
        const apiData = await response.json();
        const { countByField, maxRevenue } = apiData;

        const updatedData = [
          String(countByField.Genre.homme),
          String(countByField["Permis de conduire"].true),
          String(countByField.Motorisé.true),
          maxRevenue.value,
        ];

        setData(updatedData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="DASHBOARD" subtitle="Bienvenue sur votre dashboard" />
      </Box>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
        {/* ROW 1 */}
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={data[0]}
            subtitle="Homme"
            progress="0.725"
            increase="72%"
            icon={
              <ManIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={data[1]}
            subtitle="Permis de conduire "
            progress="0.36"
            increase="36%"
            icon={
              <TrafficIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={data[2]}
            subtitle="Motorisé"
            progress="0.41"
            increase="41%"
            icon={
              <DriveEtaIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={data[3]}
            subtitle={
              <div
                dangerouslySetInnerHTML={{
                  __html: "Pour les entrepreneurs",
                }}
              />
            }
            progress="0.23"
            increase="23%"
            icon={
              <MoneyIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>

        {/* ROW 2 */}
        <Box
          gridColumn="span 6"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Les equipes favorites
          </Typography>
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          ></Box>
          <Box height="400px" m="-20px 0 0 0">
            <PieChart alpha={false} />
          </Box>
        </Box>
        <Box
          gridColumn="span 6"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          overflow="auto"
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Repartitions des ages
          </Typography>
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="spa ce-between"
            alignItems="center"
          ></Box>

          <Box height="400px" m="-20px 0 0 0">
            <PieChart alpha={true} />
          </Box>
        </Box>
        {/* ROW 3 */}
        <Box
          gridColumn="span 6"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Most common sports
          </Typography>
          <Box height="400px" mt="-20px">
            <BarChart isDashboard={true} alpha={true} />
          </Box>
        </Box>
        <Box
          gridColumn="span 6"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Film categories
          </Typography>
          <Box height="400px" mt="-20px">
            <BarChart isDashboard={true} alpha={false} />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
