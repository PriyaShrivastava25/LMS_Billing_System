
const months = JSON.parse('{{ months|escapejs }}');
const revenue = JSON.parse('{{ revenue|escapejs }}');

new Chart(document.getElementById('revenueChart'), {
    type: 'bar',
    data: {
        labels: months,
        datasets: [{
            label: 'Revenue',
            data: revenue,
            backgroundColor: '#38bdf8'
        }]
    },
    options: {
        animation: { duration: 1500 },
        plugins: {
            legend: { labels: { color: '#e2e8f0' } }
        },
        scales: {
            x: { ticks: { color: '#e2e8f0' } },
            y: { ticks: { color: '#e2e8f0' } }
        }
    }
});

const courseLabels = JSON.parse('{{ course_labels|escapejs }}');
const courseCounts = JSON.parse('{{ course_counts|escapejs }}');

new Chart(document.getElementById('courseChart'), {
    type: 'doughnut',
    data: {
        labels: courseLabels,
        datasets: [{
            data: courseCounts,
            backgroundColor: [
                '#38bdf8',
                '#4ade80',
                '#facc15',
                '#fb7185',
                '#a78bfa'
            ]
        }]
    },
    options: {
        animation: { duration: 1500 }
    }
});

const catLabels = JSON.parse('{{ category_labels|escapejs }}');
const catRevenue = JSON.parse('{{ category_revenue|escapejs }}');

new Chart(document.getElementById('categoryChart'), {
    type: 'bar',
    data: {
        labels: catLabels,
        datasets: [{
            label: 'Revenue',
            data: catRevenue,
            backgroundColor: '#6366f1'
        }]
    },
    options: {
        animation: { duration: 1500 }
    }
});


const topCourseLabels = JSON.parse('{{ top_course_labels|escapejs }}');
const topCourseData = JSON.parse('{{ top_course_data|escapejs }}');

if (topCourseLabels.length > 0) {
    new Chart(document.getElementById('topCoursesChart'), {
        type: 'bar',
        data: {
            labels: topCourseLabels,
            datasets: [{
                label: 'Enrollments',
                data: topCourseData,
                backgroundColor: '#4ade80'
            }]
        },
        options: {
            animation: { duration: 1500 },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

