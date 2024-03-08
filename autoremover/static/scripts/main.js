var themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon");
var themeToggleLightIcon = document.getElementById("theme-toggle-light-icon");

// Change the icons inside the button based on previous settings
if (
  localStorage.getItem("color-theme") === "dark" ||
  (!("color-theme" in localStorage) &&
    window.matchMedia("(prefers-color-scheme: dark)").matches)
) {
  themeToggleLightIcon.classList.remove("hidden");
} else {
  themeToggleDarkIcon.classList.remove("hidden");
}
function toggleTheme(event) {
  // toggle icons inside button
  themeToggleDarkIcon.classList.toggle("hidden");
  themeToggleLightIcon.classList.toggle("hidden");

  // if set via local storage previously
  if (localStorage.getItem("color-theme")) {
    if (localStorage.getItem("color-theme") === "light") {
      document.documentElement.classList.add("dark");
      localStorage.setItem("color-theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("color-theme", "light");
    }

    // if NOT set via local storage previously
  } else {
    if (document.documentElement.classList.contains("dark")) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("color-theme", "light");
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("color-theme", "dark");
    }
  }
}

var themeToggleBtn = document.getElementById("theme-toggle");
var themeToggleBtn2 = document.getElementById("theme-toggle-2");

themeToggleBtn.addEventListener("click", toggleTheme);
themeToggleBtn2.addEventListener("click", toggleTheme);

const options = {
  colors: ["#3699FF"],
  series: [
    {
      name: "Files",
      color: "#3699FF",
      data: [
        { x: "Jan", y: 231 },
        { x: "Feb", y: 122 },
        { x: "Mar", y: 63 },
        { x: "Apr", y: 421 },
        { x: "May", y: 122 },
        { x: "Jun", y: 323 },
        { x: "Jul", y: 2 },
        { x: "Aug", y: 0 },
        { x: "Sep", y: 421 },
        { x: "Oct", y: 122 },
        { x: "Nov", y: 323 },
        { x: "Dec", y: 111 },
      ],
    },
  ],
  chart: {
    type: "bar",
    height: "160px",
    fontFamily: "Inter, sans-serif",
    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "70%",
      borderRadiusApplication: "end",
      borderRadius: 8,
    },
  },
  tooltip: {
    shared: true,
    intersect: false,
    style: {
      fontFamily: "Inter, sans-serif",
    },
  },
  states: {
    hover: {
      filter: {
        type: "darken",
        value: 1,
      },
    },
  },
  stroke: {
    show: true,
    width: 0,
    colors: ["transparent"],
  },
  grid: {
    show: false,
    strokeDashArray: 4,
    padding: {
      left: 2,
      right: 2,
      top: -14,
    },
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false,
  },
  xaxis: {
    floating: false,
    labels: {
      show: false,
      style: {
        fontFamily: "Inter, sans-serif",
        cssClass: "text-xs font-normal fill-white dark:fill-white",
      },
    },
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
  },
  yaxis: {
    show: false,
  },
  fill: {
    opacity: 1,
  },
};

if (
  document.getElementById("column-chart") &&
  typeof ApexCharts !== "undefined"
) {
  const chart = new ApexCharts(
    document.getElementById("column-chart"),
    options
  );
  chart.render();
}
