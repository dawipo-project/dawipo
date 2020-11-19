google.charts.load("current", { packages: ["corechart", "bar"] });
google.charts.setOnLoadCallback(drawStacked);

function drawStacked() {
  var data = google.visualization.arrayToDataTable([
    ["Problema", "Frecuencia", "Intensidad", "Prioridad"],
    ["Costos Ocultos", 2, 3, 5],
    ["Información fragmentada", 3, 2, 5],
    ["Tiempos de abastecimiento", 2, 3, 5],
    ["Tiempos de reacción lentos", 2, 3, 5],
    ["Dependen de data externa", 5, 0, 5],
    ["Consultan muchos archivos", 4, 4, 8],
    ["Poco acceso a inventario", 4, 4, 8],
    ["Concentración en otras áreas", 5, 5, 10],
    ["Muchos procesos manuales", 5, 5, 10],
  ]);

  var options = {
    title: "Principales dolores identificados por los entrevistados",
    chartArea: { width: "50%" },
    isStacked: true,
    colors: ['#fb9334', '#ebd9c8', '#007a7a'],
    fontName: "Lato",
    hAxis: {
      title: "",
      minValue: 0,
    },
    vAxis: {
      title: "",
    },
  };
  var chart = new google.visualization.BarChart(
    document.getElementById("chart_div")
  );
  chart.draw(data, options);
}

google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ["Día", "Transacciones"],
    ["Ago. 27", 349009],
    ["Ago. 28", 289608],
    ["Ago. 29", 265680],
    ["Ago. 30", 298800],
    ["Ago. 31", 371691],
    ["Sep. 1", 312045],
    ["Sep. 2", 305389],
    ["Sep. 3", 292923],
    ["Sep. 4", 321132],
    ["Sep. 5", 258797],
    ["Sep. 6", 323182],
    ["Sep. 7", 328306],
    ["Sep. 8", 310690],
    ["Sep. 9", 341825],
    ["Sep. 10", 304149],
    ["Sep. 11", 296767],
    ["Sep. 12", 251774],
    ["Sep. 13", 349764],
    ["Sep. 14", 328814],
    ["Sep. 15", 338696],
    ["Sep. 16", 344820],
    ["Sep. 17", 321101],
    ["Sep. 18", 293197],
    ["Sep. 19", 255602],
    ["Sep. 20", 293648],
    ["Sep. 21", 309101],
    ["Sep. 22", 335970],
    ["Sep. 23", 312797],
    ["Sep. 24", 349404],
    ["Sep. 25", 273219],
  ]);

  var options = {
    fontName: "Lato",
    title:
      "Cantidad de transacciones por día en la blockchain de Bitcoin durante los últimos 30 días",
    curveType: "function",
    legend: { position: "bottom" },
    hAxis: {
      textPosition: "none",
    },
    height: 350,
  };

  var chart = new google.visualization.LineChart(
    document.getElementById("bc_chart_div")
  );

  chart.draw(data, options);
}


