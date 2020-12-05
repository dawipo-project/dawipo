$(window).load(function(){
    $('#messageModal').modal('show');
});

var colors = ["#fb9334", "#fe6625", "#007a7a", "#003f5a"],
    dataColors = $("#campaign-sent-chart").data("colors");
dataColors && (colors = dataColors.split(","));
var options1 = {
    chart: { type: "bar", height: 60, sparkline: { enabled: !0 } },
    plotOptions: { bar: { columnWidth: "60%" } },
    colors: colors,
    series: [{ data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54] }],
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    xaxis: { crosshairs: { width: 1 } },
    tooltip: {
        fixed: { enabled: !1 },
        x: { show: !1 },
        y: {
            title: {
                formatter: function (o) {
                    return "";
                },
            },
        },
        marker: { show: !1 },
    },
};
new ApexCharts(document.querySelector("#campaign-sent-chart"), options1).render();
colors = ["#fb9334"];
var options_mes = {
    series: [{
        name: 'Pedidos',
        data: [10, 41, 35, 51, 49, 52, 69, 91, 148]
    }],
    colors: colors,
    chart: {
        height: 350,
        type: 'line',
        zoom: {
            enabled: false
        },
        toolbar: {
            show: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    grid: {
        row: {
            colors: ['#f3f3f3', 'transparent'],
            opacity: 0.5
        },
    },
    xaxis: {
        categories: ['Ene', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Ago', 'Sep']
    }
};
new ApexCharts(document.querySelector("#pedidos_mes"), options_mes).render();
colors = ["#003f5a"];
var options_clientes_mes = {
    series: [{
        name: 'Clientes',
        data: [4, 18, 3, 5, 9, 6, 13, 2, 15]
    }],
    colors: colors,
    chart: {
        height: 350,
        type: 'line',
        zoom: {
            enabled: false
        },
        toolbar: {
            show: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    grid: {
        row: {
            colors: ['#f3f3f3', 'transparent'],
            opacity: 0.5
        },
    },
    xaxis: {
        categories: ['Ene', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Ago', 'Sep']
    }
};
new ApexCharts(document.querySelector("#clientes_mes"), options_clientes_mes).render();
colors = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"];
(dataColors = $("#new-leads-chart").data("colors")) && (colors = dataColors.split(","));
var options2 = {
    chart: { type: "line", height: 60, sparkline: { enabled: !0 } },
    series: [{ data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54] }],
    stroke: { width: 2, curve: "smooth" },
    markers: { size: 0 },
    colors: colors,
    tooltip: {
        fixed: { enabled: !1 },
        x: { show: !1 },
        y: {
            title: {
                formatter: function (o) {
                    return "";
                },
            },
        },
        marker: { show: !1 },
    },
};
new ApexCharts(document.querySelector("#new-leads-chart"), options2).render();
colors = ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"];
(dataColors = $("#deals-chart").data("colors")) && (colors = dataColors.split(","));
var options3 = {
    chart: { type: "bar", height: 60, sparkline: { enabled: !0 } },
    plotOptions: { bar: { columnWidth: "60%" } },
    colors: colors,
    series: [{ data: [12, 14, 2, 47, 42, 15, 47, 75, 65, 19, 14] }],
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    xaxis: { crosshairs: { width: 1 } },
    tooltip: {
        fixed: { enabled: !1 },
        x: { show: !1 },
        y: {
            title: {
                formatter: function (o) {
                    return "";
                },
            },
        },
        marker: { show: !1 },
    },
};
new ApexCharts(document.querySelector("#deals-chart"), options3).render();
colors = ["#fb9334", "#fe6625", "#003f5a", "#007a7a"];
(dataColors = $("#booked-revenue-chart").data("colors")) && (colors = dataColors.split(","));
var options4 = {
    chart: { type: "bar", height: 60, sparkline: { enabled: !0 } },
    plotOptions: { bar: { columnWidth: "60%" } },
    colors: colors,
    series: [{ data: [47, 45, 74, 14, 56, 74, 14, 11, 7, 39, 82] }],
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    xaxis: { crosshairs: { width: 1 } },
    tooltip: {
        fixed: { enabled: !1 },
        x: { show: !1 },
        y: {
            title: {
                formatter: function (o) {
                    return "";
                },
            },
        },
        marker: { show: !1 },
    },
};
new ApexCharts(document.querySelector("#booked-revenue-chart"), options4).render();
colors = ["#fb9334", "#fe6625", "#003f5a", "#007a7a"];
(dataColors = $("#dash-campaigns-chart").data("colors")) && (colors = dataColors.split(","));
var options = { 
    chart: { 
        height: 358, 
        type: "radialBar" 
    }, 
    colors: colors, 
    series: [86, 36, 50], 
    labels: ["Total", "Ecommerce", "Puntos de venta"], 
    plotOptions: { 
        radialBar: { 
            track: { 
                margin: 8 
            } 
        } 
    } 
}, chart = new ApexCharts(document.querySelector("#dash-campaigns-chart"), options);
chart.render();
colors = ["#fb9334", "#fe6625", "#007a7a", "#003f5a"];
(dataColors = $("#dash-revenue-chart").data("colors")) && (colors = dataColors.split(","));
options = {
    chart: { height: 321, type: "line", toolbar: { show: !1 } },
    stroke: { curve: "smooth", width: 2 },
    series: [
        { name: "Ganancias proyectadas", type: "area", data: [44, 55, 31, 47, 31, 43, 26, 41, 31, 47, 33, 43] },
        { name: "Ganancias reales", type: "line", data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43, 56] },
    ],
    fill: { type: "solid", opacity: [0.35, 1] },
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    markers: { size: 0 },
    colors: colors,
    yaxis: [{ title: { text: "Ganancias (USD)" }, min: 0 }],
    tooltip: {
        shared: !0,
        intersect: !1,
        y: {
            formatter: function (o) {
                return void 0 !== o ? o.toFixed(0) + "k" : o;
            },
        },
    },
    grid: { borderColor: "#f1f3fa", padding: { bottom: 5 } },
    legend: { fontSize: "14px", fontFamily: "14px", offsetY: 5 },
    responsive: [{ breakpoint: 600, options: { yaxis: { show: !1 }, legend: { show: !1 } } }],
};
(chart = new ApexCharts(document.querySelector("#dash-revenue-chart"), options)).render();
!(function (o) {
    "use strict";
    function e() {
        (this.$body = o("body")), (this.charts = []);
    }
    (e.prototype.initCharts = function () {
        window.Apex = { chart: { parentHeightOffset: 0, toolbar: { show: !1 } }, grid: { padding: { left: 0, right: 0 } }, colors: ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"] };
        
        e = ["#727cf5", "#e3eaef"];
        (t = o("#high-performing-product").data("colors")) && (e = t.split(","));
        r = {
            chart: { height: 257, type: "bar", stacked: !0 },
            plotOptions: { bar: { horizontal: !1, columnWidth: "20%" } },
            dataLabels: { enabled: !1 },
            stroke: { show: !0, width: 2, colors: ["transparent"] },
            series: [
                { name: "Actual", data: [65, 59, 80, 81, 56, 89, 40, 32, 65, 59, 80, 81] },
                { name: "Projection", data: [89, 40, 32, 65, 59, 80, 81, 56, 89, 40, 65, 59] },
            ],
            zoom: { enabled: !1 },
            legend: { show: !1 },
            colors: e,
            xaxis: { categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], axisBorder: { show: !1 } },
            yaxis: {
                labels: {
                    formatter: function (e) {
                        return e + "k";
                    },
                    offsetX: -15,
                },
            },
            fill: { opacity: 1 },
            tooltip: {
                y: {
                    formatter: function (e) {
                        return "$" + e + "k";
                    },
                },
            },
        };
        new ApexCharts(document.querySelector("#high-performing-product"), r).render();
    }),
        (e.prototype.initMaps = function () {
            0 < o("#world-map-markers").length &&
                o("#world-map-markers").vectorMap({
                    map: "world_mill_en",
                    normalizeFunction: "polynomial",
                    hoverOpacity: 0.7,
                    hoverColor: !1,
                    regionStyle: { initial: { fill: "#fb9334" } },
                    markerStyle: { initial: { r: 9, fill: "#007a7a", "fill-opacity": 0.9, stroke: "#fff", "stroke-width": 7, "stroke-opacity": 0.4 }, hover: { stroke: "#fff", "fill-opacity": 1, "stroke-width": 1.5 } },
                    backgroundColor: "transparent",
                    markers: [
                        { latLng: [40.71, -74], name: "New York" },
                        { latLng: [37.77, -122.41], name: "San Francisco" },
                        { latLng: [-33.86, 151.2], name: "Sydney" },
                        { latLng: [1.3, 103.8], name: "Singapore" },
                    ],
                    zoomOnScroll: !1,
                });
        }),
        (e.prototype.init = function () {
            o("#dash-daterange").daterangepicker({ singleDatePicker: !0 }), this.initCharts(), this.initMaps();
        }),
        (o.Dashboard = new e()),
        (o.Dashboard.Constructor = e);
})(window.jQuery),
    (function (t) {
        "use strict";
        t(document).ready(function (e) {
            t.Dashboard.init();
        });
    })(window.jQuery);
