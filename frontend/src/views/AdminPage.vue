<template>
  <div class="admin-data">
    <h1>Project Records</h1>

    <div v-if="error" class="status-message error">
      {{ error }}
    </div>

    <div v-if="data.length && !error">
      <div>
        <h3>Status Distribution</h3>
        <PieChart :chart-data="statusChartData" :chart-options="chartOptions" />
      </div>

      <div>
        <h3>Projects by Enrollment Term</h3>
        <BarChart :chart-data="termChartData" :chart-options="chartOptions" />
      </div>

      <div>
        <h3>Total Projects</h3>
        <BarChart
          :chart-data="totalProjectsData"
          :chart-options="chartOptions"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { Bar, Pie } from "vue-chartjs";
import axios from "axios";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
);

export default defineComponent({
  name: "AdminData",
  components: { BarChart: Bar, PieChart: Pie },
  setup() {
    const data = ref([]);
    const error = ref(null);

    const statusChartData = ref(null);
    const termChartData = ref(null);
    const totalProjectsData = ref(null);

    const chartOptions = {
      responsive: true,
      plugins: {
        legend: { display: true, position: "top" },
        title: { display: true, text: "Project Statistics" },
      },
    };

    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/admin/get_data",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        data.value = response.data.data;
        prepareChartData();
      } catch (err) {
        error.value =
          err.response?.data?.error || "Unable to load data. Please try again.";
      }
    };

    const prepareChartData = () => {
      const completedCount = data.value.filter((d) => d.completed).length;
      const inProgressCount = data.value.length - completedCount;

      statusChartData.value = {
        labels: ["Completed", "In Progress"],
        datasets: [
          {
            label: "Projects",
            backgroundColor: ["#4caf50", "#ff9800"],
            data: [completedCount, inProgressCount],
          },
        ],
      };

      const termCounts = data.value.reduce((acc, curr) => {
        acc[curr.enrollment_term] = (acc[curr.enrollment_term] || 0) + 1;
        return acc;
      }, {});

      termChartData.value = {
        labels: Object.keys(termCounts),
        datasets: [
          {
            label: "Projects",
            backgroundColor: "#2196f3",
            data: Object.values(termCounts),
          },
        ],
      };

      const projectCounts = data.value.reduce((acc, curr) => {
        acc[curr.project_name] = (acc[curr.project_name] || 0) + 1;
        return acc;
      }, {});

      totalProjectsData.value = {
        labels: Object.keys(projectCounts),
        datasets: [
          {
            label: "Projects",
            backgroundColor: "#673ab7",
            data: Object.values(projectCounts),
          },
        ],
      };

      console.log("Chart Data Prepared", {
        statusChartData: statusChartData.value,
        termChartData: termChartData.value,
        totalProjectsData: totalProjectsData.value,
      });
    };

    onMounted(() => fetchData());

    return {
      data,
      error,
      statusChartData,
      termChartData,
      totalProjectsData,
      chartOptions,
    };
  },
});
</script>

<style scoped>
.admin-data {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  padding: 20px;
  max-width: 1000px;
  margin: 30px auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-top: 30px;
  text-align: center;
  color: #333;
  margin-bottom: 20px;
  font-size: 2em;
}

h3 {
  text-align: center;
  margin-bottom: 15px;
  font-size: 1.2em;
  font-weight: bold;
  background-color: #4caf50;
  color: white;
  padding: 10px;
  margin-top: 30px;
  border-radius: 5px;
}
</style>
