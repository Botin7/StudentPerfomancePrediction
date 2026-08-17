import axios from "axios";

const API = "http://127.0.0.1:8000";

export const uploadCSV = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  return await axios.post(`${API}/upload`, formData);
};

export const runPrediction = async (algorithm: string) => {
  return await axios.post(`${API}/predict`, null, {
    params: {
      model_name: algorithm
    }
  });
};

export const getSummary = async () => {
  return await axios.get(`${API}/summary`);
};

export const getMetrics = async (algorithm: string) => {
  return await axios.get(`${API}/metrics`, {
    params: {
      algorithm
    }
  });
};

export const getComparison = async () => {
  return await axios.get(`${API}/compare`);
};

export const getCharts = async (algorithm: string = "random_forest") => {
  return await axios.get(`${API}/charts`, {
    params: {
      algorithm
    }
  });
};

export const getAtRiskStudents = async (
  algorithm: string = "random_forest",
  threshold: number = 50
) => {
  return await axios.get(`${API}/at_risk`, {
    params: {
      algorithm,
      threshold
    }
  });
};

export const getStudent = async (
  studentId: string,
  algorithm = "random_forest"
) => {
  return await axios.get(`${API}/student`, {
    params: {
      student_id: studentId,
      algorithm
    }
  });
};

export const getFeatureImportance = async (
  algorithm = "random_forest"
) => {
  return await axios.get(`${API}/feature_importance`, {
    params: {
      algorithm
    }
  });
};

export const downloadCSV = async () => {
  return await axios.get(`${API}/download`, {
    responseType: "blob"
  });
};

export const downloadTemplate = async () => {
  return await axios.get(`${API}/template`, {
    responseType: "blob"
  });
};