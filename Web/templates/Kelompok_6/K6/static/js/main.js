document.addEventListener('DOMContentLoaded', () => {
    
    
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            document.getElementById(targetId).classList.add('active');
        });
    });

    
    const sentimentForm = document.getElementById('sentiment-form');
    const sentimentResult = document.getElementById('sentiment-result');
    const btnAnalyze = document.getElementById('btn-analyze');

    if (sentimentForm) {
        sentimentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('sentiment-text').value;
            
            const originalBtnHtml = btnAnalyze.innerHTML;
            btnAnalyze.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Menganalisis...';
            btnAnalyze.disabled = true;
            sentimentResult.classList.add('hidden');

            try {
                const response = await fetch('/api/sentiment', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });

                if (!response.ok) throw new Error('API Error');
                
                const data = await response.json();
                
                let badgeClass = 'badge-indigo';
                let iconHtml = '<i class="ph ph-question"></i>';
                
                
                let labelText = data.label;
                if (labelText === 'LABEL_2' || labelText === 'LABEL_1' || labelText.toLowerCase().includes('posit')) {
                    badgeClass = 'success';
                    labelText = 'Positif';
                    iconHtml = '<i class="ph ph-thumbs-up"></i>';
                } else if (labelText === 'LABEL_0' || labelText.toLowerCase().includes('negat')) {
                    badgeClass = 'error';
                    labelText = 'Negatif';
                    iconHtml = '<i class="ph ph-thumbs-down"></i>';
                } else {
                    
                    badgeClass = 'error';
                    labelText = 'Negatif';
                    iconHtml = '<i class="ph ph-thumbs-down"></i>';
                }

                sentimentResult.innerHTML = `
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <div class="result-title">Hasil Prediksi Sentimen</div>
                            <span class="badge ${badgeClass}">${iconHtml} ${labelText}</span>
                        </div>
                        <div style="text-align: right;">
                            <div class="result-title">Akurasi / Confidence</div>
                            <span class="result-value">${(data.score * 100).toFixed(2)}%</span>
                        </div>
                    </div>
                `;
                sentimentResult.classList.remove('hidden');
                
                
                if (typeof fetchSentimentTrends === 'function') {
                    fetchSentimentTrends();
                }
            } catch (error) {
                sentimentResult.innerHTML = `<div class="result-title" style="color: var(--error);">Error</div><div class="result-value">Gagal menghubungi server atau model belum siap.</div>`;
                sentimentResult.classList.remove('hidden');
            } finally {
                btnAnalyze.innerHTML = originalBtnHtml;
                btnAnalyze.disabled = false;
            }
        });
    }

    
    const scrapeForm = document.getElementById('scrape-form');
    const scrapeResult = document.getElementById('scrape-result');
    const scrapeLoading = document.getElementById('scrape-loading');
    const btnScrape = document.getElementById('btn-scrape');
    
    let sentimentChart = null; 

    if (scrapeForm) {
        scrapeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = document.getElementById('youtube-url').value;
            const maxComments = parseInt(document.getElementById('max-comments').value) || 50;
            
            const originalBtnHtml = btnScrape.innerHTML;
            btnScrape.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Menarik...';
            btnScrape.disabled = true;
            scrapeResult.classList.add('hidden');
            scrapeLoading.classList.remove('hidden');

            try {
                const response = await fetch('/api/scrape', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url, max_comments: maxComments })
                });

                if (!response.ok) throw new Error('API Error');
                
                const data = await response.json();
                
                
                document.getElementById('stat-total').textContent = data.total_comments;
                document.getElementById('stat-pos').textContent = data.positive;
                document.getElementById('stat-neg').textContent = data.negative;

                
                const ctx = document.getElementById('sentimentChart').getContext('2d');
                if (sentimentChart) sentimentChart.destroy();
                
                sentimentChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Positif', 'Negatif'],
                        datasets: [{
                            data: [data.positive, data.negative],
                            backgroundColor: ['#059669', '#DC2626'],
                            borderWidth: 0,
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '75%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    font: { family: "'Inter', sans-serif" },
                                    usePointStyle: true,
                                    padding: 20
                                }
                            }
                        }
                    }
                });

                
                const tbody = document.getElementById('comments-tbody');
                tbody.innerHTML = '';
                
                data.comments.forEach((comment, index) => {
                    const tr = document.createElement('tr');
                    
                    tr.style.animation = `fadeIn 300ms ease forwards ${index * 30}ms`;
                    tr.style.opacity = '0';
                    
                    let badgeClass = 'badge-indigo';
                    let iconHtml = '<i class="ph ph-question"></i>';
                    
                    if (comment.label === 'Positif') {
                        badgeClass = 'success';
                        iconHtml = '<i class="ph ph-thumbs-up"></i>';
                    } else if (comment.label === 'Negatif') {
                        badgeClass = 'error';
                        iconHtml = '<i class="ph ph-thumbs-down"></i>';
                    }

                    tr.innerHTML = `
                        <td>${comment.text}</td>
                        <td><span class="badge ${badgeClass}">${iconHtml} ${comment.label}</span></td>
                        <td>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <div style="flex-grow: 1; height: 4px; background: #E5E7EB; border-radius: 2px; overflow: hidden;">
                                    <div style="height: 100%; width: ${comment.score * 100}%; background: var(--primary);"></div>
                                </div>
                                <span style="font-size: 12px; color: var(--text-secondary);">${(comment.score * 100).toFixed(0)}%</span>
                            </div>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });

                scrapeLoading.classList.add('hidden');
                scrapeResult.classList.remove('hidden');
            } catch (error) {
                scrapeLoading.classList.add('hidden');
                alert("Gagal melakukan scraping. Pastikan URL valid dan komentar tidak dinonaktifkan.");
            } finally {
                btnScrape.innerHTML = originalBtnHtml;
                btnScrape.disabled = false;
            }
        });
    }

    
    let dbSentimentChartInstance = null;
    
    async function fetchSentimentTrends() {
        try {
            const response = await fetch('/api/sentiment-trends');
            if (!response.ok) throw new Error('API Error');
            const data = await response.json();
            
            const labels = data.map(item => item.month);
            const positiveData = data.map(item => item.positive);
            const negativeData = data.map(item => item.negative);
            
            const ctx = document.getElementById('dbSentimentChart');
            if (!ctx) return;
            
            if (dbSentimentChartInstance) {
                dbSentimentChartInstance.destroy();
            }
            
            dbSentimentChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Sentimen Positif',
                            data: positiveData,
                            borderColor: '#059669',
                            backgroundColor: 'rgba(5, 150, 105, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Sentimen Negatif',
                            data: negativeData,
                            borderColor: '#DC2626',
                            backgroundColor: 'rgba(220, 38, 38, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                font: { family: "'Inter', sans-serif" },
                                usePointStyle: true,
                                padding: 20
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0 }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Failed to load sentiment trends:', error);
        }
    }
    
    
    fetchSentimentTrends();

    
    let lstmForecastChartInstance = null;
    
    async function fetchAndRenderForecast() {
        try {
            const response = await fetch('/api/forecast');
            if (!response.ok) throw new Error('API Error fetching forecast');
            const data = await response.json();
            
            const history = data.history;
            const forecast = data.forecast;
            
            
            const labels = [...history.map(item => item.date), ...forecast.map(item => item.date)];
            
            
            const historyData = [...history.map(item => item.value), ...Array(forecast.length).fill(null)];
            
            
            const forecastData = Array(labels.length).fill(null);
            
            
            if (history.length > 0) {
                forecastData[history.length - 1] = history[history.length - 1].value;
            }
            
            
            for (let i = 0; i < forecast.length; i++) {
                forecastData[history.length + i] = forecast[i].value;
            }
            
            const ctx = document.getElementById('lstmForecastChart');
            if (!ctx) return;
            
            if (lstmForecastChartInstance) {
                lstmForecastChartInstance.destroy();
            }
            
            lstmForecastChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Historis (Aktual Smooth)',
                            data: historyData,
                            borderColor: '#3B82F6', 
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Prediksi (30 Hari ke Depan)',
                            data: forecastData,
                            borderColor: '#EF4444', 
                            borderWidth: 2,
                            borderDash: [5, 5], 
                            fill: false,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                font: { family: "'Inter', sans-serif" },
                                usePointStyle: true,
                                padding: 20
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': ' + (context.raw * 100).toFixed(2) + '% Positif';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1, 
                            ticks: {
                                callback: function(value) {
                                    return (value * 100) + '%';
                                }
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Failed to load LSTM forecast:', error);
        }
    }

    
    fetchAndRenderForecast();

});
