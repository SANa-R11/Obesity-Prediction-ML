from flask import Flask,render_template,request
import pickle
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()

app=Flask(__name__)

with open("sc_obes.pkl","rb")as file:
    sc_obesity=pickle.load(file)

with open("rf_obesity_model.pkl","rb")as file:
    obesity_model=pickle.load(file)

with open("lb_obesity.pkl","rb")as file:
    lb_obesity=pickle.load(file)

with open("lb1_obesity.pkl","rb")as file:
    lb1_obesity=pickle.load(file)

with open("lb2_obesity.pkl","rb")as file:
    lb2_obesity=pickle.load(file)

with open("lb3_obesity.pkl","rb")as file:
    lb3_obesity=pickle.load(file)

def obesityPrediction(Gender="Male", Age=43, Height=180, Weight=87, family_history="no", FAVC="no", FCVC=2,NCP=3, CAEC="Sometimes", SMOKE="no", CH2O=2, SCC="no", FAF=3, TUE=1 ,CALC="Sometimes", MTRANS="Bike"):
    lst=[]
    if Gender=="Female":
        lst=lst+[0]
    elif Gender=="Male":
        lst=lst+[1]

    lst=lst+[Age]
    lst=lst+[Height]
    lst=lst+[Weight]
    
    if family_history=="no":
        lst=lst+[0]
    elif family_history=="yes":
        lst=lst+[1]
        
    if FAVC=="no":
        lst=lst+[0]
    elif FAVC=="yes":
        lst=lst+[1]
        
    lst=lst+[FCVC]
    lst=lst+[NCP]
    
    CAEC=lb_obesity.transform([CAEC])
    lst=lst+list(CAEC)
    
    if SMOKE=="no":
        lst=lst+[0]
    elif SMOKE=="yes":
        lst=lst+[1]

    lst=lst+[CH2O]
    
    if SCC=="no":
        lst=lst+[0]
    elif SCC=="yes":
        lst=lst+[1]

    lst=lst+[FAF]
    lst=lst+[TUE]
    
    CALC=lb1_obesity.transform([CALC])
    lst=lst+list(CALC)

    MTRANS=lb2_obesity.transform([MTRANS])
    lst=lst+list(MTRANS)

    print(f"Feature vector before scaling (length={len(lst)}):", lst)

    lst=sc_obesity.transform([lst])
    
    result=obesity_model.predict(lst)
    print(result)
    if result==0:
        return "Insufficient Weight"
    elif result==1:
        return 'Normal Weight'
    elif result==2:
        return 'Obesity Type I'
    elif result==3:
        return 'Obesity Type II'
    elif result==4:
        return 'Obesity Type III'
    elif result==5:
        return 'Overweight Level I'
    elif result==6:
        return 'Overweight Level II'
    


@app.route("/",methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method=="POST":
        gender=request.form.get("gender")
        age=float(request.form.get("age"))
        height=float(request.form.get("height"))
        weight=float(request.form.get("weight"))
        family_history=(request.form.get("family_history"))
        favc=(request.form.get("FAVC"))
        fcvc=float(request.form.get("FCVC"))
        ncp=float(request.form.get("NCP"))
        caec=(request.form.get("CAEC"))
        smoke=(request.form.get("SMOKE"))
        ch20=float(request.form.get("CH2O"))
        scc=(request.form.get("SCC"))
        faf=float(request.form.get("FAF"))
        tue=float(request.form.get("TUE"))
        calc=(request.form.get("CALC"))
        mtrans=(request.form.get("MTRANS"))

        result=obesityPrediction(Gender=gender, Age=age, Height=height, Weight=weight, family_history=family_history, FAVC=favc, FCVC=fcvc,NCP=ncp, CAEC=caec, SMOKE=smoke, CH2O=ch20, SCC=scc, FAF=faf, TUE=tue ,CALC=calc, MTRANS=mtrans)

        return render_template("predict.html", prediction=result)

    return render_template("predict.html")

@app.route("/contact",methods=["GET"])
def contact():
    return render_template("contact.html")

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
