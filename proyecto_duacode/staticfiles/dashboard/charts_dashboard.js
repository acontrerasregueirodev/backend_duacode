

// Chart 1: Eventos por Sede
const renderChartSedes = (dias, reunionesPorSede) => {
    const sedes = Object.keys(reunionesPorSede);
    const colores = [
        "rgba(75, 192, 192, 1)", 
        "rgba(255, 99, 132, 1)", 
        "rgba(54, 162, 235, 1)", 
    ];

    const datasets = sedes.slice(0, 3).map((sede, index) => {
        return {
            label: `E - ${sede}`,
            data: Object.values(reunionesPorSede[sede]),
            borderColor: colores[index],
            borderWidth: 2,
            fill: false,
        };
    });

    const ctx1 = document.getElementById('grafico-sedes').getContext("2d");
    new Chart(ctx1, {
        type: "line",
        data: {
            labels: dias,
            datasets: datasets,
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
};
// Chart 2: Total de empleados por proyecto
const renderChartEmpleadosProyecto = (proyectos, empleadosPorProyectoData) => {
    console.log("cargando renderChartEmpleadosProyecto")
    const ctx2 = document.getElementById('grafico-empleados-proyecto').getContext("2d");
    new Chart(ctx2, {
        type: "bar",
        data: {
            labels: proyectos,
            datasets: [{
                label: 'Total de Empleados',
                data: empleadosPorProyectoData,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            }
        }
    });
};
