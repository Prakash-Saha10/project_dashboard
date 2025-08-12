document.addEventListener('DOMContentLoaded', function() {
    // Project progress chart
    const projectProgressCtx = document.getElementById('projectProgressChart');
    if (projectProgressCtx) {
        const projectId = projectProgressCtx.dataset.projectId;
        fetch(`/api/project/${projectId}/progress/`)
            .then(response => response.json())
            .then(data => {
                new Chart(projectProgressCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Completed', 'Remaining'],
                        datasets: [{
                            data: [data.completed_tasks, data.total_tasks - data.completed_tasks],
                            backgroundColor: ['#4e73df', '#e74a3b'],
                            hoverBackgroundColor: ['#2e59d9', '#be2617'],
                            hoverBorderColor: "rgba(234, 236, 244, 1)",
                        }]
                    },
                    options: {
                        maintainAspectRatio: false,
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `${context.label}: ${context.raw} tasks`;
                                    }
                                }
                            },
                            legend: {
                                position: 'bottom'
                            }
                        },
                        cutout: '80%'
                    }
                });
            });
    }

    // User progress chart
    const userProgressCtx = document.getElementById('userProgressChart');
    if (userProgressCtx) {
        const userId = userProgressCtx.dataset.userId;
        fetch(`/api/user/${userId}/progress/`)
            .then(response => response.json())
            .then(data => {
                const statusData = {};
                data.status_distribution.forEach(item => {
                    statusData[item.status] = item.count;
                });

                new Chart(userProgressCtx, {
                    type: 'bar',
                    data: {
                        labels: ['Not Started', 'In Progress', 'Blocked', 'Completed'],
                        datasets: [{
                            label: 'Tasks',
                            data: [
                                statusData['NOT_STARTED'] || 0,
                                statusData['IN_PROGRESS'] || 0,
                                statusData['BLOCKED'] || 0,
                                statusData['COMPLETED'] || 0
                            ],
                            backgroundColor: [
                                '#858796',
                                '#f6c23e',
                                '#e74a3b',
                                '#1cc88a'
                            ],
                            hoverBackgroundColor: [
                                '#6a6c7e',
                                '#dda20a',
                                '#be2617',
                                '#17a673'
                            ],
                            borderColor: "rgba(234, 236, 244, 1)",
                        }]
                    },
                    options: {
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `${context.raw} tasks`;
                                    }
                                }
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
            });
    }
});