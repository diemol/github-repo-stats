const dailyChart = bb.generate({
  data: {
    x: "x",
    columns: window.dailyData,
    type: "line", // for ESM specify as: line()
  },
  subchart: {
    show: true
  },
  axis: {
    x: {
      type: "timeseries",
      tick: {
        format: "%Y-%m-%d"
      }
    }
  },
  bindto: "#dailyData"
});

const lastThirtyDaysChart = bb.generate({
  data: {
    x: "x",
    columns: window.lastThirtyDays,
    type: "line", // for ESM specify as: line()
  },
  axis: {
    x: {
      type: "timeseries",
      tick: {
        format: "%Y-%m-%d"
      }
    }
  },
  bindto: "#lastThirtyDays"
});

const monthlyChart = bb.generate({
  data: {
    x: "x",
    columns: window.monthlyData,
    type: "line", // for ESM specify as: line()
  },
  subchart: {
    show: true
  },
  axis: {
    x: {
      type: "timeseries",
      tick: {
        format: "%Y-%m-%d"
      }
    }
  },
  bindto: "#monthlyData"
});

const yearlyChart = bb.generate({
  data: {
    x: "x",
    columns: window.yearlyData,
    type: "line", // for ESM specify as: line()
  },
  axis: {
    x: {
      type: "timeseries",
      tick: {
        format: "%Y-%m-%d"
      }
    }
  },
  bindto: "#yearlyData"
});

const lastUpdate = document.getElementById("lastUpdate") ;
lastUpdate.innerHTML = "Last update: " + window.lastUpdate;