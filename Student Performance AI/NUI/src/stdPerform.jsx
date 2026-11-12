import { useState } from "react"

function stdPerform(){

    const [studytime, setStudytime] = useState("")
    const [G2, setG2] = useState("")
    const [absences, setAbsences] = useState("")
    const [freetime, setFreetime] = useState("")
    const [dalc, setDalc] = useState("")
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    
    const predict = async() =>{
        if(!studytime || !G2 || !absences || !freetime || !dalc){
            alert("Please fill all the Details")
            return
        }
        setLoading(true)
        setResult(null)
        const data = {
            studytime: Number(studytime),
            G2: Number(G2),
            absences: Number(absences),
            freetime: Number(freetime),
            Dalc: Number(dalc)
        }
            console.log(data)

        try{
            console.log(data)
            const response = await fetch("http://127.0.0.1:8000/predict",{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })

            const res = await response.json()
            setResult(res)
        }
        catch(error) {
            console.error("Prediction error: ",error)
        }       
        
        finally{
          setLoading(false)  
        }
    }

    return(
        <div className="container">
            <h1 className="welcome">Welcome to the Student Performance Predictor AI</h1>
            <h2 className="welcome">Enter Your Student Details</h2>
            <div className="inputContainer">
            <input placeholder="Study Time"
              value={studytime}
              onChange={(e) => setStudytime(e.target.value)}
            /><br/>
            
            <input placeholder="G2"
              value={G2}
              onChange={(e) => setG2(e.target.value)}
            /><br/>

            <input placeholder="Absences"
              value={absences}
              onChange={(e) => setAbsences(e.target.value)}
            /><br/>

            <input placeholder="Free Time"
              value={freetime}
              onChange={(e) => setFreetime(e.target.value)}
            /><br/>

            <input placeholder="Dalc"
              value={dalc}
              onChange={(e) => setDalc(e.target.value)}
            /><br/><br/>
         

            <button className="prtbtn" onClick={predict} disabled={loading}>
                {loading ? "Predicting..." : "Predict"}
            </button><br/>
            
            {result && (
                <div className="result">
                    <h3>Score: {result.Prediction_score}</h3>
                    <p>Performance: {result.Performance}</p><br/>
                    <h2>Top Factors Affecting This Prediction</h2><br/>
                    <p>Main factor improving score: {result.Positive_Factors}</p><br/>
                    <p>Main factor reducing score: {result.Negative_Factors}</p><br/>
                    <p>Suggesstion: {result.Suggestion}</p>
                </div>
            )}

            </div>
           </div>
    )
}
export default stdPerform