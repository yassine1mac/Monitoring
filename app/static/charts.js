document.addEventListener("DOMContentLoaded", () => {
    const fetchData = async () => {
        const response = await fetch('/metrics');
        const data = await response.json();
        return data;
    };

    const createChart = (ctx, label, data, color) => {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.timestamps,
                datasets: [{
                    label: label,
                    data: data.values,
                    borderColor: color,
                    borderWidth: 2,
                    fill: false,
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'Time' } },
                    y: { title: { display: true, text: label } }
                }
            }
        });
    };

    fetchData().then(data => {
        createChart(document.getElementById('cpuChart').getContext('2d'), 'CPU Usage (%)', data.cpu, 'red');
        createChart(document.getElementById('memoryChart').getContext('2d'), 'Memory Usage (%)', data.memory, 'blue');
        createChart(document.getElementById('diskChart').getContext('2d'), 'Disk Usage (%)', data.disk, 'green');
        createChart(document.getElementById('networkChart').getContext('2d'), 'Network Usage (bytes)', data.network, 'purple');
    });
});

