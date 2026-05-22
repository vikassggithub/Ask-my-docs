from fpdf import FPDF

# PDF 1: Artificial Intelligence
pdf1 = FPDF()
pdf1.add_page()
pdf1.set_font("Arial", size=12)
pdf1.multi_cell(190, 10, "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn. Machine learning is a subset of AI that enables systems to learn from data. Deep learning uses neural networks with multiple layers. AI applications include natural language processing, computer vision, and robotics. The future of AI includes autonomous systems and general artificial intelligence.")
pdf1.output("AI_Overview.pdf")

# PDF 2: Climate Change
pdf2 = FPDF()
pdf2.add_page()
pdf2.set_font("Arial", size=12)
pdf2.multi_cell(190, 10, "Climate change refers to long-term shifts in temperatures and weather patterns. The main causes include burning fossil fuels, deforestation, and industrial processes. Global temperatures have risen 1.1°C since pre-industrial times. Sea levels are rising at 3.3mm per year. Solutions include renewable energy, electric vehicles, and reforestation.")
pdf2.output("Climate_Report.pdf")

# PDF 3: Health Guidelines
pdf3 = FPDF()
pdf3.add_page()
pdf3.set_font("Arial", size=12)
pdf3.multi_cell(190, 10, "WHO recommends 150-300 minutes of moderate exercise per week. A balanced diet should include fruits, vegetables, whole grains, and lean proteins. Adults need 7-9 hours of sleep daily. Regular health checkups are important. Stay hydrated with 2-3 liters of water daily. Avoid smoking and limit alcohol consumption.")
pdf3.output("Health_Guidelines.pdf")

print("✅ 3 PDFs created successfully!")
print("1. AI_Overview.pdf")
print("2. Climate_Report.pdf")
print("3. Health_Guidelines.pdf")