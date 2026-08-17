<template>
  <div class="dashboard-wrapper">
    <main class="dashboard-container">

      <!-- =========================
           PAGE HEADER
      ========================== -->
      <div class="page-title-row">
        <h1 class="page-title">Dashboard Summary</h1>

        <button
          class="btn btn-download title-download-btn"
          @click="handleDownloadTemplate"
        >
          📥 Download Template
        </button>
      </div>


      <div class="grid-layout">

        <!-- =========================
             SIDEBAR
        ========================== -->
        <div class="sidebar-panel">

          <!-- Configuration -->
          <div class="card control-card">

            <h3>⚙️ Configuration Panel</h3>

            <div class="form-group">

              <label class="custom-file-upload">

                <input
                  type="file"
                  accept=".csv"
                  @change="handleFile"
                />

                📁
                {{ file ? file.name : "Choose CSV Dataset" }}

              </label>

              <p class="upload-note">
                Select a CSV file to upload and analyze automatically.
              </p>

            </div>

          </div>


          <!-- Dataset Summary -->
          <div
            class="card info-card"
            v-if="summary"
          >

            <h3>📊 Dataset Summary</h3>

            <div class="summary-stat-row">

              <div class="stat-item">

                <span class="stat-label">
                  Total Records
                </span>

                <span class="stat-val">
                  {{ summary.students ?? 0 }}
                </span>

              </div>


              <div class="stat-item">

                <span class="stat-label">
                  Dimensions
                </span>

                <span class="stat-val">
                  {{ summary.features ?? 0 }} Features
                </span>

              </div>

            </div>


            <button
              class="btn btn-download"
              @click="downloadResult"
            >
              📥 Download Output Data
            </button>

          </div>


          <!-- Model Report -->
          <div
            class="card report-card"
            v-if="metrics"
          >

            <h3>🧾 Model Analysis Report</h3>

            <div class="form-group">

              <label>
                Select Model
              </label>

              <select
                v-model="algorithm"
                class="custom-select"
              >

                <option value="random_forest">
                  Random Forest
                </option>

                <option value="logistic_regression">
                  Logistic Regression
                </option>

                <option value="decision_tree">
                  Decision Tree
                </option>

                <option value="svm">
                  Support Vector Machine (SVM)
                </option>

              </select>

            </div>


            <div class="report-description">

              <p>
                <strong>Selected Model:</strong>
                {{ algorithmName }}
              </p>

              <p>
                <strong>Accuracy:</strong>
                {{ formatPercent(metrics.accuracy) }}
              </p>

              <p>
                <strong>Precision:</strong>
                {{ formatPercent(metrics.precision) }}
              </p>

              <p>
                <strong>Recall:</strong>
                {{ formatPercent(metrics.recall) }}
              </p>

              <p>
                <strong>F1 Score:</strong>
                {{ formatPercent(metrics.f1_score) }}
              </p>

            </div>

          </div>


          <!-- Risk Threshold -->
          <div
            class="card"
            v-if="summary"
          >

            <h3>🚨 AI Risk Configuration</h3>

            <div class="form-group">

              <label>
                Risk Threshold
              </label>

              <input
                v-model.number="riskThreshold"
                type="number"
                min="0"
                max="100"
                class="threshold-input"
              />

              <p class="upload-note">
                Students below this threshold are considered at risk.
              </p>

            </div>

          </div>

        </div>


        <!-- =========================
             MAIN PANEL
        ========================== -->
        <div class="main-panel">


          <!-- Empty -->
          <div
            class="card empty-state"
            v-if="
              !metrics &&
              !comparison &&
              !uploadSuccess
            "
          >

            <div class="empty-icon">
              📊
            </div>

            <h3>
              No Analytics Data Loaded
            </h3>

            <p>
              Please upload a valid student dataset CSV
              to generate metrics and predictions.
            </p>

          </div>


          <!-- Upload success -->
          <div
            class="card empty-state"
            v-if="
              uploadSuccess &&
              !metrics
            "
          >

            <div class="empty-icon">
              ✅
            </div>

            <h3>
              Upload Successful
            </h3>

            <p>
              Processing dataset...
            </p>

          </div>


          <!-- =========================
               KPI
          ========================== -->
          <div
            class="metrics-kpi-grid"
            v-if="metrics"
          >

            <div class="kpi-card accent-blue">

              <span class="kpi-title">
                Accuracy
              </span>

              <span class="kpi-value">
                {{ formatPercent(metrics.accuracy) }}
              </span>

            </div>


            <div class="kpi-card accent-green">

              <span class="kpi-title">
                Precision
              </span>

              <span class="kpi-value">
                {{ formatPercent(metrics.precision) }}
              </span>

            </div>


            <div class="kpi-card accent-orange">

              <span class="kpi-title">
                Recall
              </span>

              <span class="kpi-value">
                {{ formatPercent(metrics.recall) }}
              </span>

            </div>


            <div class="kpi-card accent-purple">

              <span class="kpi-title">
                F1 Score
              </span>

              <span class="kpi-value">
                {{ formatPercent(metrics.f1_score) }}
              </span>

            </div>

          </div>


          <!-- =========================
               STUDENT LOOKUP
          ========================== -->
          <div
            class="card"
            v-if="metrics"
          >

            <h3>
              🔎 Student Lookup
            </h3>

            <div class="lookup-row">

              <input
                v-model="studentId"
                type="text"
                placeholder="Enter Student ID"
                class="lookup-input"
              />

              <button
                class="btn btn-secondary lookup-button"
                @click="lookupStudent"
              >
                Lookup
              </button>

            </div>


            <div
              v-if="studentProfile"
              class="lookup-result"
            >

              <div class="lookup-field">
                <strong>Student ID:</strong>
                {{ studentProfile.Student_ID }}
              </div>

              <div class="lookup-field">
                <strong>Predicted Grade:</strong>
                {{ studentProfile.Predicted_Grade }}
              </div>

              <div class="lookup-field">
                <strong>Actual Grade:</strong>
                {{ studentProfile.Grade ?? "N/A" }}
              </div>

              <div class="lookup-field">

                <strong>
                  Risk Reasons:
                </strong>

                <ul>

                  <li
                    v-for="(reason, index) in studentProfile.risk_reasons || []"
                    :key="index"
                  >
                    {{ reason }}
                  </li>

                </ul>

              </div>

            </div>

          </div>


          <!-- =========================
               MODEL COMPARISON
          ========================== -->
          <div
            class="card"
            v-if="comparison"
          >

            <h3>
              ⚖️ Global Pipeline Evaluation Matrix
            </h3>

            <div class="table-container">

              <table class="modern-table">

                <thead>

                  <tr>

                    <th>
                      Model Strategy
                    </th>

                    <th>
                      Accuracy
                    </th>

                    <th>
                      Precision
                    </th>

                    <th>
                      Recall
                    </th>

                    <th>
                      F1 Score
                    </th>

                  </tr>

                </thead>


                <tbody>

                  <tr
                    v-for="(model, key) in comparison"
                    :key="key"
                    :class="{
                      'highlight-row':
                        key === algorithm
                    }"
                  >

                    <td>
                      <strong>
                        {{
                          String(key)
                            .replaceAll("_", " ")
                            .toUpperCase()
                        }}
                      </strong>
                    </td>

                    <td>
                      {{ formatPercent(model.accuracy) }}
                    </td>

                    <td>
                      {{ formatPercent(model.precision) }}
                    </td>

                    <td>
                      {{ formatPercent(model.recall) }}
                    </td>

                    <td>
                      {{ formatPercent(model.f1_score) }}
                    </td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>


          <!-- =========================
               CHART
          ========================== -->
 <div class="grid-chart-risk">

  <div class="chart-column">

    <div
      class="card chart-card"
      v-if="Object.keys(charts).length > 0"
    >

      <GradeChart
        :data="charts"
      />

    </div>

    <div
      class="card"
      v-else-if="uploadSuccess"
    >
      <h3>📈 Output Target Grade Distribution</h3>

      <div class="no-chart-data">
        No grade distribution data available.
      </div>
    </div>

  </div>

</div>


          <!-- =========================
               AI RISK
          ========================== -->
          <div
            class="card risk-card"
            v-if="summary"
          >

            <div class="risk-header">

              <div>

                <h3>
                  🤖 AI At-Risk Student Roster
                </h3>

                <p class="risk-description">
                  Students identified as potentially
                  at risk by the selected machine
                  learning model.
                </p>

              </div>

              <div class="risk-model">

                <strong>
                  {{ algorithmName }}
                </strong>

              </div>

            </div>


            <!-- Risk statistics -->
            <div class="risk-stat-grid">

              <div class="risk-stat">

                <span>
                  Total Students
                </span>

                <strong>
                  {{ totalStudents }}
                </strong>

              </div>


              <div class="risk-stat">

                <span>
                  At Risk
                </span>

                <strong class="danger-text">
                  {{ atRiskCount }}
                </strong>

              </div>


              <div class="risk-stat">

                <span>
                  Risk Rate
                </span>

                <strong>
                  {{ atRiskPercentage }}%
                </strong>

              </div>


              <div class="risk-stat">

                <span>
                  Threshold
                </span>

                <strong>
                  {{ riskThreshold }}
                </strong>

              </div>

            </div>


            <!-- No risk -->
            <div
              v-if="atRisk.length === 0"
              class="no-risk-message"
            >

              ✅ No at-risk students detected.

            </div>


            <!-- Risk table -->
            <div
              v-else
              class="table-container"
            >

              <table class="modern-table">

                <thead>

                  <tr>

                    <th>
                      Student ID
                    </th>

                    <th>
                      Predicted Grade
                    </th>

                    <th>
                      Actual Grade
                    </th>

                    <th>
                      Risk Reasons
                    </th>

                  </tr>

                </thead>


                <tbody>

                  <tr
                    v-for="student in atRisk"
                    :key="student.Student_ID"
                  >

                    <td>
                      {{ student.Student_ID }}
                    </td>

                    <td>

                      <strong>
                        {{ student.Predicted_Grade }}
                      </strong>

                    </td>

                    <td>
                      {{ student.Actual_Grade ?? "N/A" }}
                    </td>

                    <td>

                      <ul
                        class="risk-reasons"
                      >

                        <li
                          v-for="(
                            reason,
                            index
                          ) in student.risk_reasons || []"
                          :key="index"
                        >
                          {{ reason }}
                        </li>

                      </ul>

                    </td>

                  </tr>

                </tbody>

              </table>

            </div>

          </div>


          <!-- =========================
               FEATURE IMPORTANCE
          ========================== -->
          <div
            class="card"
            v-if="
              featureImportance ||
              featureImportanceMessage
            "
          >

            <h3>
              🧠 Feature Importance
            </h3>


            <p
              v-if="featureImportanceMessage"
              class="feature-unavailable"
            >
              {{ featureImportanceMessage }}
            </p>


            <div
              v-if="featureImportance"
              class="feature-list"
            >

              <div
                v-for="(
                  importance,
                  feature
                ) in featureImportance"
                :key="feature"
                class="feature-item"
              >

                <div class="feature-meta">

                  <span>
                    {{ feature }}
                  </span>

                  <strong>
                    {{
                      (
                        importance * 100
                      ).toFixed(1)
                    }}%
                  </strong>

                </div>


                <div class="feature-bar">

                  <div
                    class="feature-fill"
                    :style="{
                      width:
                        `${Math.min(
                          importance * 100,
                          100
                        )}%`
                    }"
                  ></div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </main>
  </div>
</template>


<script setup lang="ts">


import {
  computed,
  ref,
  watch
} from "vue";

import GradeChart
  from "../components/GradeChart.vue";

import {
  uploadCSV,
  runPrediction,
  getSummary,
  getMetrics,
  getCharts,
  getComparison,
  getAtRiskStudents,
  getStudent,
  getFeatureImportance,
  downloadCSV,
  downloadTemplate
} from "../services/api";


// =====================================================
// STATE
// =====================================================

const file =
  ref<File | null>(null);

const uploadSuccess =
  ref(false);

const summary =
  ref<any>(null);

const metrics =
  ref<any>(null);

const charts =
  ref<Record<string, number>>({});

const comparison =
  ref<any>(null);

const atRisk =
  ref<any[]>([]);

const studentId =
  ref("");

const studentProfile =
  ref<any>(null);

const featureImportance =
  ref<Record<string, number> | null>(null);

const featureImportanceMessage =
  ref<string | null>(null);


// Selected algorithm
const algorithm =
  ref("random_forest");


// Risk threshold
const riskThreshold =
  ref(50);


// Risk statistics
const atRiskCount =
  ref(0);

const totalStudents =
  ref(0);

const atRiskPercentage =
  ref(0);


// =====================================================
// MODEL NAME
// =====================================================

const algorithmName =
  computed(() => {

    switch (algorithm.value) {

      case "random_forest":
        return "Random Forest";

      case "logistic_regression":
        return "Logistic Regression";

      case "decision_tree":
        return "Decision Tree";

      case "svm":
        return "Support Vector Machine (SVM)";

      default:
        return String(
          algorithm.value
        ).replace(/_/g, " ");

    }

  });


// =====================================================
// FILE UPLOAD
// =====================================================

const handleFile = async (e: Event) => {
  const target = e.target as HTMLInputElement;

  if (!target.files || target.files.length === 0) {
    return;
  }

  const selectedFile = target.files[0];

  file.value = selectedFile;

  if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
    alert("Please upload a CSV file.");
    return;
  }

  try {
    await uploadCSV(selectedFile);

    uploadSuccess.value = true;

    await runPredict();

  } catch (error) {
    console.error("Upload failed:", error);

    uploadSuccess.value = false;

    alert("Upload failed.");
  }
};


// =====================================================
// MAIN PREDICTION PIPELINE
// =====================================================

const runPredict = async () => {
  try {

    // =========================
    // 1. Prediction
    // =========================

    const predictionRes =
      await runPrediction(
        algorithm.value
      );

    console.log(
      "Prediction:",
      predictionRes.data
    );


    // =========================
    // 2. Metrics
    // =========================

    const metricsRes =
      await getMetrics(
        algorithm.value
      );

    console.log(
      "Metrics:",
      metricsRes.data
    );

    metrics.value =
      metricsRes.data?.metrics ??
      metricsRes.data ??
      null;


    // =========================
    // 3. Summary
    // =========================

    const summaryRes =
      await getSummary();

    console.log(
      "Summary:",
      summaryRes.data
    );

    summary.value =
      summaryRes.data;


    // =========================
    // 4. Charts
    // =========================

    const chartRes =
      await getCharts(
        algorithm.value
      );

    console.log(
      "Charts:",
      chartRes.data
    );

    charts.value =
      chartRes.data?.grades ??
      {};


    // =========================
    // 5. AI Risk
    // =========================

    await fetchAtRisk();


    // =========================
    // 6. Feature Importance
    // =========================

    await fetchFeatureImportance();


    // =========================
    // 7. Compare Models
    // =========================

    await compareModels();

  } catch (error) {

    console.error(
      "Prediction pipeline failed:",
      error
    );

  }
};

// =====================================================
// CHARTS
// =====================================================

const fetchCharts =
  async () => {

    try {

      const res =
        await getCharts();

      console.log(
        "Charts:",
        res.data
      );


      charts.value =
        res.data?.grades ??
        res.data ??
        {};

    } catch (error) {

      console.error(
        "Charts failed:",
        error
      );

      charts.value =
        {};

    }

  };


// =====================================================
// AI AT RISK
// =====================================================

const fetchAtRisk = async () => {
  try {
    const res = await getAtRiskStudents(
      algorithm.value,
      riskThreshold.value
    );

    console.log("AI Risk Response:", res.data);

    atRisk.value =
      res.data?.students ?? [];

    atRiskCount.value =
      res.data?.at_risk_count ?? 0;

    totalStudents.value =
      res.data?.total_students ?? 0;

    atRiskPercentage.value =
      res.data?.at_risk_percentage ?? 0;

  } catch (error) {
    console.error(
      "Failed to load AI risk students:",
      error
    );

    atRisk.value = [];

    atRiskCount.value = 0;

    totalStudents.value = 0;

    atRiskPercentage.value = 0;
  }
};

// =====================================================
// STUDENT LOOKUP
// =====================================================

const lookupStudent =
  async () => {

    if (!studentId.value) {

      alert(
        "Enter a Student ID."
      );

      return;
    }


    try {

      const res =
        await getStudent(
          studentId.value,
          algorithm.value
        );

      studentProfile.value =
        res.data;


    } catch (error) {

      console.error(
        "Student lookup failed:",
        error
      );

      alert(
        "Student not found."
      );

      studentProfile.value =
        null;

    }

  };


// =====================================================
// FEATURE IMPORTANCE
// =====================================================

const fetchFeatureImportance =
  async () => {

    if (
      algorithm.value ===
        "logistic_regression" ||
      algorithm.value ===
        "svm"
    ) {

      featureImportance.value =
        null;

      featureImportanceMessage.value =
        "Feature importance is unavailable for this model.";

      return;

    }


    try {

      const res =
        await getFeatureImportance(
          algorithm.value
        );


      console.log(
        "Feature importance:",
        res.data
      );


      const data =
        res.data?.features ??
        res.data ??
        [];


      if (
        Array.isArray(data) &&
        data.length
      ) {

        featureImportance.value =
          Object.fromEntries(

            data.map(
              (
                item: {
                  feature: string;
                  importance: number;
                }
              ) => [

                item.feature,
                item.importance

              ]
            )

          );

        featureImportanceMessage.value =
          null;

      } else {

        featureImportance.value =
          null;

        featureImportanceMessage.value =
          "Feature importance is unavailable.";

      }


    } catch (error) {

      console.error(
        "Feature importance failed:",
        error
      );

      featureImportance.value =
        null;

      featureImportanceMessage.value =
        "Feature importance is unavailable.";

    }

  };


// =====================================================
// MODEL COMPARISON
// =====================================================

const compareModels =
  async () => {

    try {

      const res =
        await getComparison();

      console.log(
        "Comparison:",
        res.data
      );


      comparison.value =
        res.data?.results ??
        res.data ??
        null;


    } catch (error) {

      console.error(
        "Comparison failed:",
        error
      );

      comparison.value =
        null;

    }

  };


// =====================================================
// ALGORITHM WATCHER
// =====================================================

watch(
  algorithm,
  async (newAlgorithm) => {

    if (!summary.value) {
      return;
    }

    try {

      console.log(
        "Changing algorithm to:",
        newAlgorithm
      );


      // Prediction
      await runPrediction(
        newAlgorithm
      );


      // Metrics
      const metricsRes =
        await getMetrics(
          newAlgorithm
        );

      metrics.value =
        metricsRes.data?.metrics ??
        metricsRes.data ??
        null;


      // Charts
      const chartRes =
        await getCharts(
          newAlgorithm
        );

      console.log(
        "Updated charts:",
        chartRes.data
      );

      charts.value =
        chartRes.data?.grades ??
        {};


      // AI Risk
      await fetchAtRisk();


      // Feature importance
      await fetchFeatureImportance();


      // Comparison
      await compareModels();

    } catch (error) {

      console.error(
        "Algorithm update failed:",
        error
      );

    }
  }
);


// =====================================================
// RISK THRESHOLD WATCHER
// =====================================================

watch(
  riskThreshold,
  async () => {

    if (
      !summary.value
    ) {
      return;
    }


    console.log(
      "Risk threshold changed:",
      riskThreshold.value
    );


    // algorithm.value is used here
    // because we are NOT inside algorithm watcher

    await fetchAtRisk(
      algorithm.value
    );

  }
);


// =====================================================
// FORMAT PERCENTAGE
// =====================================================

const formatPercent =
  (
    value:
      number | string
  ) => {

    if (
      typeof value ===
      "number"
    ) {

      const percentValue =
        value <= 1
          ? value * 100
          : value;

      return `${percentValue.toFixed(1)}%`;

    }

    return value;

  };


// =====================================================
// DOWNLOAD TEMPLATE
// =====================================================

const handleDownloadTemplate =
  async () => {

    try {

      const res =
        await downloadTemplate();


      const url =
        window.URL.createObjectURL(
          new Blob([
            res.data
          ])
        );


      const link =
        document.createElement(
          "a"
        );

      link.href =
        url;

      link.download =
        "student_upload_template.csv";

      document.body.appendChild(
        link
      );

      link.click();

      document.body.removeChild(
        link
      );


    } catch (error) {

      console.error(
        error
      );

      alert(
        "Template download failed."
      );

    }

  };


// =====================================================
// DOWNLOAD RESULT
// =====================================================

const downloadResult =
  async () => {

    try {

      const res =
        await downloadCSV();


      const url =
        window.URL.createObjectURL(
          new Blob([
            res.data
          ])
        );


      const link =
        document.createElement(
          "a"
        );

      link.href =
        url;

      link.download =
        "prediction_result.csv";

      document.body.appendChild(
        link
      );

      link.click();

      document.body.removeChild(
        link
      );


    } catch (error) {

      console.error(
        "Download failed:",
        error
      );

    }

  };

</script>


<style scoped>

.dashboard-wrapper {
  background: #f4f6f9;
  min-height: 100vh;
  font-family:
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Arial,
    sans-serif;
  color: #333;
}

.dashboard-container {
  max-width: 1300px;
  margin: auto;
  padding: 30px 20px;
}

.page-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.page-title {
  margin: 0;
  font-size: 1.8rem;
  color: #0f172a;
}

.grid-layout {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 25px;
  align-items: start;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 25px;
  border: 1px solid #e2e8f0;
  box-shadow:
    0 4px 6px -1px rgba(0,0,0,.05);
}

.card h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #1e293b;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 700;
  font-size: .82rem;
  color: #64748b;
  text-transform: uppercase;
}

.custom-file-upload {
  display: block;
  border: 2px dashed #cbd5e1;
  padding: 18px;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  background: #f8fafc;
}

.custom-file-upload input {
  display: none;
}

.custom-select,
.threshold-input {
  width: 100%;
  padding: 11px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
}

.upload-note {
  color: #64748b;
  font-size: .9rem;
}

.btn {
  padding: 11px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.btn-download {
  background: #10b981;
  color: white;
}

.title-download-btn {
  width: auto;
}

.metrics-kpi-grid {
  display: grid;
  grid-template-columns:
    repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}

.kpi-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  border-left: 5px solid;
  border-top: 1px solid #e2e8f0;
  border-right: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

.kpi-title {
  display: block;
  font-size: .8rem;
  font-weight: 700;
  color: #64748b;
}

.kpi-value {
  display: block;
  font-size: 1.9rem;
  font-weight: 800;
  margin-top: 5px;
}

.accent-blue {
  border-left-color: #3b82f6;
}

.accent-green {
  border-left-color: #10b981;
}

.accent-orange {
  border-left-color: #f59e0b;
}

.accent-purple {
  border-left-color: #8b5cf6;
}

.summary-stat-row {
  display: flex;
  gap: 10px;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
}

.stat-label {
  display: block;
  font-size: .75rem;
  color: #64748b;
}

.stat-val {
  font-weight: 700;
  color: #0f172a;
}

.lookup-row {
  display: flex;
  gap: 10px;
}

.lookup-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
}

.lookup-button {
  background: #64748b;
  color: white;
}

.lookup-result {
  margin-top: 15px;
  padding: 18px;
  background: #f8fafc;
  border-radius: 10px;
}

.lookup-field {
  margin-bottom: 10px;
}

.table-container {
  overflow-x: auto;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.modern-table th {
  background: #f8fafc;
  color: #64748b;
  padding: 12px;
  text-align: left;
}

.modern-table td {
  padding: 14px 12px;
  border-bottom: 1px solid #f1f5f9;
}

.highlight-row {
  background: #f0fdf4;
}

.risk-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 20px;
}

.risk-description {
  color: #64748b;
  margin-top: -10px;
}

.risk-model {
  padding: 10px 15px;
  background: #eff6ff;
  border-radius: 8px;
  color: #1d4ed8;
}

.risk-stat-grid {
  display: grid;
  grid-template-columns:
    repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.risk-stat {
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
  text-align: center;
}

.risk-stat span {
  display: block;
  color: #64748b;
  font-size: .8rem;
}

.risk-stat strong {
  display: block;
  font-size: 1.5rem;
  margin-top: 5px;
}

.danger-text {
  color: #dc2626;
}

.risk-reasons {
  margin: 0;
  padding-left: 18px;
}

.no-risk-message {
  padding: 25px;
  text-align: center;
  color: #16a34a;
  background: #f0fdf4;
  border-radius: 8px;
  font-weight: 600;
}

.feature-list {
  display: grid;
  gap: 12px;
}

.feature-meta {
  display: flex;
  justify-content: space-between;
}

.feature-bar {
  height: 10px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
}

.feature-fill {
  height: 100%;
  background: #3b82f6;
}

.feature-unavailable {
  color: #64748b;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 3.5rem;
}

@media (max-width: 900px) {

  .grid-layout {
    grid-template-columns: 1fr;
  }

  .metrics-kpi-grid {
    grid-template-columns:
      repeat(2, 1fr);
  }

  .risk-stat-grid {
    grid-template-columns:
      repeat(2, 1fr);
  }

}

</style>