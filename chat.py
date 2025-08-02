from flask import Flask, render_template, request
import google.generativeai as genai
import markdown

app = Flask(__name__)

gorevler = []

def genai_chat(soru, gorevler):
    genai.configure(api_key="AIzaSyAj0mKZ-10EarOxivLMTAEy_tSr3-FVwws")
    model = genai.GenerativeModel('models/gemini-2.5-pro')

    gorev_listesi_str = "\n".join(f"- {g}" for g in gorevler) if gorevler else "Görev yok."

    prompt = f"""
    Aşağıdaki görevler mevcut:
    {gorev_listesi_str}

    Bu görevleri göz önünde bulundurarak aşağıdaki soruya yanıt ver:
    {soru}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"API isteği sırasında bir hata oluştu: {e}"


@app.route("/", methods=["GET", "POST"])
def index():
    cevap = None
    active_tab = 'gorevler'
    if request.method == "POST":
        form_type = request.form.get("form_type")
        
        if form_type == "gorev_formu":
            if "gorev" in request.form:
                gorev = request.form["gorev"]
                gorevler.append(gorev)
                active_tab = 'gorevler'

        
        elif form_type == "ai_formu":
            if "soru" in request.form:
                soru = request.form["soru"]
                raw_cevap = genai_chat(soru, gorevler)
                
                
                cevap = markdown.markdown(raw_cevap)
            active_tab = 'ai'


    return render_template("index.html", gorevler=gorevler, cevap=cevap, active_tab=active_tab)

if __name__ == "__main__":
    app.run(debug=True)