<template>
  <div class="grade-chart">
    <h3>📈 Output Target Grade Distribution</h3>

    <div
      v-if="!hasData"
      class="no-chart-data"
    >
      No grade distribution data available.
    </div>

    <div
      v-else
      class="chart-container"
    >
      <canvas ref="canvas"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  watch,
  onMounted,
  onBeforeUnmount,
  computed
} from "vue";

import Chart from "chart.js/auto";

const props = defineProps<{
  data: Record<string, number>;
}>();

const canvas = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const hasData = computed(() => {
  return (
    props.data &&
    Object.keys(props.data).length > 0
  );
});

const drawChart = () => {
  if (!canvas.value || !hasData.value) {
    return;
  }

  if (chart) {
    chart.destroy();
  }

  chart = new Chart(canvas.value, {
    type: "bar",

    data: {
      labels: Object.keys(props.data),

      datasets: [
        {
          label: "Students",
          data: Object.values(props.data),
          backgroundColor: "#3b82f6",
          borderRadius: 6
        }
      ]
    },

    options: {
      responsive: true,
      maintainAspectRatio: false,

      plugins: {
        legend: {
          display: true
        }
      },

      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
};

onMounted(() => {
  drawChart();
});

watch(
  () => props.data,
  () => {
    drawChart();
  },
  {
    deep: true
  }
);

onBeforeUnmount(() => {
  if (chart) {
    chart.destroy();
    chart = null;
  }
});
</script>

<style scoped>
.grade-chart {
  width: 100%;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 400px;
}

.no-chart-data {
  padding: 40px;
  text-align: center;
  color: #64748b;
  background: #f8fafc;
  border-radius: 8px;
}
</style>