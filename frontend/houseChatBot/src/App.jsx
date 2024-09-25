import React from "react"
import ChatBar from "./components/ChatBar"
import NewChat from "./components/NewChat"

function App() {

  const [actualModel, setActualModel] = React.useState('Leafy')
  const [responses, setResponses] = React.useState([])


  return (
    <div>
    <div className="flex py-5 rounded-b-xl justify-between px-10 bg-slate-950 text-white shadow-lg shadow-slate-600">
      <h1 className="text-4xl font-bold text-center">{actualModel}</h1>
      <NewChat setActualModel={setActualModel} setResponses={setResponses} actualModel={actualModel}/>
    </div> 
      <ChatBar actualModel={actualModel} responses={responses} setResponses={setResponses}/>
    </div>
  )
}

export default App
