import os
import json
from flask import Flask, render_template, jsonify, request, redirect, url_for

# Initialize Flask with the template folder set to the current directory (Web/)
app = Flask(__name__, template_folder='.', static_folder='static')

SESSIONS_FILE = os.path.join(os.path.dirname(__file__), 'sessions.json')

def read_sessions():
    """Read sessions history from JSON file."""
    if not os.path.exists(SESSIONS_FILE):
        return {}
    try:
        with open(SESSIONS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def write_sessions(data):
    """Write sessions history to JSON file."""
    try:
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error writing sessions: {e}")

# Helper definition to map Kelompok numbers to their title description (from PDF)
KELOMPOK_METADATA = {
    1: {"title": "Analisis Kandungan Gizi Makanan", "algo": "CNN", "phase": "Fase 3: Perakitan & Keamanan Pangan"},
    2: {"title": "Rekomendasi Menu Makanan", "algo": "LSTM", "phase": "Fase 1: Perencanaan Menu & Logistik"},
    3: {"title": "Prediksi Kesukaan Menu MBG", "algo": "DNN/LSTM Tabular", "phase": "Fase 1: Perencanaan Menu & Logistik"},
    4: {"title": "Analisis Sentimen Medsos", "algo": "CNN-LSTM & Word Embedding", "phase": "Fase 5: Pemantauan Opini Publik"},
    5: {"title": "Deteksi Kontaminasi Benda Asing Makro", "algo": "YOLO", "phase": "Fase 3: Perakitan & Keamanan Pangan"},
    6: {"title": "Analisis Sentimen Komentar YouTube", "algo": "LSTM & Time Series", "phase": "Fase 5: Pemantauan Opini Publik"},
    7: {"title": "Deteksi Sisa Makanan Piring Kotor", "algo": "CNN Transfer Learning", "phase": "Fase 4: Evaluasi Pasca-Konsumsi"},
    8: {"title": "Deteksi Kelengkapan Menu Tray", "algo": "YOLOv8 Instance Segmentation", "phase": "Fase 3: Perakitan & Keamanan Pangan"},
    9: {"title": "Prediksi Kebutuhan Distribusi", "algo": "ANN", "phase": "Fase 1: Perencanaan Menu & Logistik"},
    10: {"title": "Klasifikasi Kelayakan Gizi & Benda Asing Mikro", "algo": "ERX Hiperspektral", "phase": "Fase 3: Perakitan & Keamanan Pangan"},
    11: {"title": "Sortir Kualitas Kesegaran Bahan Baku", "algo": "CNN MobileNetV2", "phase": "Fase 2: Pemeriksaan Kualitas Bahan Baku"}
}

# Rich simulated operational results for each Kelompok based on PDF tasks
KELOMPOK_RESULTS = {
    1: "Kalori terhitung: 485 kcal, Protein: 24g, Karbohidrat: 58g, Lemak: 15g. Status: Seimbang.",
    2: "Menu Usulan: Nasi Putih, Ayam Kecap, Sup Bayam, Pisang. Nutrisi memenuhi target.",
    3: "Estimasi sisa porsi: 14.5%. Tingkat Kesukaan: Tinggi (Menu Layak Dilanjutkan).",
    4: "Sentimen Medsos: 72.4% Positif, 18.1% Netral, 9.5% Negatif. Respon positif stabil.",
    5: "Inspeksi Higienitas: Negatif kontaminan makro. Baki makanan 100% aman.",
    6: "Analisis YouTube: Indeks Sentimen 0.85, Tren sentimen opini mendatang meningkat.",
    7: "Evaluasi Pasca-Konsumsi: Sisa piring terdeteksi 5%, Status Piring: Habis.",
    8: "Kelengkapan baki saji: Terdeteksi Lengkap (Karbohidrat, Lauk, Sayur, Buah).",
    9: "Rencana logistik harian: Beras 75kg, Daging Ayam 45kg, Sayuran Hijau 30kg.",
    10: "Inspeksi Mikro ERX: Layak konsumsi (Safety Index: 99.8%, 0 anomali mikro).",
    11: "Penerimaan Bahan: Klasifikasi Segar (Tingkat kesegaran sayuran: 94.2%)."
}

# ==========================================
# PAGE ROUTES
# ==========================================

@app.route('/')
def index():
    """Render the Cover landing page with About section."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render the operational dashboard with log history and print report forms."""
    sessions = read_sessions()
    history = []
    
    # Calculate progress metrics for each date session
    for date, steps in sorted(sessions.items(), reverse=True):
        completed_count = 0
        for val in steps.values():
            if isinstance(val, dict) and val.get("status") == "completed":
                completed_count += 1
            elif isinstance(val, str) and val == "completed":
                completed_count += 1
                
        pct = int((completed_count / 11) * 100)
        history.append({
            "date": date,
            "pct": pct,
            "completed": completed_count
        })
        
    return render_template('dashboard.html', history=history)

@app.route('/session', methods=['POST'])
def start_session():
    """Handle redirection or creation of a daily session based on the form input date."""
    date = request.form.get('session-date')
    if not date:
        return redirect(url_for('dashboard'))
    return redirect(url_for('session_pipeline', date=date))

@app.route('/session/<date>')
def session_pipeline(date):
    """Render the daily pipeline dashboard for the given date, initializing it if new."""
    sessions = read_sessions()
    
    if date not in sessions:
        # Initialize all 11 kelompok as pending with placeholder results
        sessions[date] = {f"kelompok-{i}": {"status": "pending", "result": "Belum Selesai"} for i in range(1, 12)}
        write_sessions(sessions)
        
    steps = sessions[date]
    
    # Calculate progress metrics
    completed_count = 0
    jinja_steps = {}
    for key, val in steps.items():
        if isinstance(val, dict):
            status = val.get("status", "pending")
            jinja_steps[key] = status
            if status == "completed":
                completed_count += 1
        else:
            jinja_steps[key] = val
            if val == "completed":
                completed_count += 1
                
    pct = int((completed_count / 11) * 100)
    
    return render_template('pipeline.html', date=date, steps=jinja_steps, pct=pct, completed=completed_count)

@app.route('/session/<date>/complete/<kelompok>', methods=['GET', 'POST'])
def complete_step(date, kelompok):
    """Complete a specific group step for the specified session date, then redirect back to daily pipeline."""
    sessions = read_sessions()
    if date in sessions and kelompok in sessions[date]:
        num = int(kelompok.split('-')[1])
        custom_result = None
        if request.method == 'POST':
            custom_result = request.form.get('custom-result')
        if not custom_result:
            custom_result = KELOMPOK_RESULTS.get(num, "Tugas Selesai")
            
        sessions[date][kelompok] = {
            "status": "completed",
            "result": custom_result
        }
        write_sessions(sessions)
    return redirect(url_for('session_pipeline', date=date))


# ==========================================
# EDIT & DELETE APIS
# ==========================================

@app.route('/session/<date>/delete', methods=['POST'])
def delete_session(date):
    """Delete a daily operational session log."""
    sessions = read_sessions()
    if date in sessions:
        del sessions[date]
        write_sessions(sessions)
    return redirect(url_for('dashboard'))

@app.route('/session/<date>/rename', methods=['POST'])
def rename_session(date):
    """Rename/edit the date of an operational session log."""
    new_date = request.form.get('new-date')
    if not new_date:
        return redirect(url_for('dashboard'))
        
    sessions = read_sessions()
    if date in sessions and new_date not in sessions:
        sessions[new_date] = sessions[date]
        del sessions[date]
        write_sessions(sessions)
        
    return redirect(url_for('dashboard'))


# ==========================================
# REPORT PRINTING ROUTES (PDF FRIENDLY)
# ==========================================

def get_enriched_steps(steps):
    """Enrich steps with metadata and fallback results."""
    enriched_steps = []
    for key, val in steps.items():
        num = int(key.split('-')[1])
        meta = KELOMPOK_METADATA.get(num)
        
        status_label = "Belum Selesai"
        detail_result = "Belum Selesai (Tidak ada data)"
        
        if isinstance(val, dict):
            if val.get("status") == "completed":
                status_label = "Selesai"
            detail_result = val.get("result", "Belum Selesai (Tidak ada data)")
        elif isinstance(val, str):
            if val == "completed":
                status_label = "Selesai"
                detail_result = KELOMPOK_RESULTS.get(num, "Selesai")
                
        enriched_steps.append({
            "num": num,
            "title": meta["title"],
            "phase": meta["phase"],
            "algo": meta["algo"],
            "status": status_label,
            "result": detail_result
        })
        
    enriched_steps.sort(key=lambda x: x["num"])
    return enriched_steps

@app.route('/session/<date>/report')
def report_daily(date):
    """Render a print-ready daily operational summary report."""
    sessions = read_sessions()
    if date not in sessions:
        return redirect(url_for('index'))
        
    steps = sessions[date]
    completed_count = 0
    
    for val in steps.values():
        if isinstance(val, dict) and val.get("status") == "completed":
            completed_count += 1
        elif isinstance(val, str) and val == "completed":
            completed_count += 1
            
    pct = int((completed_count / 11) * 100)
    enriched_steps = get_enriched_steps(steps)
    
    return render_template(
        'report_print.html',
        type="Harian",
        scope=date,
        pct=pct,
        completed=completed_count,
        steps=enriched_steps
    )

@app.route('/report/monthly')
def report_monthly():
    """Render a monthly aggregate operational report based on a selected month (YYYY-MM)."""
    month = request.args.get('month')
    if not month:
        return redirect(url_for('index'))
        
    sessions = read_sessions()
    monthly_sessions = []
    
    for date, steps in sorted(sessions.items()):
        if date.startswith(month):
            completed_count = 0
            for val in steps.values():
                if isinstance(val, dict) and val.get("status") == "completed":
                    completed_count += 1
                elif isinstance(val, str) and val == "completed":
                    completed_count += 1
                    
            pct = int((completed_count / 11) * 100)
            enriched_steps = get_enriched_steps(steps)
            monthly_sessions.append({
                "date": date,
                "completed": completed_count,
                "pct": pct,
                "steps": enriched_steps
            })
            
    if not monthly_sessions:
        avg_pct = 0
    else:
        avg_pct = int(sum(s["pct"] for s in monthly_sessions) / len(monthly_sessions))
        
    return render_template(
        'report_print.html',
        type="Bulanan",
        scope=month,
        pct=avg_pct,
        completed=len(monthly_sessions),
        sessions=monthly_sessions
    )

@app.route('/report/yearly')
def report_yearly():
    """Render a yearly aggregate operational report based on a selected year (YYYY)."""
    year = request.args.get('year')
    if not year:
        return redirect(url_for('index'))
        
    sessions = read_sessions()
    yearly_sessions = []
    
    for date, steps in sorted(sessions.items()):
        if date.startswith(year):
            completed_count = 0
            for val in steps.values():
                if isinstance(val, dict) and val.get("status") == "completed":
                    completed_count += 1
                elif isinstance(val, str) and val == "completed":
                    completed_count += 1
                    
            pct = int((completed_count / 11) * 100)
            enriched_steps = get_enriched_steps(steps)
            yearly_sessions.append({
                "date": date,
                "completed": completed_count,
                "pct": pct,
                "steps": enriched_steps
            })
            
    if not yearly_sessions:
        avg_pct = 0
    else:
        avg_pct = int(sum(s["pct"] for s in yearly_sessions) / len(yearly_sessions))
        
    return render_template(
        'report_print.html',
        type="Tahunan",
        scope=year,
        pct=avg_pct,
        completed=len(yearly_sessions),
        sessions=yearly_sessions
    )


@app.route('/status')
def status():
    """Render the model status dashboard page."""
    return render_template('status.html')

@app.route('/kelompok-<int:num>')
def render_kelompok(num):
    """Render a simplified blank page template for a specific kelompok, maintaining active date context."""
    if num < 1 or num > 11:
        return redirect(url_for('index'))
        
    date = request.args.get('date')
    meta = KELOMPOK_METADATA.get(num, {"title": "Modul Kelompok", "algo": "Deep Learning", "phase": "Operasional"})
    
    # Check current status and result for this date if session is active
    status = "pending"
    result_val = KELOMPOK_RESULTS.get(num, "Tugas Selesai")
    
    if date:
        sessions = read_sessions()
        if date in sessions:
            val = sessions[date].get(f"kelompok-{num}", "pending")
            if isinstance(val, dict):
                status = val.get("status", "pending")
                result_val = val.get("result", result_val)
            else:
                status = val
                if val == "completed":
                    result_val = KELOMPOK_RESULTS.get(num, "Tugas Selesai")
            
    return render_template(
        f'Kelompok_{num}/kelompok_{num}.html',
        num=num,
        date=date,
        meta=meta,
        status=status,
        result=result_val
    )


# ==========================================
# SERVER RUNNER
# ==========================================

if __name__ == '__main__':
    # Initialize sessions.json if not present
    if not os.path.exists(SESSIONS_FILE):
        write_sessions({})
        
    app.run(debug=True, port=5050)
