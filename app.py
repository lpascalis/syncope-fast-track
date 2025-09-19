import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Syncope Fast Track", layout="wide")

st.title("Syncope Fast Track")
st.write("Strumento interattivo di supporto clinico per la valutazione di pazienti con sincope.")

# --- DATI ANAGRAFICI ---
st.header("Dati paziente")
nome = st.text_input("Nome")
eta = st.number_input("Età", min_value=1, max_value=120, value=65)
sesso = st.selectbox("Sesso", ["Maschio", "Femmina"])

# --- CIRCOSTANZA ---
st.header("Circostanza della sincope")
circostanza = st.selectbox("Evento", [
    "Supina", "Durante sforzo", "Ortostatismo", "Minzione/defecazione/deglutizione",
    "Dolore/stress emotivo", "Post-prandiale", "Altro"
])

# --- STORIA CLINICA ---
st.header("Anamnesi")
cardiopatia = st.checkbox("Cardiopatia nota (ischemica, valvolare, CMP, FE ridotta)")
familiarita = st.checkbox("Familiarità per morte improvvisa")
recidive = st.checkbox("Eventi sincopali precedenti")
trauma = st.checkbox("Trauma grave associato")

# --- SINTOMI PRODROMICI ---
st.header("Sintomi prodromici")
prodromi = st.multiselect("Seleziona", ["Palpitazioni", "Dolore toracico", "Dispnea", "Sintomi vagali", "Nessuno"])

# --- ECG ---
st.header("ECG")
ecg = st.multiselect("Seleziona", [
    "Normale", "Blocco di branca", "QT lungo", "Brugada", "Preeccitazione", "Ischemia/ST-T alterati", "TV/FV documentata"
])

# --- ORTOSTATISMO ---
st.header("Orto-statismo")
pas_supina = st.number_input("PAS supina (mmHg)", min_value=50, max_value=250, value=120)
pad_supina = st.number_input("PAD supina (mmHg)", min_value=30, max_value=150, value=70)
fc_supina = st.number_input("FC supina (bpm)", min_value=30, max_value=180, value=70)
pas_3min = st.number_input("PAS a 3' in ortostatismo (mmHg)", min_value=50, max_value=250, value=110)
pad_3min = st.number_input("PAD a 3' in ortostatismo (mmHg)", min_value=30, max_value=150, value=65)
fc_3min = st.number_input("FC a 3' in ortostatismo (bpm)", min_value=30, max_value=180, value=90)
sintomi_orto = st.checkbox("Riproduzione dei sintomi durante test ortostatico")

# --- LABORATORIO ---
st.header("Esami di laboratorio")
troponina_pos = st.checkbox("Troponina elevata")
hb = st.number_input("Emoglobina (g/dL)", min_value=5.0, max_value=20.0, value=13.0)

# --- TEST FUNZIONALI ---
st.header("Test funzionali")
tilt = st.selectbox("Tilt test", ["Non eseguito", "Riflessa", "Ortostatica", "POTS", "PPS", "Negativo"])
csm_pausa = st.number_input("CSM: pausa (s)", min_value=0.0, max_value=15.0, value=0.0)
csm_drop = st.number_input("CSM: ΔPAS (mmHg)", min_value=0, max_value=100, value=0)
csm_sintomi = st.checkbox("CSM: riproduzione sintomi")

# --- PERCORSO ARITMICO ---
st.header("Percorso aritmico")
bbb = st.checkbox("Blocco bifascicolare all'ECG")
hv = st.number_input("HV all'EPS (ms)", min_value=30, max_value=120, value=50)
blocchi_hp = st.checkbox("Blocco HP indotto all'EPS")
ilr_avb = st.checkbox("ILR: AV block/asistolia documentata")
tachiaritmia = st.selectbox("Tachiaritmie documentate", ["Nessuna", "SVT", "VT non ablata", "VT ablata"])
fe = st.number_input("Frazione di eiezione (%)", min_value=10, max_value=80, value=55)

# --- LOGICA DI RISCHIO ---
alto_rischio = False
if circostanza in ["Supina", "Durante sforzo"]:
    alto_rischio = True
if cardiopatia or trauma or troponina_pos or hb < 10:
    alto_rischio = True
if any(e in ecg for e in ["Blocco di branca", "QT lungo", "Brugada", "Preeccitazione", "Ischemia/ST-T alterati", "TV/FV documentata"]):
    alto_rischio = True

if alto_rischio:
    risk_label = "ALTO RISCHIO"
    raccomandazione = "Monitoraggio intensivo e ricovero/OBI suggerito."
else:
    risk_label = "BASSO RISCHIO"
    raccomandazione = "Possibile follow-up ambulatoriale o osservazione breve."

# --- OUTPUT ---
st.header("Risultato valutazione")
st.write(f"**Classificazione rischio:** {risk_label}")
st.write(f"**Suggerimento:** {raccomandazione}")

# --- EXPORT PDF ---
if st.button("Genera referto PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Referto Syncope Fast Track", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Nome: {nome}", ln=True)
    pdf.cell(200, 10, f"Età: {eta}", ln=True)
    pdf.cell(200, 10, f"Sesso: {sesso}", ln=True)
    pdf.cell(200, 10, f"Circostanza: {circostanza}", ln=True)
    pdf.multi_cell(0, 10, f"ECG: {', '.join(ecg)}")
    pdf.cell(200, 10, f"Classificazione: {risk_label}", ln=True)
    pdf.multi_cell(0, 10, f"Raccomandazione: {raccomandazione}")
    pdf.ln(10)
    pdf.cell(200, 10, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.output("referto.pdf")
    with open("referto.pdf", "rb") as file:
        st.download_button("Scarica referto PDF", file, "referto.pdf")
