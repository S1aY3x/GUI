import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit.components.v1 import html

# Set page config FIRST
st.set_page_config(page_title="Transformer Losses Analyzer", layout="wide")

# Custom CSS for animations and styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* Hide scrollbar but keep functionality */
::-webkit-scrollbar {
    display: none; /* Hide scrollbar for Chrome, Safari, and Opera */
}

body {
    -ms-overflow-style: none; /* Hide scrollbar for IE and Edge */
    scrollbar-width: none; /* Hide scrollbar for Firefox */
}

/* Remove black lines between all sections */
.stMarkdown, .card, .stButton, .stSlider, .stSelectbox, .stNumberInput, .stRadio {
    border-top: none !important;
    border-bottom: none !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* Rest of your existing CSS code */
body {
    font-family: 'Roboto', sans-serif;
    background-color: #1e1e1e;
    color: #ffffff;
}

.stApp {
    background: linear-gradient(135deg, #1e1e1e, #2c3e50);
}

h1, h2, h3, h4, h5, h6 {
    color: #ffffff;
    position: relative;
    padding-left: 10px;
}

h1::before, h2::before, h3::before {
    /* Remove these lines completely or comment them out */
    /* content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 4px;
    background: linear-gradient(180deg, #4CAF50, #2196F3);
    border-radius: 2px; */
}

.title-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.03); }
    100% { transform: scale(1); }
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stButton>button:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.stSlider>div>div>div>div {
    background-color: #4CAF50 !important;
}

.stSelectbox>div>div>div {
    background-color: #2c3e50 !important;
    border-radius: 5px;
}

.stNumberInput>div>div>input {
    background-color: #2c3e50 !important;
    color: white !important;
    border-radius: 5px;
}

.stRadio>div>label {
    color: #ffffff;
}

.stMarkdown {
    animation: fadeIn 1s ease-in-out;
}

.card {
    background-color: rgba(25, 25, 35, 0.7);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
}

.parameter {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.parameter-value {
    font-weight: 700;
    color: #4CAF50;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.stSidebar {
    background-color: #1a2639;
    color: #ffffff;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.stSidebar .stMarkdown {
    color: #ffffff;
}

.calculation-box {
    background-color: rgba(76, 175, 80, 0.1);
    border-left: 4px solid #4CAF50;
    padding: 15px;
    border-radius: 5px;
    margin-top: 10px;
    margin-bottom: 10px;
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

/* Light Mode Overrides */
.light-mode {
    background-color: #f8f9fa !important;
    color: #333333 !important;
}

.light-mode .stApp {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef) !important;
}

.light-mode h1, .light-mode h2, .light-mode h3, .light-mode h4, .light-mode h5, .light-mode h6 {
    color: #2c3e50 !important;
}

.light-mode .stSidebar {
    background-color: #ffffff !important;
    color: #333333 !important;
}

.light-mode .card {
    background-color: rgba(255, 255, 255, 0.9) !important;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.light-mode .parameter-value {
    color: #2c8c3c !important;
}

/* Progress bar styling */
.stProgress > div > div > div > div {
    background-color: #4CAF50 !important;
}

/* Tooltip on hover */
.tooltip {
    position: relative;
    display: inline-block;
    cursor: pointer;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -100px;
    opacity: 0;
    transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

/* 3D Card Effect */
.card-3d {
    transition: transform 0.5s;
    transform-style: preserve-3d;
}

.card-3d:hover {
    transform: perspective(1000px) rotateX(5deg) rotateY(5deg);
}
</style>
""", unsafe_allow_html=True)

# Function Definitions
def iron_loss(voltage, frequency, core_material):
    """Calculate iron losses based on voltage, frequency, and core material."""
    kh = {'CRGO': 0.002, 'Ferrite': 0.005}
    ke = {'CRGO': 0.0001, 'Ferrite': 0.0002}
    return kh.get(core_material, 0.002) * (voltage ** 2) * (frequency ** 1.6) + ke.get(core_material, 0.0001) * (voltage ** 2) * frequency

def copper_loss(current, resistance):
    """Calculate copper losses based on current and winding resistance."""
    return (current ** 2) * resistance

def stray_loss(load_power, efficiency, temp_factor=0.0005):
    """Calculate stray losses based on load power, efficiency, and temperature factor."""
    return temp_factor * load_power * (1 - efficiency / 100)

def dielectric_loss(voltage, insulation_factor=0.0005):
    """Calculate dielectric losses based on voltage and insulation factor."""
    return insulation_factor * (voltage ** 2)

def efficiency(output_power, input_power):
    """Calculate overall efficiency."""
    return (output_power / input_power) * 100 if input_power != 0 else 0

def calculate_losses(voltage, frequency, kva_rating, core_material, resistance, load_percent, temperature):
    """Calculate all losses and overall efficiency."""
    if voltage == 0 or kva_rating == 0:
        return 0, 0, 0, 0, 0, 0, 0
    
    load_power = (load_percent / 100) * (kva_rating * 1000)
    current = load_power / voltage
    iron_losses = iron_loss(voltage, frequency, core_material)
    copper_losses = copper_loss(current, resistance)
    stray_losses = stray_loss(load_power, efficiency(load_power, load_power + iron_losses + copper_losses), temperature/1000)
    dielectric_losses = dielectric_loss(voltage)
    total_losses = iron_losses + copper_losses + stray_losses + dielectric_losses
    input_power = load_power + total_losses
    overall_efficiency = efficiency(load_power, input_power)
    
    return iron_losses, copper_losses, stray_losses, dielectric_losses, total_losses, input_power, overall_efficiency

st.markdown("""
<div class="title-container">
    <h1 style="font-size: 1.5rem;">⚡ Transformer Losses Analyzer & Efficiency Calculator ⚡</h1>
</div>
""", unsafe_allow_html=True)
# Sidebar Inputs
st.sidebar.header("🔧 Transformer Input Parameters")

voltage_primary = st.sidebar.slider("Primary Voltage (V)", 200, 500, 230)
voltage_secondary = st.sidebar.slider("Secondary Voltage (V)", 50, 250, 115)  # Added secondary voltage
frequency = st.sidebar.slider("Frequency (Hz)", 40, 60, 50)
kva_rating = st.sidebar.number_input("Rated Power (kVA)", 1, 1000, 100)
core_material = st.sidebar.selectbox("Core Material", ["CRGO", "Ferrite"])
resistance = st.sidebar.slider("Winding Resistance (Ω)", 0.1, 5.0, 0.5)
load_percent = st.sidebar.slider("Load Percentage (%)", 0, 100, 50)
temperature = st.sidebar.slider("Operating Temperature (°C)", 20, 150, 75)

# Calculate Turns Ratio
turns_ratio = voltage_primary / voltage_secondary if voltage_secondary != 0 else 0

# Dark Mode Toggle
dir_mode = st.sidebar.radio("🌗 Select Mode", ["Dark Mode", "Light Mode"])

if dir_mode == "Light Mode":
    st.markdown("""
    <script>
        document.querySelector('body').classList.add('light-mode');
        document.querySelector('.stApp').classList.add('light-mode');
        document.querySelector('.stSidebar').classList.add('light-mode');
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
        document.querySelector('body').classList.remove('light-mode');
        document.querySelector('.stApp').classList.remove('light-mode');
        document.querySelector('.stSidebar').classList.remove('light-mode');
    </script>
    """, unsafe_allow_html=True)

# Calculate losses dynamically
iron_losses, copper_losses, stray_losses, dielectric_losses, total_losses, input_power, overall_efficiency = calculate_losses(
    voltage_primary, frequency, kva_rating, core_material, resistance, load_percent, temperature
)

# Current load power calculation
load_power = (load_percent / 100) * (kva_rating * 1000)


        # Graph Section
st.markdown('<div class="card card-3d">', unsafe_allow_html=True)
st.subheader("📈 Graph Visualization")
graph_option = st.radio("Choose Graph", ["Efficiency vs Load", "Losses vs Voltage", "Stray Losses vs Temperature"])

if graph_option == "Efficiency vs Load":
    # Generate data for Efficiency vs Load graph
    load_percentages = np.linspace(0, 100, 100)
    efficiencies = [calculate_losses(voltage_primary, frequency, kva_rating, core_material, resistance, load, temperature)[6] for load in load_percentages]
    
    fig = px.line(x=load_percentages, y=efficiencies, labels={'x': 'Load Percentage (%)', 'y': 'Efficiency (%)'}, title="Efficiency vs Load Percentage")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif graph_option == "Losses vs Voltage":
    # Generate data for Losses vs Voltage graph
    voltages = np.linspace(200, 500, 100)
    iron_losses_list = [iron_loss(v, frequency, core_material) for v in voltages]
    copper_losses_list = [copper_loss((load_percent / 100) * (kva_rating * 1000) / v, resistance) for v in voltages]
    stray_losses_list = [stray_loss((load_percent / 100) * (kva_rating * 1000), efficiency((load_percent / 100) * (kva_rating * 1000), (load_percent / 100) * (kva_rating * 1000) + iron_loss(v, frequency, core_material) + copper_loss((load_percent / 100) * (kva_rating * 1000) / v, resistance)), temperature/1000) for v in voltages]
    dielectric_losses_list = [dielectric_loss(v) for v in voltages]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=voltages, y=iron_losses_list, mode='lines', name='Iron Losses'))
    fig.add_trace(go.Scatter(x=voltages, y=copper_losses_list, mode='lines', name='Copper Losses'))
    fig.add_trace(go.Scatter(x=voltages, y=stray_losses_list, mode='lines', name='Stray Losses'))
    fig.add_trace(go.Scatter(x=voltages, y=dielectric_losses_list, mode='lines', name='Dielectric Losses'))
    
    fig.update_layout(title="Losses vs Voltage", xaxis_title="Voltage (V)", yaxis_title="Losses (W)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif graph_option == "Stray Losses vs Temperature":
    # Generate data for Stray Losses vs Temperature graph
    temperatures = np.linspace(20, 150, 100)
    stray_losses_list = [stray_loss((load_percent / 100) * (kva_rating * 1000), efficiency((load_percent / 100) * (kva_rating * 1000), (load_percent / 100) * (kva_rating * 1000) + iron_loss(voltage_primary, frequency, core_material) + copper_loss((load_percent / 100) * (kva_rating * 1000) / voltage_primary, resistance)), temp/1000) for temp in temperatures]
    
    fig = px.line(x=temperatures, y=stray_losses_list, labels={'x': 'Temperature (°C)', 'y': 'Stray Losses (W)'}, title="Stray Losses vs Temperature")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Display Results in Cards
st.markdown('<div class="card card-3d">', unsafe_allow_html=True)
st.subheader("📊 Losses Breakdown")
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="parameter"><span>Iron Losses:</span><span class="parameter-value">{:.2f} W</span></div>'.format(iron_losses), unsafe_allow_html=True)
    st.markdown('<div class="parameter"><span>Copper Losses:</span><span class="parameter-value">{:.2f} W</span></div>'.format(copper_losses), unsafe_allow_html=True)
    st.markdown('<div class="parameter"><span>Stray Losses:</span><span class="parameter-value">{:.2f} W</span></div>'.format(stray_losses), unsafe_allow_html=True)
    st.markdown('<div class="parameter"><span>Dielectric Losses:</span><span class="parameter-value">{:.2f} W</span></div>'.format(dielectric_losses), unsafe_allow_html=True)
    st.markdown('<div class="parameter"><span>Total Losses:</span><span class="parameter-value">{:.2f} W</span></div>'.format(total_losses), unsafe_allow_html=True)

with col2:
    st.markdown('<div class="parameter"><span>Load Power:</span><span class="parameter-value">{:.2f} W</span></div>'.format(load_power), unsafe_allow_html=True)
    st.markdown('<div class="parameter"><span>Input Power:</span><span class="parameter-value">{:.2f} W</span></div>'.format(input_power), unsafe_allow_html=True)
    st.markdown('<div class="parameter"><span>Overall Efficiency:</span><span class="parameter-value">{:.2f}%</span></div>'.format(overall_efficiency), unsafe_allow_html=True)
    st.markdown('<div class="parameter"><span>Turns Ratio (N1/N2):</span><span class="parameter-value">{:.2f}</span></div>'.format(turns_ratio), unsafe_allow_html=True)  # Added turns ratio
    
    # Progress bar for efficiency visualization
    st.progress(min(overall_efficiency/100, 1.0))
    
st.markdown('</div>', unsafe_allow_html=True)

# Efficiency section
st.markdown('<div class="card card-3d">', unsafe_allow_html=True)
st.subheader("⚙️ Efficiency Analysis")

# Toggle for detailed calculations
show_calculations = st.checkbox("📋 Show Detailed Calculations")

if show_calculations:
    st.markdown('<div class="calculation-box">', unsafe_allow_html=True)
    st.markdown("#### Iron Losses Calculation")
    st.latex(r"P_{iron} = k_h \times V^2 \times f^{1.6} + k_e \times V^2 \times f")
    st.markdown(f"""
    Where:
    - kh = {0.002 if core_material == 'CRGO' else 0.005} (based on {core_material} core)
    - ke = {0.0001 if core_material == 'CRGO' else 0.0002} (based on {core_material} core)
    - V = {voltage_primary} V
    - f = {frequency} Hz
    
    Calculation:
    - Iron Losses = {0.002 if core_material == 'CRGO' else 0.005} × ({voltage_primary}²) × ({frequency}^1.6) + {0.0001 if core_material == 'CRGO' else 0.0002} × ({voltage_primary}²) × {frequency}
    - Iron Losses = {iron_losses:.2f} W
    """)
    
    st.markdown("#### Copper Losses Calculation")
    st.latex(r"P_{copper} = I^2 \times R")
    st.markdown(f"""
    Where:
    - I = Load Power / Voltage = {load_power:.2f} / {voltage_primary} = {load_power/voltage_primary:.2f} A
    - R = {resistance} Ω
    
    Calculation:
    - Copper Losses = ({load_power/voltage_primary:.2f}²) × {resistance}
    - Copper Losses = {copper_losses:.2f} W
    """)
    
    st.markdown("#### Stray Losses Calculation")
    st.latex(r"P_{stray} = temp\_factor \times P_{load} \times (1 - \eta/100)")
    st.markdown(f"""
    Where:
    - temp_factor = {temperature/1000:.6f} (based on {temperature}°C)
    - P_load = {load_power:.2f} W
    - η = Efficiency without stray losses = {efficiency(load_power, load_power + iron_losses + copper_losses):.2f}%
    
    Calculation:
    - Stray Losses = {temperature/1000:.6f} × {load_power:.2f} × (1 - {efficiency(load_power, load_power + iron_losses + copper_losses):.2f}/100)
    - Stray Losses = {stray_losses:.2f} W
    """)
    
    st.markdown("#### Dielectric Losses Calculation")
    st.latex(r"P_{dielectric} = insulation\_factor \times V^2")
    st.markdown(f"""
    Where:
    - insulation_factor = 0.0005 (constant)
    - V = {voltage_primary} V
    
    Calculation:
    - Dielectric Losses = 0.0005 × ({voltage_primary}²)
    - Dielectric Losses = {dielectric_losses:.2f} W
    """)
    
    st.markdown("#### Overall Efficiency Calculation")
    st.latex(r"\eta = \frac{P_{output}}{P_{input}} \times 100\%")
    st.markdown(f"""
    Where:
    - P_output = Load Power = {load_power:.2f} W
    - P_input = Load Power + Total Losses = {load_power:.2f} + {total_losses:.2f} = {input_power:.2f} W
    
    Calculation:
    - Efficiency = ({load_power:.2f} / {input_power:.2f}) × 100%
    - Efficiency = {overall_efficiency:.2f}%
    """)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    Toggle the checkbox above to see step-by-step calculations with formulas.
    """)
    
st.markdown('</div>', unsafe_allow_html=True)

# 3D Transformer Visualization Section
st.markdown('<div class="card card-3d">', unsafe_allow_html=True)
st.subheader("🔄 Interactive 3D Transformer Model")

# Toggle for 3D Transformer Visualization
show_3d_model = st.checkbox("🔄 Show Interactive 3D Transformer Model")

if show_3d_model:
    # Keep the existing HTML/JavaScript code for the 3D visualization
   html("""
<div id="transformer-3d" style="height: 600px; width: 100%; margin: 20px 0; border-radius: 10px; box-shadow: 0 10px 20px rgba(0,0,0,0.2);"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
// Initialize the 3D scene
function initTransformerVisualization() {
    const container = document.getElementById('transformer-3d');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    // Create scene, camera, and renderer
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a192f); // Darker blue background for better contrast
    
    const camera = new THREE.PerspectiveCamera(75, width/height, 0.1, 1000);
    camera.position.z = 12;
    camera.position.y = 4;
    camera.position.x = 4;
    
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 1.2);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1.5);
    directionalLight.position.set(5, 5, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    
    // Add point lights for enhanced lighting
    const pointLight1 = new THREE.PointLight(0x3498db, 1, 20);
    pointLight1.position.set(8, 5, 5);
    scene.add(pointLight1);
    
    const pointLight2 = new THREE.PointLight(0xe74c3c, 1, 20);
    pointLight2.position.set(-8, -5, 5);
    scene.add(pointLight2);
    
    // Create transformer group
    const transformerGroup = new THREE.Group();
    scene.add(transformerGroup);
    
    // Add a base/platform for the transformer
    const baseMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x333333,
        shininess: 20
    });
    const baseGeometry = new THREE.BoxGeometry(8, 0.5, 6);
    const base = new THREE.Mesh(baseGeometry, baseMaterial);
    base.position.y = -3;
    base.receiveShadow = true;
    transformerGroup.add(base);
    
    // Add transformer core (E-I laminations style) with metallic material
    const coreMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x777777, 
        shininess: 80,
        specular: 0x444444,
        emissive: 0x222222
    });
    
    // Create E part of the core
    const eCoreGeometry = new THREE.BoxGeometry(4, 5, 1);
    const eCore = new THREE.Mesh(eCoreGeometry, coreMaterial);
    eCore.position.z = -0.5;
    eCore.castShadow = true;
    eCore.receiveShadow = true;
    transformerGroup.add(eCore);
    
    // Create the three prongs of the E
    const topProngGeometry = new THREE.BoxGeometry(1.3, 1, 2);
    const topProng = new THREE.Mesh(topProngGeometry, coreMaterial);
    topProng.position.set(0, 2, 0.5);
    topProng.castShadow = true;
    topProng.receiveShadow = true;
    transformerGroup.add(topProng);
    
    const middleProngGeometry = new THREE.BoxGeometry(1.3, 1, 2);
    const middleProng = new THREE.Mesh(middleProngGeometry, coreMaterial);
    middleProng.position.set(0, 0, 0.5);
    middleProng.castShadow = true;
    middleProng.receiveShadow = true;
    transformerGroup.add(middleProng);
    
    const bottomProngGeometry = new THREE.BoxGeometry(1.3, 1, 2);
    const bottomProng = new THREE.Mesh(bottomProngGeometry, coreMaterial);
    bottomProng.position.set(0, -2, 0.5);
    bottomProng.castShadow = true;
    bottomProng.receiveShadow = true;
    transformerGroup.add(bottomProng);
    
    // I part of the core
    const iCoreGeometry = new THREE.BoxGeometry(4, 5, 1);
    const iCore = new THREE.Mesh(iCoreGeometry, coreMaterial);
    iCore.position.z = 1.5;
    iCore.castShadow = true;
    iCore.receiveShadow = true;
    transformerGroup.add(iCore);
    
    // Add primary winding (copper coil) with enhanced materials
    const copperMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xcd7f32,
        shininess: 120,
        specular: 0xffd700,
        emissive: 0x3d2616,
        emissiveIntensity: 0.2
    });
    
    // Primary winding around top leg - more detailed with more turns
    const primaryWindingGeometry = new THREE.TorusGeometry(0.9, 0.3, 20, 40);
    
    // Create multiple turns for primary winding
    for (let i = 0; i < 7; i++) {
        const primaryTurn = new THREE.Mesh(primaryWindingGeometry, copperMaterial);
        primaryTurn.position.set(0, 2, 0.5);
        primaryTurn.rotation.x = Math.PI / 2;
        primaryTurn.position.y += 0.15 * (i - 3);
        primaryTurn.castShadow = true;
        primaryTurn.receiveShadow = true;
        transformerGroup.add(primaryTurn);
    }
    
    // Secondary winding around bottom leg - more detailed
    const secondaryWindingGeometry = new THREE.TorusGeometry(0.9, 0.25, 20, 40);
    
    // Create multiple turns for secondary winding
    for (let i = 0; i < 10; i++) {
        const secondaryTurn = new THREE.Mesh(secondaryWindingGeometry, copperMaterial);
        secondaryTurn.position.set(0, -2, 0.5);
        secondaryTurn.rotation.x = Math.PI / 2;
        secondaryTurn.position.y -= 0.12 * (i - 4.5);
        secondaryTurn.castShadow = true;
        secondaryTurn.receiveShadow = true;
        transformerGroup.add(secondaryTurn);
    }
    
    // Add terminal connectors with enhanced shiny look
    const terminalMaterial = new THREE.MeshPhongMaterial({
        color: 0xC0C0C0,
        shininess: 120,
        specular: 0xffffff
    });
    
    // Primary terminals
    const primaryTerminal1 = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.4, 20), terminalMaterial);
    primaryTerminal1.position.set(1.7, 2, 0.5);
    primaryTerminal1.rotation.z = Math.PI / 2;
    primaryTerminal1.castShadow = true;
    transformerGroup.add(primaryTerminal1);
    
    const primaryTerminal2 = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.4, 20), terminalMaterial);
    primaryTerminal2.position.set(-1.7, 2, 0.5);
    primaryTerminal2.rotation.z = Math.PI / 2;
    primaryTerminal2.castShadow = true;
    transformerGroup.add(primaryTerminal2);
    
    // Add connecting wires to terminals for primary
    const wireMaterial = new THREE.MeshPhongMaterial({
        color: 0x333333,
        shininess: 30
    });
    
    const primaryWire1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2, 10), wireMaterial);
    primaryWire1.position.set(2.7, 2, 0.5);
    primaryWire1.rotation.z = Math.PI / 2;
    primaryWire1.castShadow = true;
    transformerGroup.add(primaryWire1);
    
    const primaryWire2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2, 10), wireMaterial);
    primaryWire2.position.set(-2.7, 2, 0.5);
    primaryWire2.rotation.z = Math.PI / 2;
    primaryWire2.castShadow = true;
    transformerGroup.add(primaryWire2);
    
    // Secondary terminals
    const secondaryTerminal1 = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.4, 20), terminalMaterial);
    secondaryTerminal1.position.set(1.7, -2, 0.5);
    secondaryTerminal1.rotation.z = Math.PI / 2;
    secondaryTerminal1.castShadow = true;
    transformerGroup.add(secondaryTerminal1);
    
    const secondaryTerminal2 = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.4, 20), terminalMaterial);
    secondaryTerminal2.position.set(-1.7, -2, 0.5);
    secondaryTerminal2.rotation.z = Math.PI / 2;
    secondaryTerminal2.castShadow = true;
    transformerGroup.add(secondaryTerminal2);
    
    // Add connecting wires to terminals for secondary
    const secondaryWire1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2, 10), wireMaterial);
    secondaryWire1.position.set(2.7, -2, 0.5);
    secondaryWire1.rotation.z = Math.PI / 2;
    secondaryWire1.castShadow = true;
    transformerGroup.add(secondaryWire1);
    
    const secondaryWire2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2, 10), wireMaterial);
    secondaryWire2.position.set(-2.7, -2, 0.5);
    secondaryWire2.rotation.z = Math.PI / 2;
    secondaryWire2.castShadow = true;
    transformerGroup.add(secondaryWire2);
    
    // Add heat visualization particles for iron losses - more realistic
    const ironLossesGroup = new THREE.Group();
    scene.add(ironLossesGroup);
    
    // More particles for better visual effect
    for (let i = 0; i < 80; i++) {
        const particleGeometry = new THREE.SphereGeometry(0.07, 10, 10);
        const heatColor = new THREE.Color().setHSL(0.05, 0.8, 0.5 + Math.random() * 0.3);
        const particleMaterial = new THREE.MeshBasicMaterial({ 
            color: heatColor,
            transparent: true,
            opacity: 0.7
        });
        const particle = new THREE.Mesh(particleGeometry, particleMaterial);
        
        // Random positions around the core
        particle.position.x = (Math.random() - 0.5) * 5;
        particle.position.y = (Math.random() - 0.5) * 6;
        particle.position.z = (Math.random() - 0.5) * 3;
        
        // Additional properties for animation
        particle.userData = {
            speed: 0.01 + Math.random() * 0.03,
            direction: new THREE.Vector3(
                (Math.random() - 0.5) * 2,
                (Math.random() - 0.5) * 2,
                (Math.random() - 0.5) * 2
            ).normalize(),
            lifetime: Math.random() * 150 + 50,
            age: Math.random() * 50, // Start at random ages for more natural look
            initialOpacity: 0.5 + Math.random() * 0.5,
            pulseSpeed: 0.05 + Math.random() * 0.05,
            pulsePhase: Math.random() * Math.PI * 2
        };
        
        ironLossesGroup.add(particle);
    }
    
    // Add magnetic field visualization
    const magneticFieldGroup = new THREE.Group();
    scene.add(magneticFieldGroup);
    
    const fieldLineMaterial = new THREE.MeshBasicMaterial({
        color: 0x4287f5,
        transparent: true,
        opacity: 0.4
    });
    
    // Create magnetic field lines around the transformer
    for (let i = 0; i < 16; i++) {
        const angle = (Math.PI * 2 / 16) * i;
        const radius = 3 + Math.random() * 1.5;
        
        const fieldLineGeometry = new THREE.TorusGeometry(radius, 0.05, 8, 32);
        const fieldLine = new THREE.Mesh(fieldLineGeometry, fieldLineMaterial);
        
        // Position and orient the field line
        fieldLine.position.set(0, 0, 0.5);
        fieldLine.rotation.y = angle;
        fieldLine.rotation.x = Math.PI / 2;
        
        // Add properties for animation
        fieldLine.userData = {
            pulseRate: 0.03 + Math.random() * 0.02,
            pulsePhase: Math.random() * Math.PI * 2,
            initialOpacity: 0.2 + Math.random() * 0.3,
            radius: radius
        };
        
        magneticFieldGroup.add(fieldLine);
    }
    
    // Create text labels for losses with enhanced styling
    const createTextLabel = (text, position, color = 0xffffff) => {
        const div = document.createElement('div');
        div.className = 'label';
        div.textContent = text;
        div.style.position = 'absolute';
        div.style.fontSize = '14px';
        div.style.fontWeight = 'bold';
        div.style.color = `#${color.toString(16).padStart(6, '0')}`;
        div.style.padding = '4px 8px';
        div.style.backgroundColor = 'rgba(0,0,0,0.7)';
        div.style.borderRadius = '5px';
        div.style.border = `1px solid #${color.toString(16).padStart(6, '0')}`;
        div.style.boxShadow = '0 2px 5px rgba(0,0,0,0.5)';
        div.style.transition = 'opacity 0.3s';
        container.appendChild(div);
        
        return { element: div, position: position };
    };
    
    const labels = [
        createTextLabel('Iron Losses (Core)', new THREE.Vector3(0, 0, 2), 0xff5733),
        createTextLabel('Primary Winding (Copper Losses)', new THREE.Vector3(3.5, 2, 0.5), 0xcd7f32),
        createTextLabel('Secondary Winding (Copper Losses)', new THREE.Vector3(-3.5, -2, 0.5), 0xcd7f32),
        createTextLabel('Magnetic Field', new THREE.Vector3(0, 4, 0), 0x4287f5),
        createTextLabel('Dielectric Losses', new THREE.Vector3(0, -4, 0), 0x9a42f5)
    ];
    
    // Add electricity visualization for primary winding - enhanced with tails
    const primaryElectricityGroup = new THREE.Group();
    transformerGroup.add(primaryElectricityGroup);
    
    const primaryElectricityParticles = [];
    const electricityMaterial = new THREE.MeshBasicMaterial({ 
        color: 0x00ffff,
        transparent: true,
        opacity: 0.9
    });
    
    for (let i = 0; i < 18; i++) {
        const particle = new THREE.Mesh(new THREE.SphereGeometry(0.1, 10, 10), electricityMaterial);
        particle.visible = false;
        primaryElectricityGroup.add(particle);
        
        // Create particle tail (trail effect)
        const tailGeometry = new THREE.CylinderGeometry(0.05, 0.01, 0.3, 8);
        const tailMaterial = new THREE.MeshBasicMaterial({
            color: 0x7df9ff,
            transparent: true,
            opacity: 0.6
        });
        const tail = new THREE.Mesh(tailGeometry, tailMaterial);
        tail.visible = false;
        primaryElectricityGroup.add(tail);
        
        primaryElectricityParticles.push({
            mesh: particle,
            tail: tail,
            angle: (Math.PI * 2 / 18) * i,
            speed: 0.12 + Math.random() * 0.04,
            radius: 0.9,
            yPos: 2,
            pulsePhase: Math.random() * Math.PI * 2
        });
    }
    
    // Add electricity visualization for secondary winding - enhanced
    const secondaryElectricityGroup = new THREE.Group();
    transformerGroup.add(secondaryElectricityGroup);
    
    const secondaryElectricityParticles = [];
    
    for (let i = 0; i < 18; i++) {
        const particle = new THREE.Mesh(new THREE.SphereGeometry(0.1, 10, 10), new THREE.MeshBasicMaterial({
            color: 0x7df9ff,
            transparent: true,
            opacity: 0.9
        }));
        particle.visible = false;
        secondaryElectricityGroup.add(particle);
        
        // Create particle tail (trail effect)
        const tailGeometry = new THREE.CylinderGeometry(0.05, 0.01, 0.3, 8);
        const tailMaterial = new THREE.MeshBasicMaterial({
            color: 0x00ffff,
            transparent: true,
            opacity: 0.6
        });
        const tail = new THREE.Mesh(tailGeometry, tailMaterial);
        tail.visible = false;
        secondaryElectricityGroup.add(tail);
        
        secondaryElectricityParticles.push({
            mesh: particle,
            tail: tail,
            angle: (Math.PI * 2 / 18) * i,
            speed: 0.1 + Math.random() * 0.03,
            radius: 0.9,
            yPos: -2,
            pulsePhase: Math.random() * Math.PI * 2
        });
    }
    
    // Add sparking effect at terminals
    const createSparkEffect = (position) => {
        const sparkGroup = new THREE.Group();
        sparkGroup.position.copy(position);
        transformerGroup.add(sparkGroup);
        
        const sparkParticles = [];
        
        for (let i = 0; i < 8; i++) {
            const sparkGeometry = new THREE.SphereGeometry(0.03 + Math.random() * 0.04, 8, 8);
            const sparkMaterial = new THREE.MeshBasicMaterial({
                color: new THREE.Color().setHSL(0.55 + Math.random() * 0.1, 1, 0.7),
                transparent: true,
                opacity: 0.8
            });
            
            const spark = new THREE.Mesh(sparkGeometry, sparkMaterial);
            spark.visible = false;
            sparkGroup.add(spark);
            
            sparkParticles.push({
                mesh: spark,
                direction: new THREE.Vector3(
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2
                ).normalize(),
                speed: 0.05 + Math.random() * 0.2,
                lifetime: 20 + Math.random() * 30,
                age: 0,
                active: false,
                activationDelay: Math.random() * 100
            });
        }
        
        return {
            group: sparkGroup,
            particles: sparkParticles,
            activate: function() {
                this.particles.forEach(particle => {
                    if (Math.random() < 0.3) { // Randomly activate only some particles
                        particle.active = true;
                        particle.age = 0;
                        particle.mesh.visible = true;
                        particle.mesh.position.set(0, 0, 0);
                        particle.mesh.scale.set(1, 1, 1);
                    }
                });
            }
        };
    };
    
    // Create spark effects at each terminal
    const primarySpark1 = createSparkEffect(new THREE.Vector3(1.7, 2, 0.5));
    const primarySpark2 = createSparkEffect(new THREE.Vector3(-1.7, 2, 0.5));
    const secondarySpark1 = createSparkEffect(new THREE.Vector3(1.7, -2, 0.5));
    const secondarySpark2 = createSparkEffect(new THREE.Vector3(-1.7, -2, 0.5));
    
    // Create glow effect for the core
    const createGlowEffect = () => {
        const glowMaterial = new THREE.MeshBasicMaterial({
            color: 0xff2a1a,
            transparent: true,
            opacity: 0.15,
            side: THREE.BackSide
        });
        
        const glowGeometry = new THREE.BoxGeometry(4.2, 5.2, 3.7);
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        glow.position.z = 0.5;
        transformerGroup.add(glow);
        
        return {
            mesh: glow,
            pulseRate: 0.03,
            initialOpacity: 0.15
        };
    };
    
    const coreGlow = createGlowEffect();
    
    // Controls with enhanced features
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let rotationSpeed = { x: 0, y: 0.003 };
    let damping = 0.95;
    
    container.addEventListener('mousedown', (e) => {
        isDragging = true;
        previousMousePosition = {
            x: e.offsetX,
            y: e.offsetY
        };
        // Stop auto-rotation when user interacts
        rotationSpeed = { x: 0, y: 0 };
    });
    
    container.addEventListener('mouseup', () => {
        isDragging = false;
    });
    
    container.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        
        const deltaMove = {
            x: e.offsetX - previousMousePosition.x,
            y: e.offsetY - previousMousePosition.y
        };
        
        // Update rotation speed based on mouse movement
        rotationSpeed.x = deltaMove.y * 0.0005;
        rotationSpeed.y = deltaMove.x * 0.0005;
        
        previousMousePosition = {
            x: e.offsetX,
            y: e.offsetY
        };
    });
    
    container.addEventListener('mouseleave', () => {
        isDragging = false;
    });
    
    // Add mouse wheel zoom
    container.addEventListener('wheel', (e) => {
        e.preventDefault();
        
        // Adjust camera zoom
        const zoomSpeed = 0.1;
        if (e.deltaY > 0) {
            // Zoom out
            camera.position.z = Math.min(20, camera.position.z + zoomSpeed);
        } else {
            // Zoom in
            camera.position.z = Math.max(5, camera.position.z - zoomSpeed);
        }
    });
    
    // Add double-click to reset view
    container.addEventListener('dblclick', () => {
        // Reset camera position
        camera.position.set(4, 4, 12);
        camera.lookAt(0, 0, 0);
        
        // Reset transformer rotation
        transformerGroup.rotation.x = 0;
        transformerGroup.rotation.y = 0;
        transformerGroup.rotation.z = 0;
        
        // Reset rotation speed
        rotationSpeed = { x: 0, y: 0.003 };
    });
    
    // Add instructions overlay
    const instructionsDiv = document.createElement('div');
    instructionsDiv.style.position = 'absolute';
    instructionsDiv.style.bottom = '10px';
    instructionsDiv.style.left = '10px';
    instructionsDiv.style.padding = '8px 12px';
    instructionsDiv.style.backgroundColor = 'rgba(0,0,0,0.6)';
    instructionsDiv.style.color = 'white';
    instructionsDiv.style.borderRadius = '5px';
    instructionsDiv.style.fontSize = '12px';
    instructionsDiv.style.fontFamily = 'Arial, sans-serif';
    instructionsDiv.innerHTML = 'Mouse: Drag to rotate | Scroll: Zoom | Double-click: Reset view';
    container.appendChild(instructionsDiv);
    
    // Animation variables
    let timer = 0;
    let sparkTimer = 0;
    
    // Animation loop with enhanced effects
    function animate() {
        requestAnimationFrame(animate);
        
        // Update timer
        timer += 0.05;
        sparkTimer += 1;
        
        // Apply inertial rotation when not dragging
        if (!isDragging) {
            transformerGroup.rotation.x += rotationSpeed.x;
            transformerGroup.rotation.y += rotationSpeed.y;
            
            // Apply damping to gradually slow down rotation
            rotationSpeed.x *= damping;
            rotationSpeed.y *= damping;
        }
        
        // Animate heat particles for iron losses
        ironLossesGroup.children.forEach(particle => {
            const userData = particle.userData;
            
            // Update position with smoother motion
            particle.position.x += userData.direction.x * userData.speed;
            particle.position.y += userData.direction.y * userData.speed;
            particle.position.z += userData.direction.z * userData.speed;
            
            // Pulsing effect for heat particles
            const pulseFactor = 0.3 * Math.sin(timer * userData.pulseSpeed + userData.pulsePhase) + 0.7;
            particle.scale.set(pulseFactor, pulseFactor, pulseFactor);
            
            // Update age/lifetime
            userData.age += 1;
            
            // If particle is too old, reset it
            if (userData.age > userData.lifetime) {
                // Reset position to near the core
                particle.position.x = (Math.random() - 0.5) * 5;
                particle.position.y = (Math.random() - 0.5) * 6;
                particle.position.z = (Math.random() - 0.5) * 3;
                
                // Reset age
                userData.age = 0;
                userData.lifetime = Math.random() * 150 + 50;
                
                // New direction
                userData.direction = new THREE.Vector3(
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2
                ).normalize();
                
                // New pulse phase
                userData.pulsePhase = Math.random() * Math.PI * 2;
            }
            
            // Particle fades out as it ages with non-linear falloff
            const ageRatio = userData.age / userData.lifetime;
            particle.material.opacity = userData.initialOpacity * (1 - ageRatio * ageRatio);
        });
        
        // Animate magnetic field lines
        magneticFieldGroup.children.forEach(fieldLine => {
            const userData = fieldLine.userData;
            
            // Pulsating opacity for magnetic field
            const pulseValue = Math.sin(timer * userData.pulseRate + userData.pulsePhase) * 0.5 + 0.5;
            fieldLine.material.opacity = userData.initialOpacity * pulseValue;
            
            // Subtle size variation
            const scaleFactor = 0.95 + 0.1 * pulseValue;
            fieldLine.scale.set(scaleFactor, scaleFactor, scaleFactor);
            
            // Rotate the field lines slowly in different directions
            fieldLine.rotation.y += 0.002;
        });
        
        // Animate electricity particles with enhanced effects
        // Primary winding particles
        primaryElectricityParticles.forEach((particle, index) => {
            particle.mesh.visible = true;
            particle.tail.visible = true;
            particle.angle += particle.speed;
            
            // Position particles in a circle around the primary winding
            const x = Math.cos(particle.angle + timer) * particle.radius;
            const z = Math.sin(particle.angle + timer) * particle.radius;
            particle.mesh.position.x = x;
            particle.mesh.position.z = z;
            particle.mesh.position.y = particle.yPos;
            
            // Position the tail behind the particle
            particle.tail.position.x = x - 0.2 * Math.cos(particle.angle + timer);
            particle.tail.position.z = z - 0.2 * Math.sin(particle.angle + timer);
            particle.tail.position.y = particle.yPos;
            
            // Rotate tail to follow the direction of movement
            particle.tail.rotation.x = Math.PI / 2;
            particle.tail.rotation.z = -particle.angle - timer;
                        // Pulse effect for particles
            const pulseFactor = 0.8 + 0.2 * Math.sin(timer * 0.1 + particle.pulsePhase);
            particle.mesh.scale.set(pulseFactor, pulseFactor, pulseFactor);
            particle.tail.scale.set(pulseFactor, pulseFactor, pulseFactor);

            // Fade tail based on distance from particle
            const tailOpacity = 0.6 * (1 - Math.abs(Math.sin(particle.angle + timer)));
            particle.tail.material.opacity = tailOpacity;
        });

        // Secondary winding particles
        secondaryElectricityParticles.forEach((particle, index) => {
            particle.mesh.visible = true;
            particle.tail.visible = true;
            particle.angle += particle.speed;

            // Position particles in a circle around the secondary winding
            const x = Math.cos(particle.angle + timer) * particle.radius;
            const z = Math.sin(particle.angle + timer) * particle.radius;
            particle.mesh.position.x = x;
            particle.mesh.position.z = z;
            particle.mesh.position.y = particle.yPos;

            // Position the tail behind the particle
            particle.tail.position.x = x - 0.2 * Math.cos(particle.angle + timer);
            particle.tail.position.z = z - 0.2 * Math.sin(particle.angle + timer);
            particle.tail.position.y = particle.yPos;

            // Rotate tail to follow the direction of movement
            particle.tail.rotation.x = Math.PI / 2;
            particle.tail.rotation.z = -particle.angle - timer;

            // Pulse effect for particles
            const pulseFactor = 0.8 + 0.2 * Math.sin(timer * 0.1 + particle.pulsePhase);
            particle.mesh.scale.set(pulseFactor, pulseFactor, pulseFactor);
            particle.tail.scale.set(pulseFactor, pulseFactor, pulseFactor);

            // Fade tail based on distance from particle
            const tailOpacity = 0.6 * (1 - Math.abs(Math.sin(particle.angle + timer)));
            particle.tail.material.opacity = tailOpacity;
        });

        // Animate spark effects at terminals
        if (sparkTimer % 60 === 0) {
            // Randomly activate spark effects
            if (Math.random() < 0.5) primarySpark1.activate();
            if (Math.random() < 0.5) primarySpark2.activate();
            if (Math.random() < 0.5) secondarySpark1.activate();
            if (Math.random() < 0.5) secondarySpark2.activate();
        }

        // Update spark particles
        [primarySpark1, primarySpark2, secondarySpark1, secondarySpark2].forEach(sparkEffect => {
            sparkEffect.particles.forEach(particle => {
                if (particle.active) {
                    particle.age += 1;

                    // Move particle along its direction
                    particle.mesh.position.x += particle.direction.x * particle.speed;
                    particle.mesh.position.y += particle.direction.y * particle.speed;
                    particle.mesh.position.z += particle.direction.z * particle.speed;

                    // Fade out particle as it ages
                    const ageRatio = particle.age / particle.lifetime;
                    particle.mesh.material.opacity = 0.8 * (1 - ageRatio);

                    // Scale down particle as it ages
                    particle.mesh.scale.set(1 - ageRatio, 1 - ageRatio, 1 - ageRatio);

                    // Deactivate particle if it exceeds its lifetime
                    if (particle.age > particle.lifetime) {
                        particle.active = false;
                        particle.mesh.visible = false;
                    }
                }
            });
        });

        // Animate core glow effect
        const glowPulse = Math.sin(timer * coreGlow.pulseRate) * 0.5 + 0.5;
        coreGlow.mesh.material.opacity = coreGlow.initialOpacity * glowPulse;

        // Update labels position based on camera
        labels.forEach(label => {
            const screenPosition = label.position.clone().project(camera);
            const x = (screenPosition.x * 0.5 + 0.5) * container.clientWidth;
            const y = (-screenPosition.y * 0.5 + 0.5) * container.clientHeight;

            label.element.style.left = `${x}px`;
            label.element.style.top = `${y}px`;
        });

        // Render the scene
        renderer.render(scene, camera);
    }

    // Start the animation loop
    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
        const width = container.clientWidth;
        const height = container.clientHeight;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        renderer.setSize(width, height);
    });
}

// Initialize the visualization
initTransformerVisualization();
</script>
""", height=600)
else:
    st.info("Toggle the checkbox above to view the interactive 3D transformer model.")
    
st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
<div style="text-align: center; padding: 20px; font-size: 14px; color: #aaa;">
    <p>⚡ Powered by <strong>Streamlit</strong>, <strong>Plotly</strong>, and <strong>Three.js</strong></p>
    <p>© 2025 Transformer Analyzer. All Rights Reserved.</p>
    <p style="font-size: 12px;">Designed with ❤️ for Engineers & Researchers.</p>
</div>
""", unsafe_allow_html=True)

