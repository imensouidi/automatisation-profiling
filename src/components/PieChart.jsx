import { ResponsivePie } from "@nivo/pie";
import { tokens } from "../theme";
import { useTheme } from "@mui/material";
import React, { useEffect, useState } from "react";

const PieChart = ({ alpha = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5001/api/chartage");
        const apiData = await response.json();
        const { data, labels } = apiData;

        const updatedChartData = data.map((value, index) => ({
          id: labels[index],
          label: labels[index],
          value,
          color: colors[index % colors.length],
        }));

        setChartData(updatedChartData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const [mockData, setChartData2] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5001/api/chartclub");
        const apiData = await response.json();
        const { data, labels } = apiData;

        const updatedmockData = data.map((value, index) => ({
          id: labels[index],
          label: labels[index],
          value,
          color: colors[index % colors.length],
        }));

        setChartData2(updatedmockData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <ResponsivePie
      data={alpha ? chartData : mockData}
      theme={{
        axis: {
          domain: {
            line: {
              stroke: colors.grey[100],
            },
          },
          legend: {
            text: {
              fill: colors.grey[100],
            },
          },
          ticks: {
            line: {
              stroke: colors.grey[100],
              strokeWidth: 1,
            },
            text: {
              fill: colors.grey[100],
            },
          },
        },
        legends: {
          text: {
            fill: colors.grey[100],
          },
        },
      }}
      margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
      innerRadius={0.5}
      padAngle={0.7}
      cornerRadius={3}
      activeOuterRadiusOffset={8}
      borderColor={{
        from: "color",
        modifiers: [["darker", 0.2]],
      }}
      arcLinkLabelsSkipAngle={10}
      arcLinkLabelsTextColor={colors.grey[100]}
      arcLinkLabelsThickness={2}
      arcLinkLabelsColor={{ from: "color" }}
      enableArcLabels={true}
      arcLabelsRadiusOffset={0.6}
      arcLabelsSkipAngle={10}
      arcLabel={(arc) => `${arc.value}`}
      arcLabelsTextColor={{
        from: "color",
        modifiers: [["darker", 7]],
      }}
      defs={[
        {
          id: "dots",
          type: "patternDots",
          background: "inherit",
          color: "rgba(255, 255, 255, 0.3)",
          size: 4,
          padding: 1,
          stagger: true,
        },
        {
          id: "lines",
          type: "patternLines",
          background: "inherit",
          color: "rgba(255, 255, 255, 0.3)",
          rotation: -45,
          lineWidth: 6,
          spacing: 10,
        },
      ]}
      legends={[
        {
          anchor: "bottom",
          direction: "row",
          justify: false,
          translateX: 0,
          translateY: 56,
          itemsSpacing: 0,
          itemWidth: 100,
          itemHeight: 18,
          itemTextColor: "#999",
          itemDirection: "left-to-right",
          itemOpacity: 1,
          symbolSize: 18,
          symbolShape: "circle",

          effects: [
            {
              on: "hover",
              style: {
                itemTextColor: "#000",
                itemBackground: "#f7fafb",
              },
            },
          ],
        },
      ]}
    />
  );
};

export default PieChart;
