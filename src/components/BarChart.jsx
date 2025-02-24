import { useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../theme";
import { useEffect, useState } from "react";

const BarChart = ({ isDashboard = false, alpha = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5001/api/chartfilm");
        const data = await response.json();
        const slicedData = data.data.slice(0, 6);
        const updatedChartData = slicedData.map((value, index) => ({
          country: data.labels[index],
          fries: value,
          friesColor: `hsl(${index * 50}, 70%, 50%)`,
        }));
        setChartData(updatedChartData);
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    };

    fetchData();
  }, []);

  const mockBarData2 = [
    {
      country: "Football",
      fries: 1375,
      friesColor: "hsl(275, 70%, 50%)",
    },
    {
      country: "Basketball",
      sandwich: 86,
      "sandwich color": "hsl(72, 70%, 50%)",
    },
    {
      country: "Tennis",
      donut: 120,
      donutColor: "hsl(9, 70%, 50%)",
    },
    {
      country: "Handball",
      kebab: 106,
      kebabColor: "hsl(54, 70%, 50%)",
    },
    {
      country: "Autres",
      "hot dog": 30,
      "hot dogColor": "hsl(208, 70%, 50%)",
    },
  ];

  return (
    <ResponsiveBar
      data={alpha ? chartData : mockBarData2}
      theme={{
        // added
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
      keys={["hot dog", "burger", "sandwich", "kebab", "fries", "donut"]}
      indexBy="country"
      margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
      padding={0.3}
      valueScale={{ type: "linear" }}
      indexScale={{ type: "band", round: true }}
      colors={{ scheme: "nivo" }}
      defs={[
        {
          id: "dots",
          type: "patternDots",
          background: "inherit",
          color: "#38bcb2",
          size: 4,
          padding: 1,
          stagger: true,
        },
        {
          id: "lines",
          type: "patternLines",
          background: "inherit",
          color: "#eed312",
          rotation: -45,
          lineWidth: 6,
          spacing: 10,
        },
      ]}
      borderColor={{
        from: "color",
        modifiers: [["darker", "1.6"]],
      }}
      axisTop={null}
      axisRight={null}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "country", // changed
        legendPosition: "middle",
        legendOffset: 32,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "food", // changed
        legendPosition: "middle",
        legendOffset: -40,
      }}
      enableLabel={false}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{
        from: "color",
        modifiers: [["darker", 1.6]],
      }}
      role="application"
      barAriaLabel={function (e) {
        return e.id + ": " + e.formattedValue + " in country: " + e.indexValue;
      }}
    />
  );
};

export default BarChart;
